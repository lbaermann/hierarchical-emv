import pickle
import sys
from datetime import timedelta, datetime
from itertools import chain
from pathlib import Path
from typing import Union

from em.em_tree import HigherLevelSummary, GoalBasedSummary, EventBasedSummary
from em.em_util import LazyLoadPILImage

MAX_DISTANCE_TO_IMG = timedelta(seconds=0.5)


def _iter_scenes(history: Union[HigherLevelSummary, GoalBasedSummary, EventBasedSummary]):
    if isinstance(history, EventBasedSummary):
        yield from history.scenes
    elif isinstance(history, GoalBasedSummary):
        for e in history.events:
            yield from _iter_scenes(e)
    else:
        for c in history.children:
            yield from _iter_scenes(c)


def main():
    history_file = Path(sys.argv[1])
    img_dirs = [Path(x) for x in sys.argv[2:]]
    all_img_files = list(chain(*(
        d.rglob('0/image.rgb.png')
        for d in img_dirs
    )))
    print('Found', len(all_img_files), 'img files')

    all_files_with_date = [
        (datetime.fromtimestamp(int(p.parent.parent.name) / 1e6), p)
        for p in all_img_files
    ]
    all_files_with_date.sort()

    history = pickle.loads(history_file.read_bytes())
    linked_scenes = 0
    for scene in _iter_scenes(history):
        ts = scene.raw.timestamp
        nearest_img_idx = max((i for i, (d, p) in enumerate(all_files_with_date)
                               if d <= ts), default=None)
        if nearest_img_idx is not None:
            nearest_ts, img_p = all_files_with_date[nearest_img_idx]
            if ts - nearest_ts <= MAX_DISTANCE_TO_IMG:
                scene.raw.image = LazyLoadPILImage(img_p)
                linked_scenes += 1
    print('Linked', linked_scenes, 'to img files')

    history_file.write_bytes(pickle.dumps(history))


if __name__ == '__main__':
    main()
