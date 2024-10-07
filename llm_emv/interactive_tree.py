from datetime import datetime, date
from functools import cached_property
from itertools import chain
from typing import Any, Callable, List, Tuple

import torch

from lmp.repl.semantic_hint_errror import SemanticHintError

PRETTY_PRINT = False
USE_DASH_IN_SIMPLIFIED_REPR = False
INDENT_SIZE = 2


def _overlaps_date(query: date, date_range: Tuple[datetime, datetime]):
    start, end = date_range
    return start.date() <= query <= end.date()


def _overlaps_datetime(query: datetime, date_range: Tuple[datetime, datetime]):
    # Replace some value since a query for "5:52" (without second precision)
    # should match an event that starts at "5:52:42"

    start_replace = dict(microsecond=0)
    end_replace = dict(microsecond=0)

    # Simplification: assuming value == 0 means no information given.
    #  Better would be to patch datetime class to record what precision was provided at construction time
    if query.second == 0:
        start_replace['second'] = 0
        end_replace['second'] = 59
        if query.minute == 0:
            start_replace['minute'] = 0
            end_replace['minute'] = 59

    start, end = date_range
    return start.replace(**start_replace) <= query <= end.replace(**end_replace)


def _overlaps_date_range(query_start: date, query_end: date, date_range: Tuple[datetime, datetime]):
    start, end = date_range
    return query_start <= start.date() <= query_end or query_start <= end.date() <= query_end


def _overlaps_datetime_range(query_start: datetime, query_end: datetime, date_range: Tuple[datetime, datetime]):
    start, end = date_range
    return query_start <= start <= query_end or query_start <= end <= query_end


def create_index_only_filter_fn(length, args):
    if len(args) == 1:
        a = args[0]
        if isinstance(a, int):
            if a < 0:
                a = length - a
            return lambda c, i: i == a
        elif isinstance(a, range):
            return lambda c, i: i in a
        else:
            raise NotImplementedError
    elif len(args) == 2:
        # TODO
        raise NotImplementedError
    return lambda c, i: True


def create_expandable_tree_node_filter_fn(length, args):
    if len(args) == 0:
        return lambda c, i: True
    elif len(args) == 1:
        a = args[0]
        if isinstance(a, datetime):
            return lambda c, i: _overlaps_datetime(a, c.range)
        elif isinstance(a, date):
            return lambda c, i: _overlaps_date(a, c.range)
        elif isinstance(a, int):
            if a < 0:
                a = length - a
            return lambda c, i: i == a
        else:
            raise TypeError('expand function cannot handle', type(a))
    elif len(args) == 2:
        a, b = args
        if type(a) is not type(b):
            raise TypeError('Both arguments to expand must be of the same type. Got:', type(a), '!=', type(b))
        elif isinstance(a, int):
            if a < 0:
                a = length - a
            if b < 0:
                b = length - b
            return lambda c, i: i in range(a, b)
        elif isinstance(a, datetime):
            return lambda c, i: _overlaps_datetime_range(a, b, c.range)
        elif isinstance(a, date):
            return lambda c, i: _overlaps_date_range(a, b, c.range)
        else:
            raise TypeError('expand function cannot handle', type(a))
    else:
        raise NotImplementedError


def format_datetime_range(start: datetime, end: datetime):
    if (end - start).days > 0:
        # Date-only formatting
        start_str = end_str = '%Y/%m/%d'
    else:
        if (end - start).total_seconds() / 60 > 3:
            # More than 3 minutes => neglect seconds
            start_str = '%Y/%m/%d %H:%M'
            end_str = '%H:%M'
        else:
            start_str = '%Y/%m/%d %H:%M:%S'
            end_str = '%H:%M:%S'
        if end.day != start.day:
            end_str = '%Y/%m/%d ' + end_str
    return start.strftime(start_str) + ' - ' + end.strftime(end_str)


def indent_following_lines(s: str, num_spaces: int):
    return s.replace('\n', '\n' + ' ' * num_spaces)


class ExpandableList:
    def __init__(self,
                 children: List[Any],

                 # Generates a filter function. Receives:
                 #  - int length: total number of children, for handling negative indices
                 #  - ... *args: The arguments based on which to filter.
                 # Returns: A filter function with signature (item, index) -> include?
                 filter_fn_generator: Callable[[int, ...], Callable[[Any, int], bool]],

                 # Receives (query, all children, **kwargs), returns indices of search results
                 search_filter_fn: Callable[[str, List[Any], ...], List[int]]
                 ) -> None:
        super().__init__()
        self.children = children
        self._children_states = [False] * len(self.children)
        self._filter_fn_generator = filter_fn_generator
        self._search_filter_fn = search_filter_fn
        self._simplified_repr = False

    def expand(self, *args):
        self._set_expanded(True, *args)
        return self

    def collapse(self, *args):
        self._set_expanded(False, *args)

    def collapse_all_but(self, *args):
        self.collapse()
        self.expand(*args)

    def collapse_deep(self):
        self._set_expanded(False, recursive=True)

    def search(self, query, **kwargs):
        self.collapse()
        indices = self._search_filter_fn(query, list(self.children), **kwargs)
        if len(indices) == 0:
            if kwargs.get('close_match', False):
                return 'No close matches found.'
            else:
                self.expand()
                raise SemanticHintError(
                    'No children matching search query. Expanded all nodes so you can check manually.',
                    critical=False)
        for i in indices:
            self._children_states[i] = True
        return self

    def _set_expanded(self, state, *args, recursive=False):
        filter_fn = self._filter_fn_generator(len(self.children), args)
        for i, c in enumerate(self.children):
            if filter_fn(c, i):
                self._children_states[i] = state
                if recursive and isinstance(c, ExpandableList):
                    c._set_expanded(state, *args, recursive=True)

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, item):
        if item >= len(self.children):
            raise IndexError(f'Index {item} out of range (length {len(self.children)})')
        return self.children[item]

    def __repr__(self):
        if len(self.children) == 0:
            return '[]'

        pretty = PRETTY_PRINT or self._simplified_repr
        pretty_not_simplified = PRETTY_PRINT and not self._simplified_repr
        dash = '- ' * self._simplified_repr * USE_DASH_IN_SIMPLIFIED_REPR
        any_expanded = any(s for s in self._children_states)
        if any_expanded:
            prev_expanded = True
            children_str = ''
            for i, (c, s) in enumerate(zip(self.children, self._children_states)):
                start = ('' if i == 0 or self._simplified_repr else ', ') + (
                        ('\n' + ' ' * INDENT_SIZE * pretty_not_simplified) * pretty)
                if s:
                    children_str += start + dash + f'{i}: ' + indent_following_lines(
                        repr(c), num_spaces=INDENT_SIZE * pretty_not_simplified)
                elif prev_expanded:
                    children_str += start + dash + '...'
                prev_expanded = s
        else:
            children_str = dash + '...'

        return (
                '[' + children_str + ('\n' * pretty * any_expanded) + ']'
        )


class ExpandableTreeNode(ExpandableList):

    def __init__(self,
                 wrapped: Any,
                 children_extractor: Callable[[Any], List[Any]],
                 search_similarity_fn: Callable[[str, Any], float],
                 search_filter_kwargs=None
                 ) -> None:
        search_filter_kwargs = search_filter_kwargs or {}
        children = children_extractor(wrapped) or []

        if len(children) > 0:  # non-leaf node must have attributes for rendering. leaf nodes just use __repr__
            assert hasattr(wrapped, 'range'), str(wrapped)
            assert isinstance(wrapped.range, Tuple), str(wrapped)
            assert len(wrapped.range) == 2 and all(isinstance(x, datetime) for x in wrapped.range), str(wrapped)
            assert hasattr(wrapped, 'nl_summary'), str(wrapped)
            assert isinstance(wrapped.nl_summary, str), str(wrapped)

        self._wrapped = wrapped
        search_filter_fn = search_similarity_to_filter_fn(search_similarity_fn, **search_filter_kwargs)
        super().__init__(children=[
            ExpandableTreeNode(c, children_extractor, search_similarity_fn)
            for c in children
        ], filter_fn_generator=create_expandable_tree_node_filter_fn,
            search_filter_fn=search_filter_fn)

        self._all_leaves = None

    @cached_property
    def all_leaves(self):
        if len(self.children) == 0:
            return [self._wrapped]
        return ExpandableList(
            list(chain(*(c.all_leaves for c in self.children))),
            create_index_only_filter_fn,
            self._search_filter_fn
        )

    def __repr__(self):
        if len(self.children) == 0:
            return repr(self._wrapped)  # leaf node
        pretty = PRETTY_PRINT or self._simplified_repr  # Simplified depends on spacing

        cls_name = self._wrapped.__class__.__name__
        range_str = format_datetime_range(*self._wrapped.range)
        children_str = super().__repr__()[1:-1].strip()  # strip away the [] and whitespace
        children_str = indent_following_lines(children_str, num_spaces=INDENT_SIZE * pretty)
        children_str = ((('\n' + ' ' * INDENT_SIZE * (1 if self._simplified_repr else 2)) * pretty)
                        + children_str + (('\n' + ' ' * INDENT_SIZE) * pretty))

        nl_summary = indent_following_lines(self._wrapped.nl_summary, num_spaces=INDENT_SIZE * pretty)
        if len(nl_summary.splitlines()) > 1:
            nl_summary = f'"""{nl_summary}"""'
        else:
            nl_summary = f'"{nl_summary}"'

        ____ = ' ' * INDENT_SIZE * pretty
        _n = '\n' if pretty else ''
        _ns = '\n' if pretty else ' '

        if self._simplified_repr:
            return (
                f'{range_str}: {nl_summary}'
                f'{____}{children_str.rstrip()}'
            )
        return (
                f'{cls_name}({_n}'
                f'{____}{range_str},{_ns}'
                f"{____}{nl_summary},{_ns}"
                + ____ + r'children={' + children_str + '}' + _n +
                f')'
        )

    def __getattribute__(self, __name):
        if '__' in __name or __name.startswith('_') or __name in dir(self):
            return super().__getattribute__(__name)
        return getattr(self._wrapped, __name)


def recursive_apply(node, fn):
    fn(node)
    if hasattr(node, 'children'):
        for c in node.children:
            recursive_apply(c, fn)


def search_similarity_to_filter_fn(
        search_similarity_fn: Callable[[str, Any], float],
        top_p=0.5,
        min_cos_sim=0.2,
        close_match_top_p=0.4,
        close_match_min_cos_sim=0.7,
) -> Callable[[str, List[Any], ...], List[int]]:
    def search(query: str, items: List[Any], close_match=False):
        _top_p = close_match_top_p if close_match else top_p
        _min_cos_sim = close_match_min_cos_sim if close_match else min_cos_sim

        similarities = torch.tensor([search_similarity_fn(query, item) for item in items])
        normalized_scores = torch.softmax(similarities, dim=0)
        sorted_scores, indices = torch.sort(normalized_scores, descending=True)
        cum_scores = torch.cumsum(sorted_scores, dim=0)
        # noinspection PyTypeChecker
        top_k = torch.count_nonzero(cum_scores < _top_p) + 1
        top_indices = indices[:top_k]
        top_raw_scores = similarities[top_indices]
        return top_indices[top_raw_scores > _min_cos_sim].tolist()

    return search
