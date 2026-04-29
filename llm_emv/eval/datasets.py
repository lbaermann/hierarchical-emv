from argparse import ArgumentParser
from itertools import islice
from typing import List

from .ego4d_custom_qa import Ego4dCustomQADataset
from .qa_eval import EpisodicQADataset
from .simple_qa_data import SimpleHistoryQADataset
from .dechant_qa_dataset import TeachDeChantDataset

_dataset_classes = {
    'teach-dechant': TeachDeChantDataset,
    'ego4d-custom': Ego4dCustomQADataset,
    'simple': SimpleHistoryQADataset,
}
assert all(issubclass(x, EpisodicQADataset) for x in _dataset_classes.values())


def add_dataset_args_and_parse(parser: ArgumentParser, arg_list: List[str] = None, ignore_unknown=False):
    parser.add_argument('--dataset', type=str, choices=_dataset_classes.keys(), default='simple')
    parser.add_argument('--n-samples', type=int, default=None,
                        help='Use only the first n samples from the dataset')

    args, _ = parser.parse_known_args(arg_list)
    dataset_cls = _dataset_classes[args.dataset]
    dataset_cls.add_argparse_args(parser)
    if ignore_unknown:
        args, _ = parser.parse_known_args(arg_list)
    else:
        args = parser.parse_args(arg_list)

    dataset = dataset_cls.from_argparse_args(args)
    if args.n_samples:
        dataset = islice(dataset, args.n_samples)

    return args, dataset
