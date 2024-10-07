import ast
import pickle
from abc import ABC
from argparse import Namespace
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from functools import cache, cached_property
from hashlib import md5
from pathlib import Path
from random import Random
from typing import Iterator, Dict, List, Any, Tuple, Iterable, Optional, Union

from em.em_tree import HigherLevelSummary
from em.em_util import move_history_to_start_date
from em.llm_summary import LLMBasedSummarizer
from em.randomize_episodes import gen_random_date_from_seed, randomize_datetimes
from em.teach import load_teach_episode, load_teach_episode_no_gt
from .qa_eval import EpisodicQADataset, EpisodicQASample
from .util import make_llm_summarizer_from_cfg, pick_random_question_date_after_history


class DeChantQaDataset(EpisodicQADataset, ABC):

    def __init__(self, qa_file: Path,
                 samples_per_episode: int = None,
                 filter_by_question_types: Tuple[str] = None,
                 skip_first_n_episodes=0
                 ):
        super().__init__()
        self._skip_first_n_episodes = skip_first_n_episodes
        self._loaded_qa_data = pickle.loads(qa_file.read_bytes())
        self._samples_per_episode = samples_per_episode
        self._filter_by_question_types = filter_by_question_types

    @cached_property
    def _qa_data(self):
        return self._read_qa_data(self._loaded_qa_data)

    def _read_qa_data(self, loaded_data: Any) -> OrderedDict[
        Tuple[str, ...],  # Teach Trial IDs (might be multiple ones for combined episodes)
        List[  # there might be multiple batches of questions
            Dict[
                str,  # keys, some are in cls._non_question_keys(), the rest is treated as question
                Any  # value for this key. if it's a question key, assuming dict(text_input: str, target_output: str)
            ]
        ]
    ]:
        raise NotImplementedError

    def _parse_datetime_from_trial_id(self, trial_id: Tuple[str, ...]) -> datetime:
        raise NotImplementedError

    def _load_history(self, batch: Dict[str, Any], start_time: datetime) -> Optional[HigherLevelSummary]:
        raise NotImplementedError

    @classmethod
    def _non_question_keys(cls) -> Iterable[str]:
        raise NotImplementedError

    def __iter__(self) -> Iterator[EpisodicQASample]:
        for i, trial_ids in enumerate(self._qa_data.keys()):
            if i < self._skip_first_n_episodes:
                continue

            start_time = self._parse_datetime_from_trial_id(trial_ids)

            for i, sample in enumerate(self._iter_single_trial(start_time, trial_ids)):
                if i == self._samples_per_episode:
                    break
                yield sample

    def _iter_single_trial(self, start_time, trial_ids):
        for b, batch in enumerate(self._qa_data[trial_ids]):
            if (self._filter_by_question_types is not None
                    and all(key not in self._filter_by_question_types for key in batch.keys())):
                # Prevent loading history if it is not usable with the current filter
                continue

            history = self._load_history(batch, start_time)
            if history is None:
                continue

            for key, value in batch.items():
                if key in self._non_question_keys():
                    continue
                if self._filter_by_question_types is not None and key not in self._filter_by_question_types:
                    continue
                assert (isinstance(value, dict)
                        and 'text_input' in value
                        and 'target_output' in value), f'key={key}, value={value}'
                q, a = value['text_input'], value['target_output']
                sample_id = f'{"-".join(trial_ids)}-{b}-{key}'
                if 'now_time_stamp' in batch:
                    q_time = batch['now_time_stamp']
                else:
                    q_time = pick_random_question_date_after_history(history, Random(sample_id))
                yield EpisodicQASample(sample_id, q, q_time, a, deepcopy(history))

    @cache
    def __len__(self):
        n = 0
        for t in self._qa_data.keys():
            for b in self._qa_data[t]:
                for k, v in b.items():
                    if k in self._non_question_keys():
                        continue
                    n += 1
        return n

    @classmethod
    def add_argparse_args(cls, parser):
        parser.add_argument('--qa-file', type=Path, required=True)
        parser.add_argument('--max-samples-per-episode', type=int, default=None)
        parser.add_argument('--use-only-question-types', nargs='+', default=None)
        parser.add_argument('--skip-first-n-episodes', type=int, default=0)

    @classmethod
    def _make_constructor_args_from_argparse_args(cls, args: Namespace) -> Dict[str, Any]:
        return dict(qa_file=args.qa_file,
                    samples_per_episode=args.max_samples_per_episode,
                    filter_by_question_types=args.use_only_question_types,
                    skip_first_n_episodes=args.skip_first_n_episodes)


class TeachDeChantDataset(DeChantQaDataset):

    def __init__(self, teach_base_path: Path,
                 qa_file: Path,
                 llm_summarizer: LLMBasedSummarizer = None,
                 pure_img_approach_args: dict = None,
                 **kwargs):
        super().__init__(qa_file, **kwargs)
        assert teach_base_path.is_dir()
        assert (teach_base_path / 'games').is_dir() and (teach_base_path / 'images').is_dir()
        self.teach_base_path = teach_base_path
        self.llm_summarizer = llm_summarizer
        self.pure_img_approach_args = pure_img_approach_args
        if pure_img_approach_args:
            assert pure_img_approach_args['obj_det_dir']
            assert pure_img_approach_args['action_inference_dir']

    def _read_qa_data(self, loaded_data: Any) -> OrderedDict[str, List[Dict[str, Any]]]:
        # For single-episode teach generated QA, loaded_data is List[Dict[str, Any]]
        # Multi-episode data is also List[Dict[str, Any]], but with different keys.
        if len(loaded_data) == 0:
            return OrderedDict()

        if 'episode_ids' in loaded_data[0]:  # multi-episode case
            sample_to_id = lambda sample: tuple(sample['episode_ids'])
        else:  # single-episode case
            sample_to_id = lambda sample: (sample['game_id'],)

        result = OrderedDict()
        for sample in loaded_data:
            key = sample_to_id(sample)
            result.setdefault(key, []).append(sample)
        return result

    def _parse_datetime_from_trial_id(self, trial_ids: Tuple[str, ...]) -> datetime:
        # This will be ignored in the multi-episode case when there are predefined dates and times in the data dict
        return gen_random_date_from_seed("-".join(trial_ids))  # Seed with game id to ensure deterministic behavior

    def _load_history(self, batch: Dict[str, Any], start_time: datetime) -> Optional[HigherLevelSummary]:
        split = batch['dataset_name']
        single_episode = 'game_id' in batch
        cached_history, cache_file = self._get_cached_history(
            split, batch['game_id'] if single_episode else batch['episode_ids'])

        if cached_history:
            if single_episode and start_time is not None:
                cached_history = move_history_to_start_date(cached_history, start_time)
            return cached_history

        if single_episode:
            game_id = batch["game_id"]
            game_file = self.teach_base_path / 'games' / split / f'{game_id}.game.json'
            if self.pure_img_approach_args:
                args_copy = dict(self.pure_img_approach_args)
                raw_history = load_teach_episode_no_gt(
                    teach_trial_image_dir=self.teach_base_path / 'images' / split / game_id,
                    obj_det_dir=args_copy.pop('obj_det_dir') / game_id,
                    action_inference_dir=args_copy.pop('action_inference_dir') / game_id,
                    start_time=start_time,
                    **args_copy
                )
            else:
                raw_history = load_teach_episode(game_file, start_time)
        else:
            episode_ids = batch["episode_ids"]
            time_info = batch.get('time_stamps', [])
            time_info = {
                ep_id: ts for ep_id, ts in zip(episode_ids, time_info)
            }
            single_ep_histories = [
                self._load_history(dict(dataset_name=split, game_id=ep_id), time_info.get(ep_id))
                for ep_id in episode_ids
            ]
            if not time_info:
                # Seed deterministically based on start time, which itself is seeded based on the episode ids
                single_ep_histories = randomize_datetimes(single_ep_histories, rng=Random(str(start_time)))
            raw_history = HigherLevelSummary('', single_ep_histories)

        if self.llm_summarizer is None:
            return raw_history

        hierarchical_history = self.llm_summarizer.recursively_summarize(raw_history.children)
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_bytes(pickle.dumps(hierarchical_history))
        return hierarchical_history

    def _get_cached_history(self, split: str, history_id: Union[str, Tuple[str, ...]]
                            ) -> Tuple[Optional[HigherLevelSummary], Path]:
        single_episode = isinstance(history_id, str)
        if self.pure_img_approach_args:
            use_speech = self.pure_img_approach_args.get("use_speech", True)
            split = f'img-only-{"with" if use_speech else "no"}-speech-{split}'
        if single_episode:
            game_id: str = history_id
            preprocessed_history_file = self.teach_base_path / 'preprocessed_histories' / split / f'{game_id}.pkl'
        else:
            episode_ids: Tuple[str, ...] = history_id
            # Don't want to run into "too long file name" errors, but still want unique file names
            if len(episode_ids) >= 100:
                md5()
                quarter_size = len(episode_ids) // 4 + 1
                episode_id_str = ''.join(md5(''.join(episode_ids[i * quarter_size:(i + 1) * quarter_size]
                                                     ).encode()).hexdigest()
                                         for i in range(4))
            elif len(episode_ids) >= 50:
                episode_id_str = (''.join(x[:3] for x in episode_ids)
                                  + '-' + md5(''.join(episode_ids).encode()).hexdigest())
            else:
                episode_id_str = '-'.join(x[:6] for x in episode_ids)
            preprocessed_history_file = (self.teach_base_path / 'preprocessed_histories'
                                         / f'{split}-multi' / f'{episode_id_str}.pkl')

        if preprocessed_history_file.is_file():
            return pickle.loads(preprocessed_history_file.read_bytes()), preprocessed_history_file
        else:
            return None, preprocessed_history_file

    @classmethod
    def _non_question_keys(cls) -> Iterable[str]:
        return ('dataset_name', 'game_id', 'image_names', 'episode_id',
                'episode_ids', 'images_lengths', 'dialogues', 'time_stamps', 'time_stamp_strings',
                'now_time_stamp', 'source_file_names_dict')

    @classmethod
    def add_argparse_args(cls, parser):
        super().add_argparse_args(parser)
        parser.add_argument('--teach-base', type=Path, required=True)
        parser.add_argument('--llm-summarizer-cfg', type=ast.literal_eval, default=None)
        parser.add_argument('--pure-img-approach', type=ast.literal_eval, default=None)

    @classmethod
    def _make_constructor_args_from_argparse_args(cls, args, **kwargs) -> Dict[str, Any]:
        summarizer = kwargs.pop('llm_summarizer', None)
        if summarizer is None and args.llm_summarizer_cfg is not None:
            summarizer = make_llm_summarizer_from_cfg(args.llm_summarizer_cfg)
        return {'teach_base_path': args.teach_base,
                'llm_summarizer': summarizer,
                'pure_img_approach_args':
                    {k: Path(v) if isinstance(v, str) else v
                     for k, v in args.pure_img_approach.items()}
                    if args.pure_img_approach else None,
                **super()._make_constructor_args_from_argparse_args(args),
                **kwargs}
