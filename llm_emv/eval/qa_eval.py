import traceback
from abc import ABC
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator, Callable, Dict, Iterable, List, Any, final

from em.em_tree import HigherLevelSummary as History


@dataclass
class EpisodicQASample:
    sample_id: str
    question: str
    question_time: datetime  # What "now" means in the question
    answer: str
    history: History


@dataclass
class EpisodicQAModelOutput(EpisodicQASample):
    hypothesis: str


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
        results.append(EpisodicQAModelOutput(hypothesis=hypothesis, **sample.__dict__))
    return results
