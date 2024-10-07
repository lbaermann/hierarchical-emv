import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Optional, List, Tuple

import torch
from langchain_core.language_models import BaseChatModel
from sentence_transformers import SentenceTransformer

from em.em_tree import HigherLevelSummary
from lmp.api_visibility_wrapper import ApiVisibilityWrapper
from lmp.namespace import DynamicNamespaceDict
from lmp.repl.code_execution import ReplExecutionEnvironment
from lmp.setup import load_config, setup_lmp, instantiate_llm, instantiate_error_handlers
from .emv_api import EMVerbalizationAPI
from .simplified_agent.simple_coding_emv import SimplifiedCodingEMV
from .vlm import OpenAiVision
from .zs_flat_history_qa import ZeroShotOnePassSemiFlatQA


class _DatetimePackageNamespace:
    """
    This class is a little hack to enable both "datetime.datetime" and "datetime" to be valid in the namespace.

    This object itself is available via "datetime". The getattr method will either emulate the package when asking for
    any of the exported class names, or directly dispatch to the datetime class.
    Calling the object emulates the datetime constructor.
    """

    def __call__(self, *args, **kwargs):
        # This emulates the datetime constructor
        return datetime.datetime(*args, **kwargs)

    def __getattribute__(self, item):
        if item.startswith('__'):
            return super().__getattribute__(item)
        if item in datetime.__all__:
            # forwarding to package
            return getattr(datetime, item)
        else:
            # forwarding to class
            return getattr(datetime.datetime, item)


def setup_llm_emv(cfg_path='teach/simplified/full',
                  history: HigherLevelSummary = None,
                  now_time: datetime.datetime = None,
                  wait_for_trigger_callback=lambda: {'type': 'dialog', 'text': input('User:')},
                  tts=lambda s: print('System:', s)):
    if history is None:
        raise ValueError('history == None')
    full_cfg_path = Path(__file__).parent / 'config' / f'{cfg_path}.yaml'
    cfg = load_config(full_cfg_path, ((None, ('base', 'loop_prevention', 'suffix')),
                                      ('simplified_coding',
                                       ('system', 'usage', 'user_question', 'history', 'final_try'))))
    if cfg.get('type') == 'zs_one_pass':
        model = ZeroShotOnePassSemiFlatQA(instantiate_llm(cfg.pop('llm')), now_time=now_time, **cfg)
        return partial(model, history)

    vlm = _instantiate_vlm(cfg.pop('question_vlm', None))
    search_emb, filter_kwargs = create_search_embedding_and_cfg(cfg.pop('search', None))
    # noinspection PyTypeChecker
    api = EMVerbalizationAPI(wait_for_trigger=wait_for_trigger_callback, tts=tts, history=history,
                             now_time=now_time, hierarchy_level=cfg.pop('hierarchy_level', 'deep'),
                             vlm=vlm, search_embedding_fn=search_emb, search_filter_kwargs=filter_kwargs)
    api = ApiVisibilityWrapper(api, **cfg.pop('api'))
    namespace = setup_namespace(api)
    if vlm is None:
        cfg.setdefault('exclude_imports', []).append('vqa')

    if cfg.get('type') == 'simplified_coding':
        cfg.pop('type', None)
        cfg.pop('import_lmps', None)
        llm = instantiate_llm(cfg.pop('llm', {}))
        assert isinstance(llm, BaseChatModel)
        exec_env = ReplExecutionEnvironment(namespace)
        error_handlers = instantiate_error_handlers(cfg)
        return SimplifiedCodingEMV(llm, cfg.pop('prompt_cfg'), exec_env, error_handlers, **cfg)
    else:
        return setup_lmp(cfg, namespace)


def setup_namespace(api):
    namespace = DynamicNamespaceDict(api)
    namespace.predefined_globals['datetime'] = _DatetimePackageNamespace()
    namespace.predefined_globals['timedelta'] = datetime.timedelta
    namespace.predefined_globals['date'] = datetime.date
    namespace.predefined_globals['time'] = datetime.time
    return namespace


def _instantiate_vlm(vlm_cfg: Optional[dict]):
    if vlm_cfg is None:
        return None
    assert vlm_cfg.get('type') == 'ChatOpenAI'
    model = instantiate_llm(vlm_cfg)
    # noinspection PyTypeChecker
    return OpenAiVision(model)


def create_search_embedding_and_cfg(search_cfg: Optional[dict]):
    if search_cfg is None:
        return None, None

    embedding_model_name = search_cfg.pop('embedding', 'all-MiniLM-L6-v2')
    embedding_model = SentenceTransformer(embedding_model_name)
    cache = {}
    cache_file = Path('search-embedding-cache.pt')
    if cache_file.is_file():
        cache = torch.load(cache_file, map_location=embedding_model.device)
    write_cache_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='search-emb-cache-writer')

    def _embed_cached(texts: Tuple[str, ...]):
        result = torch.empty(len(texts), embedding_model.get_sentence_embedding_dimension(),
                             device=embedding_model.device)
        todo_texts, todo_indices = [], []
        for i, text in enumerate(texts):
            if text in cache:
                result[i] = cache[text]
            else:
                todo_texts.append(text)
                todo_indices.append(i)

        print('Embedding', len(texts), ', new:', len(todo_texts))
        if todo_indices:
            new_embeddings = embedding_model.encode(list(todo_texts), convert_to_tensor=True)
            result[todo_indices] = new_embeddings
            for text, emb in zip(todo_texts, new_embeddings):
                cache[text] = emb
            write_cache_executor.submit(lambda: torch.save(dict(cache), cache_file))
        return result

    def _embed(texts: List[str]):
        original_to_unique_indices = []
        unique_entries: List[str] = []
        for text in texts:
            try:
                idx = unique_entries.index(text)
                original_to_unique_indices.append(idx)
            except ValueError:
                original_to_unique_indices.append(len(unique_entries))
                unique_entries.append(text)
        embeddings = _embed_cached(tuple(unique_entries))
        return torch.index_select(embeddings, 0, torch.tensor(original_to_unique_indices))

    return _embed, search_cfg.pop('filter_kwargs', {})
