import asyncio
from asyncio import CancelledError
from dataclasses import dataclass
from datetime import timedelta, datetime
from threading import RLock
from typing import Union, Tuple, Optional, List

from llm_emv.interactive_tree import format_datetime_range
from ..em_tree import AnyTreeNode, SceneGraphInstant, EventBasedSummary, GoalBasedSummary, HigherLevelSummary, \
    RawDataInstant, type_to_children_property_map
from ..list_util import first_line

AnyTreeNodeInclRaw = Union[AnyTreeNode, RawDataInstant]


class RelevanceEstimator:

    def value(self, node: AnyTreeNodeInclRaw, parent_path: List[AnyTreeNode], now: datetime) -> Optional[int]:
        """
        Values the given node's relevance according to the context. This is never called for the root node, so the
        parent_path is always non-empty.
        :param node: the node to value
        :param parent_path: The path of parents, from the direct parent to the root node
        :param now: the current time
        :return: 0 if this is not relevant and can be forgotten, higher int values to signify more relevance.
                 The relevance will be used as a factor for the added lifetime of this memory.
                 Can return None if this estimator cannot handle this item.
        """
        raise NotImplementedError

    async def async_batch_value(self,
                                nodes: List[AnyTreeNodeInclRaw],
                                shared_parent_path: List[AnyTreeNode],
                                now: datetime
                                ) -> List[Optional[int]]:
        return [
            self.value(node, shared_parent_path, now)
            for node in nodes
        ]


@dataclass
class ForgettingManagerSettings:
    default_raw_ttl: timedelta = timedelta(minutes=15)
    default_scene_ttl: timedelta = timedelta(hours=1)
    default_event_ttl: timedelta = timedelta(hours=3)
    default_goal_ttl: timedelta = timedelta(hours=24)
    default_higher_ttl: timedelta = timedelta(days=3)
    higher_level_ttl_multiplier: int = 2

    @property
    def type_to_default_ttl(self):
        return {
            RawDataInstant: self.default_raw_ttl,
            SceneGraphInstant: self.default_scene_ttl,
            EventBasedSummary: self.default_event_ttl,
            GoalBasedSummary: self.default_goal_ttl,
            HigherLevelSummary: self.default_higher_ttl,
        }


# duck typing
class _ForgottenSceneEntry:

    def __init__(self, timestamp: datetime):
        super().__init__()
        self._forgotten = True
        self.objects = []
        self.relations = []
        self.image = None
        self.index_content = []
        self.nl_graph_summary = ''
        self.raw = RawDataInstant(timestamp=timestamp, current_action='<forgotten>')
        self.scene_description = '<forgotten>'

    def __repr__(self):
        return self.raw.timestamp.strftime('%Y/%m/%d %H:%M:%S') + ': ' + self.scene_description


# duck typing
class _ForgottenSummaryEntry:

    def __init__(self, range: Tuple[datetime, datetime],
                 num_deeper_summary_layers=0,
                 include_higher=True,
                 forgotten_summary=None):
        super().__init__()
        self.range = range
        self._forgotten = True
        self.num_deeper_summary_layers = num_deeper_summary_layers

        # Event
        self.scenes = []
        self.audio_description = None
        self.explicit_action = 'forgotten'
        self.action_parameter_summary = None
        self.latest_scene = _ForgottenSceneEntry(self.range[1])
        self.latest_raw = self.latest_scene.raw
        self.speech_events = []
        self.image = None
        self.nl_summary = '<forgotten>'
        self.forgotten_summary = forgotten_summary
        self.index_content = []

        if include_higher:
            # Goal
            self.events = []
            self.explicit_goal = 'forgotten'
            self.latest_event = _ForgottenSummaryEntry(range, include_higher=False)  # avoid endless recursion
            # Higher
            self.children = []

    def __repr__(self):
        return format_datetime_range(*self.range) + ': ' + self.nl_summary


def _range(n: AnyTreeNodeInclRaw):
    if isinstance(n, RawDataInstant):
        return n.timestamp, n.timestamp
    elif isinstance(n, (SceneGraphInstant, _ForgottenSceneEntry)):
        return _range(n.raw)
    else:
        return n.range


def _count_deeper_summary_layers(h: HigherLevelSummary):
    if not isinstance(h, HigherLevelSummary):
        return 0
    if isinstance(h, _ForgottenSummaryEntry):
        return h.num_deeper_summary_layers

    result = 1e6  # arbitrary high value
    for c in h.children:
        if isinstance(c, HigherLevelSummary):
            result = min(result, _count_deeper_summary_layers(c) + 1)
        else:
            return 0
    return result


class ForgettingManager:

    def __init__(self,
                 relevance_estimators: List[RelevanceEstimator],
                 **kwargs):
        super().__init__()
        self.relevance_estimators = relevance_estimators
        self._s = ForgettingManagerSettings(**kwargs)
        self._running = False
        self._cancel = False
        self._estimator_tasks = []
        self._state_lock = RLock()

    async def modify(self, history: HigherLevelSummary,
                     now: datetime = None):
        with self._state_lock:
            self._running = True
            self._cancel = False
            self._estimator_tasks = []
        if now is None:
            now = datetime.now()
        await self._assign_or_extend_expiry_dates([history], [], now)
        await self._deep_iter(history, [], now)
        with self._state_lock:
            self._running = False
            self._estimator_tasks = []

    def cancel_forgetting(self):
        with self._state_lock:
            if self._running:
                self._cancel = True
                for task in self._estimator_tasks:
                    task.cancel()

    async def _assign_or_extend_expiry_dates(self,
                                             nodes: List[AnyTreeNodeInclRaw],
                                             shared_parent_path: List[AnyTreeNode],
                                             now: datetime):
        todo_check_extend = []
        for node in nodes:
            if is_forgotten(node):
                continue

            expiry_date: datetime
            if hasattr(node, '_expiry_date'):
                expiry_date = node._expiry_date
            else:
                try:
                    if isinstance(node, HigherLevelSummary):
                        num_deeper_summary_layers = _count_deeper_summary_layers(node)
                        expiry_date = _range(node)[1] + self._s.type_to_default_ttl[HigherLevelSummary] * (
                                self._s.higher_level_ttl_multiplier ** num_deeper_summary_layers)
                    else:
                        node_type = type(node)
                        if isinstance(shared_parent_path[0], GoalBasedSummary):
                            node_type = EventBasedSummary  # Even for nested goals, only keep the top-level goal longer
                        expiry_date = _range(node)[1] + self._s.type_to_default_ttl[node_type]
                except OverflowError:
                    expiry_date = datetime.max

            node._expiry_date = expiry_date

            if expiry_date < now:
                todo_check_extend.append(node)

        if shared_parent_path:
            extended_dates = await self._check_extend_lifetimes(todo_check_extend, shared_parent_path, now)

            for node, extended_date in zip(todo_check_extend, extended_dates):
                node._expiry_date = extended_date or node._expiry_date

    async def _deep_iter(
            self, node: AnyTreeNodeInclRaw,
            parent_path: List[AnyTreeNode],
            now: datetime
    ) -> bool:
        if is_forgotten(node):
            return False

        with self._state_lock:
            if self._cancel:
                # Do not recurse further into children
                return False

        expiry_date = node._expiry_date

        if expiry_date < now and parent_path:
            print('Forgetting', str(node)[:150] + '...')
            if isinstance(node, RawDataInstant):
                node._forgotten = True
                node.image = None if node.image is None else 'forgotten'
                node.sound = None if node.sound is None else 'forgotten'
                node.current_action_parameters = None if node.current_action_parameters is None else 'forgotten'
            return True  # Remove from parent

        new_parent_path = [node] + parent_path
        # Not yet expired (or allowed to expire), but may have expired children
        if isinstance(node, SceneGraphInstant):
            await self._assign_or_extend_expiry_dates([node.raw], new_parent_path, now)
            await self._deep_iter(node.raw, new_parent_path, now)
            # noinspection PyUnresolvedReferences,PyProtectedMember
            expiry_date = max(expiry_date, getattr(node.raw, '_expiry_date', expiry_date))
        elif isinstance(node, (EventBasedSummary, GoalBasedSummary, HigherLevelSummary)):
            children = getattr(node, type_to_children_property_map[type(node)])
            await self._assign_or_extend_expiry_dates(children, new_parent_path, now)
            for i, child in enumerate(children):
                if await self._deep_iter(child, new_parent_path, now):
                    children[i] = (_ForgottenSceneEntry(child.raw.timestamp)
                                   if isinstance(child, SceneGraphInstant)
                                   else _ForgottenSummaryEntry(child.range,
                                                               _count_deeper_summary_layers(child),
                                                               forgotten_summary=first_line(child.nl_summary)))
                    # Assign explicit action or goal if necessary (to keep summary)
                    if i + 1 == len(children):
                        if isinstance(node, EventBasedSummary) and not node.explicit_action:
                            node.explicit_action = child.raw.current_action
                        if isinstance(node, GoalBasedSummary) and not node.explicit_goal:
                            node.explicit_goal = child.latest_raw.current_goal
            _merge_forgotten_children(children)
            expiry_date = max([expiry_date] + [c._expiry_date for c in children if hasattr(c, '_expiry_date')])

        node._expiry_date = expiry_date
        return False

    async def _check_extend_lifetimes(self, nodes: List[AnyTreeNode],
                                      shared_parent_path: List[AnyTreeNode],
                                      now: datetime) -> List[Optional[datetime]]:
        relevant_indices = []
        for i, node, in enumerate(nodes):
            is_irrelevant_raw = (
                    isinstance(node, RawDataInstant)
                    and node.image is None
                    and node.sound is None
                    and node.current_action_parameters is None
            )
            if not is_irrelevant_raw:
                relevant_indices.append(i)
        relevant_nodes = [nodes[i] for i in relevant_indices]

        values = [0] * len(relevant_nodes)
        cancelled = False
        for estimator in self.relevance_estimators:
            task = asyncio.create_task(estimator.async_batch_value(relevant_nodes, shared_parent_path, now))
            with self._state_lock:
                if self._cancel:
                    task.cancel()
                    cancelled = True
                    break
                else:
                    self._estimator_tasks.append(task)
            try:
                await task
            except CancelledError:
                cancelled = True
                break
            estimator_values = task.result()
            for i, estimator_value in enumerate(estimator_values):
                if estimator_value is not None:
                    values[i] = max(values[i], estimator_value)

        if cancelled:
            return [None] * len(nodes)

        result = []
        for i, node in enumerate(nodes):
            if i in relevant_indices:
                rel_idx = relevant_indices.index(i)
                if values[rel_idx] > 0:
                    try:
                        result.append(now + values[rel_idx] * self._s.type_to_default_ttl[type(node)])
                    except OverflowError:
                        result.append(datetime.max)
            else:
                result.append(None)

        return result


def _merge_forgotten_children(children: List[AnyTreeNode]):
    # noinspection PyTypeChecker
    def merge_marked_indices():
        if len(consecutive_forgotten_indices) <= 1:
            return 0  # Not possible to merge anything
        first_idx = consecutive_forgotten_indices[0]
        last_idx = consecutive_forgotten_indices[-1]
        start = _range(children[first_idx])[0]
        end = _range(children[last_idx])[1]
        forgotten_children_type = type(children[first_idx])
        forgotten_children = children[first_idx:last_idx + 1]
        assert all(isinstance(c, forgotten_children_type) for c in forgotten_children)
        num_deeper_layers = min(c.num_deeper_summary_layers for c in forgotten_children
                                ) if forgotten_children_type == _ForgottenSummaryEntry else None
        old_children_length = len(children)
        del children[first_idx:last_idx + 1]
        idx_correction = len(consecutive_forgotten_indices)
        if forgotten_children_type == _ForgottenSummaryEntry:
            children.insert(first_idx, _ForgottenSummaryEntry((start, end),
                                                              num_deeper_layers,
                                                              forgotten_summary='. '.join(c.forgotten_summary
                                                                                          for c in forgotten_children)))
            idx_correction -= 1
        elif forgotten_children_type == _ForgottenSceneEntry:
            # Need to make sure to keep first and last entry for DT range
            if first_idx == 0:
                children.insert(first_idx, _ForgottenSceneEntry(start))
                idx_correction -= 1
            if last_idx + 1 == old_children_length:
                children.append(_ForgottenSceneEntry(end))
                idx_correction -= 1
        else:
            raise NotImplementedError(forgotten_children_type)

        return idx_correction

    consecutive_forgotten_indices = []
    i = 0
    while i < len(children):
        if isinstance(children[i], (_ForgottenSceneEntry, _ForgottenSummaryEntry)):
            consecutive_forgotten_indices.append(i)
        else:
            i -= merge_marked_indices()
            consecutive_forgotten_indices.clear()
        i += 1
    merge_marked_indices()


def is_forgotten(p):
    return getattr(p, '_forgotten', False)
