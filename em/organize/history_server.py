"""
Improved FastAPI server for asynchronous incremental history processing
without blocking clients when reading history.

Key improvements:
- Writes (update + forgetting) are protected by a lock
- Reads NEVER wait for writes: clients always read a cached, pickled snapshot
- After every write, a fresh snapshot is generated atomically

Endpoints:
POST /update      → enqueue pickled SceneGraphInstant for processing
GET /history      → retrieve latest pickled HigherLevelSummary snapshot

This is an architecture template; plug in your real classes.
"""
import asyncio
import io
import json
import os
import pickle
import sys
import traceback
from collections import namedtuple
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from time import time
from typing import List, Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, UploadFile, HTTPException, Body, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import Response, JSONResponse, HTMLResponse

from lmp.setup import instantiate_llm
from .forget import ForgettingManager
from .language_rule_relevance import LanguageRuleBasedRelevanceEstimator, LanguageRuleManager
from ..armarx_mem_incremental import ArmarXMemoryIncrementalTreeBuilder
from ..em_tree import SceneGraphInstant, HigherLevelSummary, iter_nodes_of_type

sys.path.append(str((Path(__file__).parent.parent.parent / 'experiments/demo').absolute()))

_BATCH_SIZE = 25


# noinspection PyTypeChecker
def _setup_model():
    global _BATCH_SIZE
    from langchain_community.cache import SQLiteCache
    import langchain.globals
    langchain.globals.set_llm_cache(SQLiteCache(database_path="armar-live-langchain-cache.db"))
    langchain.globals.set_debug(True)

    cfg_file = Path(__file__).parent / 'armar_server_cfg.json'
    cfg = json.loads(cfg_file.read_text())
    tree_builder_conf = cfg['builder']
    _BATCH_SIZE = tree_builder_conf.pop('batch_size', _BATCH_SIZE)
    forget_conf = cfg['forget']
    rule_mod_llm = cfg['rule_mod_llm']
    relevance_file = Path(__file__).parent / 'armar_relevance_rules.json'
    tree_builder_llm = instantiate_llm(tree_builder_conf.pop('llm'))
    hist_builder = ArmarXMemoryIncrementalTreeBuilder(
        llm=tree_builder_llm,
        action_param_summarizer_llm=tree_builder_llm,
        relevance_language_rule_file_path=relevance_file,
        **tree_builder_conf,
    )
    rule_mng = LanguageRuleManager(
        relevance_file,
        rule_modifier_llm=instantiate_llm(rule_mod_llm)
    )
    forget_manager = ForgettingManager(
        relevance_estimators=[
            LanguageRuleBasedRelevanceEstimator(
                estimation_llm=instantiate_llm(forget_conf.pop('llm')),
                rule_manager=rule_mng,
                **forget_conf
            )
        ]
    )
    return hist_builder, forget_manager, rule_mng


# =====================
# Global State
# =====================
history_builder, forgetting_manager, rule_manager = _setup_model()

# Queue carries batches: each item is a List[SceneGraphInstant]
update_queue: "asyncio.Queue[List[SceneGraphInstant]]" = asyncio.Queue()
latest_timestamp = datetime.fromtimestamp(0)

# The live mutable history tree (mutated under history_lock)
current_history: Optional[HigherLevelSummary] = None

# The pickled snapshot returned to clients immediately (always consistent)
history_snapshot_bytes: Optional[bytes] = None

# Lock to serialize writers (builder + forgetting)
history_lock = asyncio.Lock()

latest_timestamp_lock = asyncio.Lock()

_SNAPSHOT_FINISHED_FILE = Path(__file__).parent / 'time_snapshot_finished.log'
_RECEIVED_UPDATES_FILE = Path(__file__).parent / 'time_received_update.log'
_NUM_SCENES_IN_QUEUE_FILE = Path(__file__).parent / 'time_to_num_scenes_in_queue.log'
_NUM_SCENES_IN_TREE_FILE = Path(__file__).parent / 'time_to_num_scenes_in_tree.log'
snapshot_finished_log = _SNAPSHOT_FINISHED_FILE.open('a')
received_updates_log = _RECEIVED_UPDATES_FILE.open('a')
num_scenes_in_queue_log = _NUM_SCENES_IN_QUEUE_FILE.open('a')
num_scenes_in_tree_log = _NUM_SCENES_IN_TREE_FILE.open('a')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await on_startup()
    yield
    # Could do shut down logic here


app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=16000, compresslevel=5)

# =====================
# Snapshot Helpers
# =====================
SNAPSHOT_FILE = Path(__file__).parent / "armar_history_snapshot.pkl"
Snapshot = namedtuple('Snapshot', ['bytes', 'range_end', 'num_scenes'])


def create_snapshot(history: HigherLevelSummary) -> Snapshot:
    """Synchronous pickling of history. Keep sync so it can be run in a thread."""
    num_scenes = len(list(iter_nodes_of_type(history, SceneGraphInstant)))
    return Snapshot(pickle.dumps(history),
                    history.range[-1].timestamp(),
                    num_scenes)


def _write_snapshot_sync(snapshot: Snapshot) -> None:
    """Synchronous write to disk (used inside a thread)."""
    if SNAPSHOT_FILE.is_file():
        SNAPSHOT_FILE.rename(SNAPSHOT_FILE.with_stem(SNAPSHOT_FILE.stem + f'_{time()}'))
    SNAPSHOT_FILE.write_bytes(snapshot.bytes)

    # Logging
    print(f'{time()}: {snapshot.range_end}', file=snapshot_finished_log, flush=True)
    print(f'{time()}: {snapshot.num_scenes}', file=num_scenes_in_tree_log, flush=True)


async def async_write_snapshot(*args) -> None:
    """Write snapshot to disk without blocking event-loop."""
    await asyncio.to_thread(_write_snapshot_sync, *args)


async def refresh_snapshot(history: HigherLevelSummary) -> bytes:
    """
    Create a pickled snapshot and schedule asynchronous disk write.
    Returns the snapshot bytes.
    """
    snapshot = await asyncio.to_thread(create_snapshot, history)
    # schedule non-blocking disk write (fire-and-forget)
    asyncio.create_task(async_write_snapshot(snapshot))

    return snapshot.bytes


def _log_scenes_in_queue():
    try:
        # this a hack to estimate the size of the queue, does not need to be reliable
        num_scenes_in_queue = 0
        # noinspection PyUnresolvedReferences
        for batch in update_queue._queue:
            num_scenes_in_queue += len(batch)
        print(f'{time()}: {num_scenes_in_queue}', file=num_scenes_in_queue_log, flush=True)
    except:
        traceback.print_exc()
        pass


# =====================
# Background worker for updates
# =====================
def _run_history_builder(scenes: List[SceneGraphInstant]):
    try:
        yield from history_builder.process_batch(scenes, max_new_scene_batch=_BATCH_SIZE)
    except BaseException as e:
        failure_file = SNAPSHOT_FILE.with_name(f'failure-input-{time()}.pkl')
        failure_file.write_bytes(pickle.dumps(scenes))
        print('History builder failed with', e,
              '. Wrote error-causing input to', failure_file)
        raise


async def _to_async_iterable(sync_iterable):
    # to_thread errors if StopIteration raised in it. So we use a sentinel to detect the end
    done = object()
    it = iter(sync_iterable)
    while (value := await asyncio.to_thread(next, it, done)) is not done:
        yield value


async def update_worker() -> None:
    """
    Worker that merges all currently queued update batches into one list
    before processing. This provides best-effort batching and reduces lock
    contention while ensuring the tree is always modified atomically.
    """
    global current_history, history_snapshot_bytes

    while True:
        # Always take at least one batch
        first_batch = await update_queue.get()
        merged: List[SceneGraphInstant] = list(first_batch)

        # Non-blocking merge: drain everything currently queued
        while True:
            try:
                next_batch = update_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            else:
                merged.extend(next_batch)
                update_queue.task_done()

        asyncio.create_task(asyncio.to_thread(_log_scenes_in_queue))

        try:
            async with history_lock:
                # Process the merged batch
                async for hist in _to_async_iterable(_run_history_builder(merged)):
                    current_history = hist
                    # Refresh snapshot and schedule async disk write
                    history_snapshot_bytes = await refresh_snapshot(current_history)

                # Forgetting is applied after each step, but can be cancelled by new updates
                if update_queue.qsize() == 0:  # Only an estimate here, but forgetting can be cancelled anyway
                    await forgetting_manager.modify(current_history)
                    history_snapshot_bytes = await refresh_snapshot(current_history)

        except Exception:
            traceback.print_exc()
            raise
        finally:
            update_queue.task_done()


# =====================
# Scheduled forgetting job
# =====================
async def scheduled_forgetting() -> None:
    global current_history, history_snapshot_bytes

    async with history_lock:
        if current_history is not None:
            await forgetting_manager.modify(current_history)
            # Refresh snapshot and persist asynchronously
            history_snapshot_bytes = await refresh_snapshot(current_history)


# =====================
# API Endpoints
# =====================
@app.post("/update")
async def update_scene(ensure_latest_timestamp: str, file: UploadFile):
    """
    Accept a pickled SceneGraphInstant or a pickled list of them.
    The payload should be a pickle serialized object.
    Returns immediately after enqueuing the batch.
    """
    global latest_timestamp

    data = await file.read()
    try:
        obj = pickle.loads(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid pickle payload: {e}")

    # Normalize to list of SceneGraphInstant
    if isinstance(obj, list):
        scenes = obj
    else:
        scenes = [obj]
    scenes.sort(key=lambda s: s.raw.timestamp)

    if not scenes:
        raise HTTPException(status_code=400, detail="Empty scene list")

    try:
        ensure_latest_timestamp = datetime.fromtimestamp(float(ensure_latest_timestamp))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid latest timestamp: {e}")

    async with latest_timestamp_lock:
        if ensure_latest_timestamp != latest_timestamp:
            raise HTTPException(status_code=409, detail='Latest timestamp did not match expectations. '
                                                        'Concurrent update likely')

        await update_queue.put(scenes)

        # Logging
        latest_timestamp = scenes[-1].raw.timestamp
        print(f'{time()}: {latest_timestamp.timestamp()}', file=received_updates_log, flush=True)
        _log_scenes_in_queue()
    forgetting_manager.cancel_forgetting()

    return JSONResponse({"status": "queued", "queued_batch_size": len(scenes)})


@app.post("/feedback")
async def receive_history_feedback(feedback: str = Body(...)):
    rule_manager.incorporate_feedback(feedback)
    return {"status": "ok"}


@app.get("/history")
async def get_history():
    """Return the latest pickled HigherLevelSummary snapshot."""
    if history_snapshot_bytes is None:
        return Response(status_code=204)
    return Response(content=history_snapshot_bytes, media_type="application/octet-stream")


@app.get("/latest")
async def get_latest_timestamp():
    """Return the latest scene timestamp received."""
    async with latest_timestamp_lock:
        return latest_timestamp.timestamp()


@app.get("/health")
async def health():
    return {"status": "ok", "queue_size": update_queue.qsize()}


# =====================
# Progress visualization
# =====================

def _load_log(path: Path):
    times = []
    values = []
    if not path.exists():
        return times, values
    with path.open('r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                t, v = map(float, line.split(":"))
            except Exception:
                continue
            times.append(t)
            values.append(v)
    return times, values


def _filter_by_range(times, vals, start_ts, end_ts, include_edges=False):
    """Filter parallel lists times[] and vals[] by optional start_ts/end_ts (unix seconds).
       If start_ts or end_ts is None, that side is unbounded."""
    if start_ts is None and end_ts is None:
        return times, vals
    assert sorted(times) == times
    out_t, out_v = [], []
    prev_val, after_val = None, None
    for t, v in zip(times, vals):
        if start_ts is not None and t < start_ts:
            prev_val = v
            continue
        if end_ts is not None and t > end_ts:
            after_val = v
            break
        out_t.append(t)
        out_v.append(v)
    if include_edges and prev_val is not None:
        out_t.insert(0, start_ts)
        out_v.insert(0, prev_val)
    if include_edges and after_val is not None:
        out_t.append(end_ts)
        out_v.append(after_val)
    return out_t, out_v


@app.get("/progress")
def progress_plot(start: float = None, end: float = None, include_edges: bool = False):
    """
    Generate PNG plot with:
      - X axis: absolute wall-clock time (datetime)
      - Y axis: item timestamp (datetime)
    Optional query params:
      start, end = unix timestamps in seconds to filter the data range.
    """
    proc_times, proc_values = _load_log(_SNAPSHOT_FINISHED_FILE)
    recv_times, recv_values = _load_log(_RECEIVED_UPDATES_FILE)

    # Apply start/end filters (they are unix timestamps)
    proc_times_f, proc_values_f = _filter_by_range(proc_times, proc_values, start, end, include_edges)
    recv_times_f, recv_values_f = _filter_by_range(recv_times, recv_values, start, end, include_edges)

    # Convert X axis times to datetime objects (absolute)
    proc_x = [datetime.fromtimestamp(t) for t in proc_times_f]
    recv_x = [datetime.fromtimestamp(t) for t in recv_times_f]

    # Convert Y axis timestamps → datetime objects (these are item times)
    proc_y = [datetime.fromtimestamp(v) for v in proc_values_f]
    recv_y = [datetime.fromtimestamp(v) for v in recv_values_f]

    fig, ax = plt.subplots(figsize=(10, 6))

    if proc_x or recv_x:
        if proc_x:
            ax.step(proc_x, proc_y, where="post", label="Processed", linewidth=2)
        if recv_x:
            ax.step(recv_x, recv_y, where="post", label="Received", linewidth=2)

        ax.set_xlabel("Wall-clock time")
        ax.set_ylabel("Item time")

        # Format X axis as readable datetimes
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))

        # Format Y axis as readable datetimes (same style)
        ax.yaxis.set_major_locator(mdates.AutoDateLocator())
        ax.yaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))

        ax.set_title("Online Algorithm Progress (received vs processed)")
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()  # rotate x labels if needed
    else:
        ax.text(0.5, 0.5,
                "No data found\n"
                f"({_SNAPSHOT_FINISHED_FILE}, {_RECEIVED_UPDATES_FILE})",
                ha="center", va="center", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="pdf", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)

    return Response(buf.getvalue(), media_type="application/pdf")


@app.get("/queue_tree_plot")
def queue_tree_plot(start: float = None, end: float = None, include_edges: bool = False):
    """
    Plot queue/tree sizes over absolute time (X axis is wall-clock datetime).
    Optional query params:
      start, end = unix timestamps in seconds to filter the data range.
    """
    queue_times, queue_vals = _load_log(_NUM_SCENES_IN_QUEUE_FILE)
    tree_times, tree_vals = _load_log(_NUM_SCENES_IN_TREE_FILE)

    # apply range filters
    queue_times_f, queue_vals_f = _filter_by_range(queue_times, queue_vals, start, end, include_edges)
    tree_times_f, tree_vals_f = _filter_by_range(tree_times, tree_vals, start, end, include_edges)

    # convert times to datetimes
    queue_x = [datetime.fromtimestamp(t) for t in queue_times_f]
    tree_x = [datetime.fromtimestamp(t) for t in tree_times_f]

    fig, ax = plt.subplots(figsize=(10, 6))

    if queue_x or tree_x:
        if tree_x:
            ax.step(tree_x, tree_vals_f, where="post", label="Tree size", linewidth=2)
        if queue_x:
            ax.step(queue_x, queue_vals_f, where="post", label="Queue size", linewidth=2)

        ax.set_xlabel("Wall-clock time")
        ax.set_ylabel("Number of scenes")
        ax.set_title("Queue / Tree Size Over Time")

        # format x-axis as dates
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M:%S"))
        ax.grid(True)
        ax.legend()
        fig.autofmt_xdate()
    else:
        ax.text(0.5, 0.5,
                "No data found\n"
                f"({_NUM_SCENES_IN_QUEUE_FILE}, {_NUM_SCENES_IN_TREE_FILE})",
                ha="center", va="center", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="pdf", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)

    return Response(buf.getvalue(), media_type="application/pdf")


# HTML template for the view page; JS replaces only <img> periodically.
# The page exposes datetime-local pickers for start/end for each plot.
VIEW_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Online Algorithm Progress</title>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial; background: #f7f7f7; }
    .container { max-width: 980px; margin: 24px auto; text-align: center; }
    img { box-shadow: 0 2px 6px rgba(0,0,0,0.12); background: white; border: 1px solid #ddd; margin-top: 20px; }
    .controls { margin-bottom: 12px; }
    label { margin-right: 6px; }
    input[type="number"] { width: 80px; padding: 4px; }
    input[type="datetime-local"] { padding: 4px; margin: 0 6px; }
    button { padding: 6px 10px; margin-left: 8px; }
    small { color: #666; display:block; margin-top:6px; }
    .section { margin-top: 32px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Online Algorithm Progress</h1>

    <div class="controls">
      <label for="refresh_ms">Refresh (ms):</label>
      <input id="refresh_ms" type="number" min="200" value="{{ refresh }}" />

      <span style="margin-left:20px"></span>

      <label for="start_time">Start:</label>
      <input id="start_time" type="datetime-local">

      <label for="end_time">End:</label>
      <input id="end_time" type="datetime-local">

      <label for="include_edges">Force edges</label>
      <input id="include_edges" type="checkbox">

      <button id="apply">Apply</button>
      <button id="pause">Pause</button>
    </div>

    <div class="section">
      <h2>Processed vs Received Items</h2>
      <img id="plot_main" src="progress?cb={{ ts }}" alt="progress plot" width="900" />
      <small>Automatically refreshes</small>
    </div>

    <div class="section">
      <h2>Queue / Tree Size Over Time</h2>
      <img id="plot_queue" src="queue_tree_plot?cb={{ ts }}" alt="queue/tree plot" width="900" />
      <small>Automatically refreshes</small>
    </div>
  </div>

<script>
(function(){
  let refreshMs = Number({{ refresh }});
  let timer = null;

  const imgMain = document.getElementById("plot_main");
  const imgQueue = document.getElementById("plot_queue");
  const refreshInput = document.getElementById("refresh_ms");
  const applyBtn = document.getElementById("apply");
  const pauseBtn = document.getElementById("pause");

  const startInput = document.getElementById("start_time");
  const endInput = document.getElementById("end_time");
  const edgeInput = document.getElementById("include_edges");

  function buildParams() {
    const params = new URLSearchParams();
    params.set("cb", Date.now());

    const startVal = startInput.value;
    const endVal = endInput.value;
    const edgeVal = edgeInput.checked;

    if (startVal) params.set("start", Date.parse(startVal) / 1000);
    if (endVal)   params.set("end",   Date.parse(endVal) / 1000);
    if (edgeVal)   params.set("include_edges", "True");

    return "?" + params.toString();
  }

  function updateImages() {
    const q = buildParams();
    imgMain.src  = "progress" + q;
    imgQueue.src = "queue_tree_plot" + q;
  }

  function startTimer() {
    if (timer) clearInterval(timer);
    timer = setInterval(updateImages, refreshMs);
    pauseBtn.textContent = "Pause";
  }

  function stopTimer() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    pauseBtn.textContent = "Resume";
  }

  // Init refresh timer
  startTimer();

  applyBtn.addEventListener("click", function() {
    const val = Number(refreshInput.value) || 2000;
    refreshMs = Math.max(200, val);
    updateImages();
    startTimer();
  });

  pauseBtn.addEventListener("click", function() {
    if (timer) stopTimer();
    else startTimer();
  });

  document.addEventListener("visibilitychange", function() {
    if (!document.hidden) updateImages();
  });
})();
</script>
</body>
</html>
"""


@app.get("/view", response_class=HTMLResponse)
def view_page(request: Request):
    """Serve HTML frontend with JS auto-refresh."""
    refresh_param = request.query_params.get("refresh", "2000")
    try:
        refresh = max(1000, int(refresh_param))
    except ValueError:
        refresh = 2000

    html = VIEW_HTML.replace("{{ refresh }}", str(refresh)) \
        .replace("{{ ts }}", str(os.urandom(4).hex()))
    return HTMLResponse(html)


# =====================
# Startup / Scheduler
# =====================
async def on_startup() -> None:
    global current_history, history_snapshot_bytes, latest_timestamp

    # Load previous snapshot if present
    if SNAPSHOT_FILE.exists():
        try:
            data = SNAPSHOT_FILE.read_bytes()
            restored = pickle.loads(data)
            # Basic sanity check: we expect a HigherLevelSummary-like object
            current_history = restored
            history_snapshot_bytes = data
            latest_timestamp = restored.range[-1]
            # Initialize builder with restored tree (mutates the builder's internal tree)
            history_builder._tree = current_history
        except Exception:
            # If loading fails, ignore and start fresh (or log the error)
            current_history = None
            history_snapshot_bytes = None
            traceback.print_exc()

    # Start background worker
    asyncio.create_task(update_worker())

    # Start scheduler for forgetting job (example: nightly at 00:30 and 05:00)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_forgetting, "cron", hour=0, minute=30)
    scheduler.add_job(scheduled_forgetting, "cron", hour=5, minute=0)
    scheduler.start()
