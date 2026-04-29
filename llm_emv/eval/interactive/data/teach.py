import ast
import json
from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Iterable, Tuple, Callable, Union

from em.em_tree import iter_nodes_of_type, SceneGraphInstant, HigherLevelSummary
from em.llm_summary import LLMBasedSummarizer
from em.teach import load_teach_episode
from em.teach_incremental import TeachIncrementalHistoryBuilder, FlatTeachIncrementalHistoryBuilder
from lmp.setup import instantiate_llm
from .base import HistorySequenceQaDataset
from ...qa_eval import EpisodicQASample
from ...util import make_llm_summarizer_from_cfg


class TeachHistorySequenceDataset(HistorySequenceQaDataset):

    def __init__(self,
                 teach_base_dir: Path,
                 dataset_file: Path):
        super().__init__()
        self.game_dir = teach_base_dir / 'games'
        assert self.game_dir.is_dir(), str(self.game_dir)
        self.data = json.loads(dataset_file.read_text())['data']

    def __iter__(self) -> Iterable[Tuple[
        str,  # history id
        Iterable[Tuple[  # history iterator
            HigherLevelSummary,  # tree at this step (current time = history.range[-1])
            str  # name for log
        ]],
        Dict[datetime, List[EpisodicQASample]]  # qa samples
    ]]:
        for history_id, episodes in self.data.items():
            if history_id.startswith('#'):
                print('Skipping disabled sample', history_id)
                continue

            full_episodes, qa_samples = self._load_full_sample(history_id, episodes)

            yield history_id, self._iter_histories_from_episodes(
                history_id, full_episodes, qa_samples), qa_samples

    def _iter_histories_from_episodes(self, history_id: str,
                                      full_episodes: List[HigherLevelSummary],
                                      qa_samples: Dict[datetime, List[EpisodicQASample]]):
        raise NotImplementedError

    def _load_full_sample(self, history_id: str, episodes: list[dict]):
        full_episodes = []
        qa_samples: Dict[datetime, List[EpisodicQASample]] = {}
        for ep_idx, ep in enumerate(episodes):
            start_date = datetime.strptime(ep['start_date'], '%Y-%m-%d %H:%M:%S')
            assert len(full_episodes) == 0 or full_episodes[-1].range[-1] < start_date
            episode, ts_correction = load_teach_episode(self.game_dir / f'{ep["game_id"]}.game.json',
                                                        start_date,
                                                        return_initial_ts_correction=True)
            full_episodes.append(episode)
            for question_time, questions in self._iter_qa_samples_for_episode(ep, episode, ts_correction, start_date,
                                                                              id_prefix=f'{history_id}-{ep_idx}'):
                qa_samples.setdefault(question_time, []).extend(questions)

        return full_episodes, qa_samples

    @staticmethod
    def _iter_qa_samples_for_episode(ep_spec: dict, episode: HigherLevelSummary, ts_correction: float,
                                     start_date: datetime, id_prefix: str):
        all_timestamps_of_this_episode = [s.raw.timestamp for s in
                                          iter_nodes_of_type(episode, SceneGraphInstant)]
        for qa_time_key, qa_list in ep_spec['qa'].items():
            if qa_time_key.startswith('#'):
                continue
            question_time = start_date + timedelta(seconds=float(qa_time_key) - ts_correction)
            assert question_time in all_timestamps_of_this_episode, (
                f'{qa_time_key} not valid (ts correction {ts_correction}, '
                f'start date = {start_date}, q time = {question_time})')
            # noinspection PyTypeChecker
            yield question_time, [
                EpisodicQASample(
                    sample_id=f'{id_prefix}-{ep_spec["game_id"].replace("/", "-")}-{qa_time_key}-{i}',
                    question=q_data['question'],
                    answer=q_data['answer'],
                    question_time=(datetime.strptime(q_data['question_time'], '%Y-%m-%d %H:%M:%S')
                                   if 'question_time' in q_data else question_time),
                    history=None,
                    gt_answer_time_spans=[tuple(datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
                                                for x in q_data['reference'])],
                    meta={
                        'q_pair_id': q_data['pairid'],
                        'auto_correction': q_data['correction'],
                        'q_pair_idx': q_data['pair_idx']
                    }
                )
                for i, q_data in enumerate(qa_list)
            ]

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        super().add_argparse_args(parser)
        parser.add_argument('--dataset-file', type=Path,
                            help='Path to JSON dataset file like teach-interactive.json',
                            required=True)
        parser.add_argument('--teach-base-dir', type=Path, required=True)


class TeachHistorySequenceSceneIncrementalDataset(TeachHistorySequenceDataset):

    def __init__(self, teach_base_dir: Path, dataset_file: Path,
                 history_builder_fn: Callable[[str], TeachIncrementalHistoryBuilder]):
        super().__init__(teach_base_dir, dataset_file)
        self.history_builder_fn = history_builder_fn

    def _iter_histories_from_episodes(self, history_id: str,
                                      full_episodes: List[HigherLevelSummary],
                                      qa_samples: Dict[datetime, List[EpisodicQASample]]):
        history_builder = self.history_builder_fn(history_id)
        for ep in full_episodes:
            for scene in iter_nodes_of_type(ep, SceneGraphInstant):
                history = self._incremental_process_scene_with_tracking_and_error_logging(
                    history_id, history_builder, scene
                )

                yield history, str(scene)

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        super().add_argparse_args(parser)
        parser.add_argument('--history-builder-llm', type=ast.literal_eval, required=True)
        parser.add_argument('--history-builder-kwargs', type=ast.literal_eval, default={})

    @classmethod
    def _parse_additional_args(cls, args) -> dict:
        flat = args.history_builder_kwargs.pop('flat', False)
        apply_rules_for_summarization = args.history_builder_kwargs.pop('apply_rules_for_summarization', True)
        # noinspection PyTypeChecker
        return {
            **super()._parse_additional_args(args),
            'history_builder_fn': lambda history_id: (
                FlatTeachIncrementalHistoryBuilder()
                if flat else
                TeachIncrementalHistoryBuilder(
                    instantiate_llm(args.history_builder_llm),
                    relevance_language_rule_file_path=(args.output_dir / history_id / 'language-rules.json'
                                                       if apply_rules_for_summarization
                                                       else None),
                    **args.history_builder_kwargs
                ))
        }


class TeachHistorySequenceFullStateDataset(TeachHistorySequenceDataset):

    def __init__(self, teach_base_dir: Path, dataset_file: Path,
                 llm_summarizer: Union[LLMBasedSummarizer, dict] = None,
                 ):
        super().__init__(teach_base_dir, dataset_file)
        if isinstance(llm_summarizer, dict):
            llm_summarizer = make_llm_summarizer_from_cfg(llm_summarizer)
        self.llm_summarizer = llm_summarizer

    def _iter_histories_from_episodes(self, history_id: str,
                                      full_episodes: List[HigherLevelSummary],
                                      qa_samples: Dict[datetime, List[EpisodicQASample]]):
        group_qa_times_by_episode = [[] for _ in range(len(full_episodes))]
        for qa_time in qa_samples.keys():
            for i, ep in enumerate(full_episodes):
                if ep.range[0] <= qa_time <= ep.range[1]:
                    group_qa_times_by_episode[i].append(qa_time)
                    break

        for i, ep in enumerate(full_episodes):
            relevant_questions_times = group_qa_times_by_episode[i]
            if not relevant_questions_times:
                continue

            for q_time in relevant_questions_times:
                history = HigherLevelSummary('', full_episodes[:i + 1])  # include i
                history = deepcopy(history)  # To avoid forgetting/cutting to affect the original full_episodes
                self._cut_node_to_date_inplace(history, q_time)
                if self.llm_summarizer:
                    history = self._track_builder_time_and_costs(
                        lambda: self.llm_summarizer.recursively_summarize(history.children)
                    )
                yield history, f'{ep.nl_summary} @ {q_time}'

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        super().add_argparse_args(parser)
        parser.add_argument('--llm-summarizer', type=ast.literal_eval, default=None)
