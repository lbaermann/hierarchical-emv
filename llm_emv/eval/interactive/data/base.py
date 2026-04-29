import inspect
import pickle
import time
from abc import ABC
from argparse import ArgumentParser
from datetime import datetime
from itertools import islice
from pathlib import Path
from typing import Iterable, Tuple, Dict, List, final, Any

from em.em_tree import HigherLevelSummary, AnyTreeNode, SceneGraphInstant, type_to_children_property_map
from em.incremental_history import IncrementalHistoryBuilder
from lmp.setup import instantiate_llm
from lmp.token_callback import get_token_tracking_callback
from ...qa_eval import EpisodicQASample


class HistorySequenceQaDataset(ABC):

    def __init__(self):
        super().__init__()
        self.total_time_builder = 0
        self.builder_prompt_tokens = 0
        self.builder_completion_tokens = 0
        self.__prev_state_dump = {}

    def __iter__(self) -> Iterable[Tuple[
        str,  # history id
        Iterable[Tuple[  # history iterator
            HigherLevelSummary,  # tree at this step (current time = history.range[-1])
            str  # name for log
        ]],
        Dict[datetime, List[EpisodicQASample]]  # qa samples
    ]]:
        raise NotImplementedError

    @property
    @final
    def builder_token_costs(self):
        return {
            'prompt_tokens': self.builder_prompt_tokens,
            'completion_tokens': self.builder_completion_tokens,
        }

    @final
    def _incremental_process_scene_with_tracking_and_error_logging(self,
                                                                   history_id: str,
                                                                   history_builder: IncrementalHistoryBuilder,
                                                                   scene: SceneGraphInstant) -> HigherLevelSummary:
        try:
            result = self._track_builder_time_and_costs(
                lambda: history_builder.process(scene)
            )
            self.__prev_state_dump[history_id] = pickle.dumps(result)
            return result
        except:
            print('Failed to update history with scene', scene)
            f_name = f'failure-state-{time.time()}.pkl'
            Path(f_name).write_bytes(pickle.dumps({
                'prev_state': self.__prev_state_dump.get(history_id, None),
                'scene': scene,
                'history_builder_type': str(type(history_builder)),
            }))
            print('Wrote failure state to', f_name)
            raise

    @final
    def _track_builder_time_and_costs(self, fn):
        with get_token_tracking_callback() as cb:
            t = time.time()
            result = fn()
            self.total_time_builder += (time.time() - t)
            self.builder_prompt_tokens += cb.prompt_tokens
            self.builder_completion_tokens += cb.completion_tokens
            return result

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        pass

    @classmethod
    def _parse_additional_args(cls, args) -> dict:
        return {}

    @classmethod
    @final
    def from_argparse_args(cls, args):
        sig = inspect.signature(cls)
        matched_args = {}
        for key, param in sig.parameters.items():
            if hasattr(args, key):
                value = getattr(args, key)
                if param.annotation and param.annotation != param.empty:
                    assert isinstance(value, param.annotation), (f'Expected {param.annotation}, but got {type(value)} '
                                                                 f'for parameter {key} of {cls.__name__}')
                matched_args[key] = value

        matched_args.update(cls._parse_additional_args(args))

        # noinspection PyArgumentList
        return cls(**matched_args)

    @staticmethod
    def _copy_and_instantiate_llm_args(args):
        args: Dict[str, Any] = dict(args)
        for k, v in args.items():
            if k.endswith('llm'):
                args[k] = instantiate_llm(v)
        return args

    @staticmethod
    def _cut_node_to_date_inplace(node: AnyTreeNode, cutoff: datetime):
        if isinstance(node, SceneGraphInstant):
            return node.raw.timestamp > cutoff
        children = getattr(node, type_to_children_property_map[type(node)])
        for c in list(children):
            if HistorySequenceQaDataset._cut_node_to_date_inplace(c, cutoff):
                children.remove(c)
        return len(children) == 0  # Remove from parent if all gone


class OnlyFirstNSamplesDataset(HistorySequenceQaDataset):
    def __init__(self, wrapped: HistorySequenceQaDataset, n: int):
        super().__init__()
        self._n = n
        self._wrapped = wrapped

    def __iter__(self) -> Iterable[Tuple[
        str,  # history id
        Iterable[Tuple[  # history iterator
            HigherLevelSummary,  # tree at this step (current time = history.range[-1])
            str  # name for log
        ]],
        Dict[datetime, List[EpisodicQASample]]  # qa samples
    ]]:
        # noinspection PyTypeChecker
        yield from islice(self._wrapped, self._n)

    def __getattribute__(self, item):
        if item.startswith('_'):
            return super().__getattribute__(item)
        else:
            return getattr(self._wrapped, item)
