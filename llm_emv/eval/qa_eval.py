import json
import traceback
from abc import ABC
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterator, Callable, Dict, Iterable, List, Any, final, Tuple

from em.em_tree import HigherLevelSummary as History
from .util import determine_git_commit


@dataclass
class EpisodicQASample:
    sample_id: str
    question: str
    question_time: datetime  # What "now" means in the question
    answer: str
    history: History

    gt_answer_time_spans: List[Tuple[datetime, datetime]] = field(default_factory=lambda: [], kw_only=True)
    meta: Dict = field(default_factory=lambda: {}, kw_only=True)


@dataclass
class EpisodicQAModelOutput(EpisodicQASample):
    hypothesis: str

    @classmethod
    def from_sample(cls, sample: EpisodicQASample, hypothesis: str):
        return cls(hypothesis=hypothesis, **sample.__dict__)


class EpisodicQADataset(ABC):

    def __iter__(self) -> Iterator[EpisodicQASample]:
        raise NotImplementedError

    @classmethod
    def add_argparse_args(cls, parser: ArgumentParser):
        pass

    @classmethod
    @final
    def from_argparse_args(cls, args: Namespace, **kwargs):
        # noinspection PyArgumentList
        return cls(**cls._make_constructor_args_from_argparse_args(args, **kwargs))

    @classmethod
    def _make_constructor_args_from_argparse_args(cls, args: Namespace) -> Dict[str, Any]:
        raise NotImplementedError


def run_evaluation(model: Callable[[str, datetime, History], str],
                   dataset: Iterable[EpisodicQASample]) -> List[EpisodicQAModelOutput]:
    results = []
    for sample in dataset:
        print('Evaluating sample', sample.sample_id)
        try:
            hypothesis = model(sample.question, sample.question_time, sample.history)
        except KeyboardInterrupt:
            break
        except Exception as e:
            traceback.print_exc()
            hypothesis = '###ERROR### ' + str(e)
        results.append(EpisodicQAModelOutput.from_sample(sample, hypothesis))
    return results


def write_results(results: List[EpisodicQAModelOutput], args: Namespace,
                  out_file: Path, **additional_data):
    out_file.write_text(json.dumps({
        'config': {k: str(v) for k, v in args.__dict__.items()},
        'code_commit': determine_git_commit(),
        'results': {
            r.sample_id: {
                'q_time': r.question_time.strftime('%Y/%m/%d %H:%M:%S'),
                'q': r.question,
                'gt': r.answer,
                'hyp': r.hypothesis,
                **({'ref_ts': [[t.strftime('%Y/%m/%d %H:%M:%S') for t in span]
                               for span in r.gt_answer_time_spans]}
                   if r.gt_answer_time_spans else {}),
                **({'meta': r.meta} if r.meta else {})
            }
            for r in results
        },
        **additional_data
    }, indent=2))
