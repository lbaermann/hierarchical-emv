import json
import pickle
from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path
from random import Random
from typing import Iterator, Dict, Any

from llm_emv.eval.qa_eval import EpisodicQADataset, EpisodicQASample
from llm_emv.eval.util import pick_random_question_date_after_history


class SimpleHistoryQADataset(EpisodicQADataset):
    """
    Reads histories from pickle files and loads QA from simple JSON.
    JSON format: [
        {
            "id": "...",
            "history": file name in pickled_histories_base_dir,
            "q": "...",
            "q_time": "2024-08-01 10:25:34", (optional)
            "a": "..." (optional)
        }
    ]
    """

    def __init__(self,
                 pickled_histories_base_dir: Path,
                 qa_file: Path):
        super().__init__()
        self.pickled_histories_base_dir = pickled_histories_base_dir
        self.qa_data = json.loads(qa_file.read_text())
        assert len(self.qa_data) == len(set(sample['id'] for sample in self.qa_data)), 'Check for duplicate keys'
        for sample in self.qa_data:
            assert (pickled_histories_base_dir / f'{sample["history"]}.pkl').exists(), sample['history']

    def __iter__(self) -> Iterator[EpisodicQASample]:
        for sample in self.qa_data:
            q_id = sample['id']
            question = sample['q']
            answer = sample.get('a', None)
            history_file = self.pickled_histories_base_dir / f'{sample["history"]}.pkl'
            history = pickle.loads(history_file.read_bytes())
            q_time = (datetime.strptime(sample['q_time'], '%Y-%m-%d %H:%M:%S')
                      if 'q_time' in sample else pick_random_question_date_after_history(history, Random(q_id)))
            if history.range[-1] > q_time:
                print('WARN: Question time', q_time, 'not after', history.range[-1], 'for sample', q_id)
            yield EpisodicQASample(q_id, question, q_time, answer, history)

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        super().add_argparse_args(parser)
        parser.add_argument('--history-dir', type=Path, required=True,
                            help='Directory containing files of pickled histories')
        parser.add_argument('--qa-file', type=Path, required=True)

    @classmethod
    def _make_constructor_args_from_argparse_args(cls, args: Namespace, **kwargs) -> Dict[str, Any]:
        return {
            'pickled_histories_base_dir': args.history_dir,
            'qa_file': args.qa_file,
            **kwargs
        }
