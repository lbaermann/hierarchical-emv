import ast
import json
import pickle
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from random import Random
from typing import Iterator, Dict, Any, Callable

from em.em_tree import HigherLevelSummary
from em.em_util import move_history_to_start_date
from llm_emv.eval.qa_eval import EpisodicQADataset, EpisodicQASample
from llm_emv.eval.util import pick_random_question_date_after_history, make_llm_summarizer_from_cfg


class Ego4dCustomQADataset(EpisodicQADataset):

    def __init__(self,
                 history_pickle_dir: Path,
                 qa_file: Path,
                 llm_summarizer: Callable[[list], HigherLevelSummary] = None,
                 pkl_suffix='first_person.objs.pkl',
                 ):
        super().__init__()
        self.llm_summarizer = llm_summarizer
        self.history_pkl_dir = history_pickle_dir
        self.pkl_suffix = pkl_suffix
        assert not pkl_suffix.startswith('.')
        self.qa_data = json.loads(qa_file.read_text())

    def __iter__(self) -> Iterator[EpisodicQASample]:
        for i, history_sample in enumerate(self.qa_data):
            video_ids = '-'.join(h['video_id'][:6] for h in history_sample['history'])
            history = self._get_history(history_sample['history'])
            for q, question_sample in enumerate(history_sample['questions']):
                q_id = f'{video_ids}-{i}-q{q}'
                yield EpisodicQASample(
                    sample_id=q_id,
                    question=question_sample['q'],
                    question_time=(datetime.strptime(question_sample['q_time'], '%Y-%m-%d %H:%M:%S')
                                   if 'q_time' in question_sample
                                   else pick_random_question_date_after_history(history, Random(q_id))),
                    answer=question_sample['a'],
                    history=history
                )

    def _get_history(self, history_spec: list):
        histories = []
        for spec in history_spec:
            pkl_file = self.history_pkl_dir / f'{spec["video_id"]}.history.{self.pkl_suffix}'
            start_time = datetime.strptime(spec['start_time'], '%Y-%m-%d %H:%M:%S')
            history = pickle.loads(pkl_file.read_bytes())
            history = move_history_to_start_date(history, start_time)
            histories.append(history)

        if self.llm_summarizer:
            return self.llm_summarizer([  # Let the LLM re-summarize the children of each history
                x for h in histories for x in h.children
            ])
        else:
            return HigherLevelSummary('', histories)

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        super().add_argparse_args(parser)
        parser.add_argument('--history-pickle-dir', type=Path, required=True)
        parser.add_argument('--qa-file', type=Path, required=True)
        parser.add_argument('--llm-summarizer-cfg', type=ast.literal_eval, default=None)
        parser.add_argument('--pkl-suffix', type=str, default='first_person.objs.pkl')

    @classmethod
    def _make_constructor_args_from_argparse_args(cls, args: Namespace) -> Dict[str, Any]:
        if args.llm_summarizer_cfg is not None:
            summarizer = make_llm_summarizer_from_cfg(args.llm_summarizer_cfg).recursively_summarize
        else:
            summarizer = None
        return {
            'history_pickle_dir': args.history_pickle_dir,
            'qa_file': args.qa_file,
            'llm_summarizer': summarizer,
            'pkl_suffix': args.pkl_suffix
        }
