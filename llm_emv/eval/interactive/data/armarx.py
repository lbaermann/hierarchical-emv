import ast
import json
import pickle
from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Tuple, Dict, List, Optional

from em.armarx_mem_incremental import ArmarXMemoryIncrementalTreeBuilder, FlatArmarXIncrementalTreeBuilder
from em.em_tree import HigherLevelSummary, iter_nodes_of_type, SceneGraphInstant
from em.em_util import move_history_to_start_date
from em.llm_summary import LLMBasedSummarizer
from .base import HistorySequenceQaDataset
from ...qa_eval import EpisodicQASample

_QaSamples = Dict[datetime, List[EpisodicQASample]]


class ArmarXHistorySeqDataset(HistorySequenceQaDataset):
    def __init__(self,
                 qa_file: Path,
                 pkl_base_dir: Path,
                 output_dir: Path,
                 online_builder_args: Optional[Dict] = None,
                 offline_summarizer_args: Optional[Dict] = None,
                 ):
        super().__init__()
        self.output_dir = output_dir
        self.pkl_base_dir = pkl_base_dir
        self.qa_data = json.loads(qa_file.read_text())
        assert online_builder_args is not None or offline_summarizer_args is not None and not (
                offline_summarizer_args and online_builder_args)
        self.online_builder_args = online_builder_args
        self.offline_summarizer_args = offline_summarizer_args

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        super().add_argparse_args(parser)
        parser.add_argument('--qa-file', type=Path, required=True)
        parser.add_argument('--pkl-base-dir', type=Path, required=True)
        # output dir is assumed to be a global argparse args, will just be injected here
        parser.add_argument('--online-builder-args', type=ast.literal_eval, default=None)
        parser.add_argument('--offline-summarizer-args', type=ast.literal_eval, default=None)

    def __iter__(self) -> Iterable[Tuple[
        str,  # history id
        Iterable[Tuple[  # history iterator
            HigherLevelSummary,  # tree at this step (current time = history.range[-1])
            str  # name for log
        ]],
        _QaSamples
    ]]:
        for name, history_spec in self.qa_data['data'].items():
            full_episodes, qa_samples = self._load_full_sample(name, history_spec)
            yield name, self._iter_histories_from_episodes(
                name, full_episodes, qa_samples), qa_samples

    def _load_full_sample(self, name: str, history_spec: List[Dict]) -> Tuple[List[HigherLevelSummary], _QaSamples]:
        full_episodes = []
        qa: _QaSamples = {}
        for ep_idx, ep in enumerate(history_spec):
            start_date = datetime.strptime(ep['start_date'], '%Y-%m-%d %H:%M:%S')
            assert len(full_episodes) == 0 or full_episodes[-1].range[-1] < start_date
            episode = pickle.loads((self.pkl_base_dir / ep["episode"]).read_bytes())
            episode = move_history_to_start_date(episode, start_date)
            full_episodes.append(episode)
            scenes = list(iter_nodes_of_type(episode, SceneGraphInstant))

            for q_time_str, question_defs in ep['qa'].items():
                questions = []
                q_time_raw = start_date + timedelta(seconds=float(q_time_str))
                scene_before = [s for s in scenes if s.raw.timestamp <= q_time_raw][-1]
                q_time_clamped = scene_before.raw.timestamp
                for q_idx, question_sample in enumerate(question_defs):
                    # noinspection PyTypeChecker
                    questions.append(EpisodicQASample(
                        sample_id=f'{name}-{ep_idx}-{q_time_str}-{q_idx}',
                        question=question_sample['question'],
                        answer=question_sample['answer'],
                        history=None,
                        question_time=q_time_raw,
                        gt_answer_time_spans=[tuple(datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
                                                    for x in question_sample['reference'])],
                        meta={
                            'q_pair_id': question_sample['pairid'],
                            'auto_correction': question_sample['correction'],
                            'q_pair_idx': question_sample['pair_idx']
                        }
                    ))
                qa.setdefault(q_time_clamped, []).extend(questions)

        return full_episodes, qa

    def _iter_histories_from_episodes(self, name: str, full_episodes: List[HigherLevelSummary], qa_samples: _QaSamples):
        if self.online_builder_args:
            yield from self._iter_histories_online(name, full_episodes)
        elif self.offline_summarizer_args:
            yield from self._iter_histories_offline(full_episodes, qa_samples)
        else:
            assert False

    def _iter_histories_online(self, history_id: str, full_episodes: List[HigherLevelSummary]):
        args = self._copy_and_instantiate_llm_args(self.online_builder_args)
        history_builder = FlatArmarXIncrementalTreeBuilder() if args.get('flat', False) \
            else ArmarXMemoryIncrementalTreeBuilder(
            relevance_language_rule_file_path=self.output_dir / history_id / 'language-rules.json',
            **args
        )
        all_scenes = (s for e in full_episodes for s in iter_nodes_of_type(e, SceneGraphInstant))
        for scene in all_scenes:
            history = self._incremental_process_scene_with_tracking_and_error_logging(
                history_id, history_builder, scene
            )
            yield history, str(scene)

    def _iter_histories_offline(self, full_episodes: List[HigherLevelSummary], qa_samples: _QaSamples):
        args = self._copy_and_instantiate_llm_args(self.offline_summarizer_args)
        llm_summarizer = LLMBasedSummarizer(**args)
        for qa_time in sorted(qa_samples.keys()):
            relevant_episodes = [e for e in full_episodes
                                 if e.range[0] < qa_time]
            tmp_history = HigherLevelSummary('', relevant_episodes)
            tmp_history = deepcopy(tmp_history)
            self._cut_node_to_date_inplace(tmp_history, qa_time)
            history = self._track_builder_time_and_costs(
                lambda: llm_summarizer.recursively_summarize(tmp_history.children)
            )
            yield history, f'{qa_time}'
