from enum import Enum
from typing import List

_label_to_broad_label = {
    'correct': 'correct',
    'correct_summarized': 'correct',
    'correct_tmi': 'correct',
    'partially_correct_tmi': 'partially_correct',
    'partially_correct_missing': 'partially_correct',
    'wrong': 'wrong',
    'no_answer': 'wrong',
}


class _EnumUtilBase:
    @property
    def index(self):
        # noinspection PyTypeChecker
        return list(self.__class__).index(self)

    @classmethod
    def all_names(cls):
        # noinspection PyTypeChecker
        return [v.name for v in cls]


class FineEmvOutputCategory(_EnumUtilBase, Enum):
    correct = 'correct'
    correct_summarized = 'correct_summarized'
    correct_tmi = 'correct_tmi'

    partially_correct_tmi = 'partially_correct_tmi'
    partially_correct_missing = 'partially_correct_missing'

    wrong = 'wrong'
    no_answer = 'no_answer'

    @property
    def broad(self) -> 'BroadEmvOutputCategory':
        return BroadEmvOutputCategory(_label_to_broad_label[self.name])


class BroadEmvOutputCategory(_EnumUtilBase, Enum):
    correct = 'correct'
    partially_correct = 'partially_correct'
    wrong = 'wrong'

    @property
    def fine(self) -> List[FineEmvOutputCategory]:
        return [FineEmvOutputCategory(fine)
                for fine, broad in _label_to_broad_label.items()
                if broad == self.name]

