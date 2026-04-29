import json
import re
import traceback
from collections import defaultdict, namedtuple
from concurrent.futures.thread import ThreadPoolExecutor
from copy import copy
from datetime import datetime, timedelta
from itertools import chain
from pathlib import Path
from typing import Union, List, Optional, Dict, Tuple, Literal, Any, Generator, Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate as SystemMsg, HumanMessagePromptTemplate as HumanMsg, \
    AIMessagePromptTemplate as AIMsg, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from lmp.util import invoke_chain_with_adaptive_length_content
from .em_tree import (HigherLevelSummary, EventBasedSummary, GoalBasedSummary, SceneGraphInstant,
                      AnyTreeNode, type_to_children_property_map)
from .em_util import initial_text_forgiving_json_fixing_parser
from .list_util import SliceListView, ConcatenatedListView, first_line
from .organize.forget import is_forgotten


def format_rel_date(prev_date: Optional[datetime], date_to_format: datetime):
    if prev_date is None or date_to_format.date() != prev_date.date():
        return date_to_format.strftime('%Y/%m/%d %H:%M:%S')
    else:
        return date_to_format.strftime('%H:%M:%S')


_SummaryGroup = namedtuple('SummaryGroup', ['summary', 'items'])
_HistoryItem = namedtuple('HistoryItem', ['text', 'range'])


# Stateful (!) object to build history incrementally
class IncrementalHistoryBuilder:

    def __init__(self,
                 llm: Union[BaseChatModel, List[BaseChatModel]],
                 context_window=3,
                 finalize_llm=None,
                 retry_llm=None,
                 fix_json_llm=None,
                 receive_item_prompt: Union[List[ChatPromptTemplate], ChatPromptTemplate] = None,
                 simple_summary_prompt: Union[List[ChatPromptTemplate], ChatPromptTemplate, str] = None,
                 relevance_language_rule_file_path: Path = None,
                 reduce_old_item_details_to_characters=None):
        super().__init__()

        if not isinstance(llm, List):
            llm = [llm]

        if finalize_llm is None:
            finalize_llm = llm  # Can also be multiple ones
        default_llm = llm[-1]
        if fix_json_llm is None:
            fix_json_llm = default_llm
        if retry_llm is None:
            retry_llm = default_llm

        if isinstance(simple_summary_prompt, str):
            simple_summary_prompt = (
                    SystemMsg.from_template(simple_summary_prompt)
                    + HumanMsg.from_template("{input}")
            )
        if not isinstance(simple_summary_prompt, list):
            simple_summary_prompt = [simple_summary_prompt]
        inject_relevance_rules = RunnablePassthrough.assign(
            relevance_rule_msg=lambda x: self._prepare_relevance_rule_msg())
        if not isinstance(finalize_llm, list):
            finalize_llm = [finalize_llm]
        self._simple_summarize_chains = defaultdict(
            lambda: inject_relevance_rules | simple_summary_prompt[-1] | finalize_llm[-1] | StrOutputParser(),
            {i: inject_relevance_rules
                | simple_summary_prompt[min(len(simple_summary_prompt) - 1, i)]
                | finalize_llm[min(len(finalize_llm) - 1, i)]
                | StrOutputParser()
             for i in range(max(len(finalize_llm), len(simple_summary_prompt)))}
        )

        retry_prompt = (
                AIMsg.from_template('{wrong_output}') +
                HumanMsg.from_template(
                    'The given output is not valid:\n'
                    '{errors}\n'
                    'Carefully consider the input indices, and the erroneous output. '
                    'Provide an improved JSON that fixes all errors.'
                )
        )
        if not isinstance(receive_item_prompt, list):
            receive_item_prompt = [receive_item_prompt]
        self._receive_item_chains = defaultdict(
            lambda: (inject_relevance_rules | receive_item_prompt[-1] | default_llm
                     | initial_text_forgiving_json_fixing_parser(fix_json_llm)),
            {i: (inject_relevance_rules
                 | receive_item_prompt[min(len(receive_item_prompt) - 1, i)]
                 | llm[min(len(llm) - 1, i)]
                 | initial_text_forgiving_json_fixing_parser(fix_json_llm))
             for i in range(max(len(llm), len(receive_item_prompt)))}
        )
        if not isinstance(retry_llm, list):
            retry_llm = [retry_llm]
        self._retry_receive_item_chains = defaultdict(
            lambda: ((receive_item_prompt[-1] + retry_prompt)
                     | retry_llm[-1] | initial_text_forgiving_json_fixing_parser(fix_json_llm)),
            {i: ((receive_item_prompt[min(len(receive_item_prompt) - 1, i)]
                  + retry_prompt)
                 | retry_llm[min(len(retry_llm) - 1, i)]
                 | initial_text_forgiving_json_fixing_parser(fix_json_llm))
             for i in range(max(len(retry_llm), len(receive_item_prompt)))}
        )
        self._max_retry_attempts = 2
        self._max_retry_reduce_length_attempts = 10
        self._reduce_old_item_details_to_characters = reduce_old_item_details_to_characters
        self._relevance_language_rule_file_path = relevance_language_rule_file_path
        self._reduce_chars_remove_date_threshold = 40
        self._reduce_chars_remove_date_threshold_2 = 25

        self._context_window = context_window

        self._tree: HigherLevelSummary = None

    def _prepare_relevance_rule_msg(self):
        if self._relevance_language_rule_file_path is None or not self._relevance_language_rule_file_path.is_file():
            return []
        rules = json.loads(self._relevance_language_rule_file_path.read_text())
        if not rules:
            return []
        rule_str = '\n'.join(f'- {rule}' for rule in rules)
        return [HumanMessage('Consider the following rules when summarizing items:' + rule_str)]

    def _batch_scenes(self, scenes: List[SceneGraphInstant],
                      batch_size_hint: int):
        for i in range(0, len(scenes), batch_size_hint):
            yield scenes[i:i + batch_size_hint]

    def process_batch(self, new_scenes: List[SceneGraphInstant],
                      max_new_scene_batch=25):
        new_scenes.sort(key=lambda s: s.raw.timestamp)
        if self._tree is None and len(new_scenes) > 1:
            self._process(new_scenes[:1])
            yield from self.process_batch(new_scenes[1:], max_new_scene_batch)  # not _process to use batching
        else:
            for batch in self._batch_scenes(new_scenes, max_new_scene_batch):
                yield self._process(batch)

    def process(self, scene: SceneGraphInstant) -> HigherLevelSummary:
        return self._process([scene])

    def _process(self, new_scenes: List[SceneGraphInstant]) -> HigherLevelSummary:
        if self._tree is None:
            assert len(new_scenes) == 1
            self._tree = new_scenes[0]
            for i in range(3):  # event, goal, summary
                self._tree = self._merge([], [self._tree], i)[0]
            # noinspection PyTypeChecker
            return self._tree

        previous_range = self._tree.range
        assert all(s.raw.timestamp > previous_range[-1] for s in new_scenes)
        _propagate_parent(self._tree, deep=True)  # In case entries have been modified, e.g. by forgetting manager

        edge_children_per_layer = [[self._tree]] + _collect_edge_children(self._tree, self._context_window)
        # Sanity check: all items in one layer should have the same type (or forgotten)
        for layer in edge_children_per_layer:
            non_forgotten_layer = [n for n in layer if not is_forgotten(n)]
            assert all(isinstance(n, type(non_forgotten_layer[-1])) for n in non_forgotten_layer)

        new_items = new_scenes
        i = 0
        while i < len(edge_children_per_layer):
            layer_parents = edge_children_per_layer[-(i + 2)]
            valid_parents = [p for p in layer_parents
                             if len(_children(p)) > 0  # invalid empty nodes (by lower-level modification) => exclude
                             or is_forgotten(p)  # Forgotten children have a valid range => include
                             ]

            if (
                    self._disallow_push_to_upper_layer(i, new_items)
                    and valid_parents
                    and not is_forgotten(valid_parents[-1])
            ):
                print('Disallowing push to upper layer!', i, new_items[0].range[0])
                last_parent = valid_parents[-1]
                new_last_parent = self._simple_summarize_items(_children(last_parent) + new_items, i)
                if last_parent.parent is None:
                    assert i + 2 == len(edge_children_per_layer)
                    self._tree = new_last_parent
                else:
                    siblings = _children(last_parent.parent)
                    siblings[siblings.index(last_parent)] = new_last_parent
                    # could also recursively update parent summaries here
                new_last_parent.parent = last_parent.parent
                last_parent.parent = None
                break

            cutoff_times_and_new_items = self._cluster_new_items_with_visibility_cutoff(i, new_items)
            assert len(cutoff_times_and_new_items) >= 1
            result = valid_parents
            visible_parents, first_visible_idx = ..., ...  # Only here to avoid warning, loop will definitely run once
            for cutoff_time, local_new_items in cutoff_times_and_new_items:
                print('Cutoff', cutoff_time, 'for', len(local_new_items), 'of', len(new_items), 'items on lvl', i)
                first_visible_idx = min((i for i, p in enumerate(result)
                                         if p.range[1] >= cutoff_time),
                                        default=len(result)  # in case there is no visible item
                                        )
                first_visible_idx = max(
                    [i + 1 for i, p in enumerate(result) if is_forgotten(p)]
                    + [first_visible_idx]
                    # first_visible_idx is not default but also in the list since it should be considered by
                    # max even if there are previous forgotten parents
                )  # Automatically cut off visibility when there is a forgotten parent summary.
                # Otherwise, this could mix up everything when re-grouping the child items
                # (since forgotten summary has no children).
                visible_parents = result[first_visible_idx:]
                for p in visible_parents:
                    p._finalized = False  # reset finalized state
                local_result = self._merge(visible_parents, local_new_items, i)
                result = result[:first_visible_idx] + local_result  # put the hidden children back in

            first_changed_idx = None
            for j in range(len(result)):
                if j >= len(valid_parents) or not self._treat_as_equal(valid_parents[j], result[j]):
                    first_changed_idx = j
                    break
            any_change = first_changed_idx is not None

            if len(result) > len(visible_parents):  # Finalize hidden and soon out of context window items
                visible_next_time = min(self._context_window, len(result) - first_visible_idx)
                for item_to_finalize in result[:-visible_next_time]:
                    if not getattr(item_to_finalize, '_finalized', False):
                        self._finalize(item_to_finalize, i)
                        item_to_finalize._finalized = True

            i += 1
            if i + 1 == len(edge_children_per_layer):
                if len(result) == 1:
                    self._tree = result[0]
                else:
                    self._tree = self._simple_summarize_items(result, i)
                break
            for prev, new in zip(valid_parents, result[:first_changed_idx]):
                if prev is new:
                    continue  # Do not modify if instance stayed the same
                siblings = _children(prev.parent)
                idx = siblings.index(prev)
                siblings[idx] = new
                new.parent = prev.parent
                prev.parent = None
            if any_change:
                new_items = result[first_changed_idx:]  # This is merged again in the layer above

                all_siblings = []
                for old in valid_parents[first_changed_idx:]:
                    # The old item should be removed from its parent. However, this very likely invalidates the summary
                    #  of the parent => all siblings of the old item should be treated as new_items as well
                    siblings = _children(old.parent)
                    for s in list(siblings):
                        if s not in all_siblings and s not in valid_parents[first_changed_idx:]:
                            all_siblings.append(s)
                            _remove_recursively(s)
                    _remove_recursively(old)

                new_items += all_siblings
                new_items.sort(key=lambda item: item.range)
                _ensure_consecutive_times(HigherLevelSummary('', new_items))
            else:
                for removed in valid_parents[len(result):]:
                    _remove_recursively(removed)
                    removed.parent = None
                # could adapt summary of parents that lost some children. Ignoring for now.
                break

        self._tree = _simplify_ensuring_balanced_tree(self._tree)
        self._tree.parent = None  # Might be in case unnecessary single-item summary was dropped

        _ensure_consecutive_times(self._tree)
        assert self._tree.range[0] == previous_range[0]
        assert self._tree.range[1] > previous_range[1]
        assert self._tree.range[1] == new_scenes[-1].raw.timestamp

        return self._tree

    def _get_time_ranges(self, ctx=50):
        highest_layer = [[self._tree]] if self._tree.children else []
        layers = highest_layer + _collect_edge_children(self._tree, num=ctx)  # num for sufficient stats
        layers.reverse()
        return [
            [
                _range(s)
                for s in layer
            ]
            for layer in layers
        ]

    def _cluster_time_ranges(self, lvl: int,
                             time_ranges: List[Tuple[datetime, datetime]],
                             tolerance_masters: int = None) -> List[Tuple[datetime, datetime]]:
        if tolerance_masters is None:
            tolerance_masters = len(time_ranges)
        clusters = list(time_ranges)
        num_clusters_before = None
        while num_clusters_before != len(clusters) > 1:
            num_clusters_before = len(clusters)

            # Find the nearest two ranges
            distances = [(r2[0] - r1[1], i)
                         for i, (r1, r2) in enumerate(zip(clusters[:-1], clusters[1:]))]
            min_dist, i = min(distances)
            r1, r2 = clusters[i], clusters[i + 1]
            max_duration = max(max(c[1] - c[0] for c in clusters[-tolerance_masters:]),
                               timedelta(seconds=1))  # some min clustering tolerance
            merge_threshold = max_duration * (5 + lvl)  # 5: arbitrary base tolerance. tolerance increases with lvl

            if min_dist <= merge_threshold:
                if i >= len(clusters) - tolerance_masters:
                    tolerance_masters -= 1
                    assert tolerance_masters > 0 or len(clusters) == 1
                # Merge r1, r2
                clusters[i:i + 2] = [(r1[0], r2[1])]

        for c1, c2 in zip(clusters[:-1], clusters[1:]):
            assert c1[1] < c2[0]
        return clusters

    def _cluster_new_items_with_visibility_cutoff(self, lvl: int, new_items: List[AnyTreeNode]
                                                  ) -> List[Tuple[datetime, List[AnyTreeNode]]]:
        layers = self._get_time_ranges()
        if lvl >= len(layers):  # Tree got modified
            return [(datetime.min, new_items)]

        time_ranges = layers[lvl]
        if len(time_ranges) == 0:
            return [(datetime.min, new_items)]

        clusters = self._cluster_time_ranges(lvl,
                                             time_ranges + [_range(n) for n in new_items],
                                             len(new_items))

        result = []
        for n in new_items:
            r_n = _range(n)
            cluster_containing_n = [c for c in clusters if c[0] <= r_n[0] <= r_n[1] <= c[1]]
            assert len(cluster_containing_n) == 1
            cluster_containing_n = cluster_containing_n[0]
            if result and result[-1][0] == cluster_containing_n[0]:
                result[-1][1].append(n)
            else:
                result.append((cluster_containing_n[0], [n]))

        return result

    def _disallow_push_to_upper_layer(self, lvl: int, new_items: List[AnyTreeNode]) -> bool:
        if lvl <= 1:
            return False
        all_time_ranges = self._get_time_ranges()
        if lvl + 1 >= len(all_time_ranges):  # happens if tree was modified in between
            return False

        # We need to look at the layer above here. We disallow pushing to upper layer if the gap on the upper layer
        #  would be very small in comparison to the existing gaps there.
        time_ranges = all_time_ranges[lvl + 1]
        distances = [r2[0] - r1[1]
                     for r1, r2 in zip(time_ranges[:-1], time_ranges[1:])]

        resulting_gap = new_items[0].range[0] - time_ranges[-1][1]
        if resulting_gap.total_seconds() <= 0:  # Existing item was extended
            return False

        if len(distances):
            min_gap_on_this_layer = min(distances)
            if resulting_gap * 10 < min_gap_on_this_layer:  # Gap would be weirdly small
                return True
        else:  # Consider the duration instead
            existing_duration = time_ranges[0][1] - time_ranges[0][0]
            new_duration = max(new_items[-1].range[1] - new_items[0].range[0], timedelta(seconds=1))
            if new_duration * 10 < existing_duration and resulting_gap * 10 < existing_duration:
                return True

        return False

    def _finalize(self, item, lvl: int):
        # Finalizing a tree item when it is not part of the context window anymore
        #   => regenerate summary based on the actual children
        #      (independent of previous/next summaries, to ensure consistency with its own content)
        if is_forgotten(item):
            return item

        if isinstance(item, HigherLevelSummary):
            summary_prop_name = 'nl_summary'
            children = item.children
        elif isinstance(item, GoalBasedSummary):
            summary_prop_name = 'explicit_goal'
            children = item.events
        elif isinstance(item, EventBasedSummary):
            summary_prop_name = 'explicit_action'
            children = item.scenes
        else:
            raise ValueError(item)

        def _create_children_str(reduce_chars: int):
            children_str = ''
            prev_date = None
            for c in children:
                if isinstance(c, SceneGraphInstant):
                    children_str += (f'- {format_rel_date(prev_date, c.raw.timestamp)}: '
                                     f'{self._scene_to_text(c)[:reduce_chars]}\n')
                    prev_date = c.raw.timestamp

                else:
                    summary = self._hl_item_to_text(c).replace("Action: ", "")
                    children_str += (f'{self._adaptive_format_date_range(prev_date, c.range, reduce_chars, lvl)}'
                                     f'{summary[:reduce_chars]}\n')
                    prev_date = c.range[1]
            return children_str

        new_summary = self._simple_summarize_with_adaptive_length(_create_children_str, lvl)
        setattr(item, summary_prop_name, new_summary)
        return item

    def _simple_summarize_items(self, items: List[Union[GoalBasedSummary, HigherLevelSummary]], lvl: int):
        assert items
        if len(items) == 1 and isinstance(items[0], HigherLevelSummary):
            return items[0]

        def _create_children_str(reduce_chars: int):
            children_str = ''
            prev_date = None
            for c in items:
                children_str += (f'{self._adaptive_format_date_range(prev_date, c.range, reduce_chars, lvl)}'
                                 f'{self._hl_item_to_text(c)[:reduce_chars]}\n')
                prev_date = c.range[1]
            return children_str

        new_summary = self._simple_summarize_with_adaptive_length(_create_children_str, lvl)
        summary = HigherLevelSummary(new_summary, items)
        summary.parent = None
        _propagate_parent(summary)
        _ensure_consecutive_times(summary)
        return summary

    def _merge(self, existing_items, new_items, lvl: int):
        lower_merge_fns = {0: self._merge_new_scene,
                           1: self._merge_new_event,
                           2: self._merge_new_goal}
        if lvl in lower_merge_fns:
            # noinspection PyArgumentList
            result = lower_merge_fns[lvl](existing_items, new_items)
        else:
            result = self._merge_new_summary(existing_items, new_items, lvl)

        for r in result:
            assert getattr(r, 'parent', None) is None, f'Merge results should be new instances, {r}'
            r.parent = None
            _propagate_parent(r)
            _ensure_consecutive_times(r)
        return result

    # Stateless
    def _merge_new_summary(self, prev_summaries: List[HigherLevelSummary],
                           new_items: List[HigherLevelSummary], lvl: int):
        all_summaries = [h for s in prev_summaries for h in s.children] + new_items
        assert all(isinstance(s, HigherLevelSummary) for s in all_summaries if not is_forgotten(s))

        if len(all_summaries) == 1:
            # Save some computation. But stack anyway to (internally) ensure balanced tree
            return [HigherLevelSummary(self._hl_item_to_text(all_summaries[0]),
                                       children=all_summaries)]

        if len(all_summaries) == 2:
            # creating two single-item summaries would be useless => force simple summary
            return [self._simple_summarize_items(all_summaries, lvl)]

        clusters = self._cluster_time_ranges(lvl, [s.range for s in all_summaries],
                                             len(new_items))
        if len(clusters) == len(all_summaries):
            # enforcing single-item clusters would be useless. The LLM can do whatever it wants
            clusters = [(clusters[0][0], clusters[-1][1])]
        if len(clusters) == 1:
            new_groups = self._merge_new_items(
                prev_summaries=[_SummaryGroup(
                    summary=h.nl_summary,
                    items=[_HistoryItem(self._hl_item_to_text(s), s.range) for s in h.children]
                ) for h in prev_summaries],
                new_items=[_HistoryItem(self._hl_item_to_text(new_item), new_item.range)
                           for new_item in new_items],
                lvl=lvl
            )
            return [
                HigherLevelSummary(
                    children=all_summaries[start:end],
                    nl_summary=summary,
                )
                for start, end, summary in new_groups
            ]
        else:
            result = []
            for c in clusters:
                items_in_c = [s for s in all_summaries
                              if c[0] <= s.range[0] <= s.range[1] <= c[1]]
                parents_in_c = [p for p in prev_summaries
                                if all(x in items_in_c for x in p.children)]
                if sum(len(p.children) for p in parents_in_c) == len(items_in_c):
                    result += [  # Copy to hold the assumption that merge_new_summary always returns fresh objects
                        shallow_copy_summary(p)
                        for p in parents_in_c
                    ]
                else:
                    items_without_parent = [i for i in items_in_c
                                            if not any(i in p.children for p in parents_in_c)]
                    if items_without_parent == items_in_c[-len(items_without_parent):]:
                        # This is the "standard" case: The clustering aligns with the boundaries of prev_summaries
                        result += self._merge_new_summary(parents_in_c, items_without_parent, lvl)
                    else:
                        # Rarely, this can happen: Clustering does not align with prev_summaries.
                        #  Then, a previous cluster already used part of a summary but not all children.
                        #  => need to re-construct all unaligned subsequent summaries
                        result += self._merge_new_summary([], items_in_c, lvl)
            return result

    # Stateless
    def _merge_new_goal(self, prev_summaries: List[HigherLevelSummary], new_items: List[GoalBasedSummary]):
        all_goals = [g for s in prev_summaries for g in s.children] + new_items
        assert all(isinstance(g, GoalBasedSummary) for g in all_goals if not is_forgotten(g)), str([type(x) for x in all_goals])

        def _goal(g: GoalBasedSummary):
            if getattr(g, 'explicit_goal', None):
                return g.explicit_goal
            else:
                return g.nl_summary.replace('Goal: ', '')

        new_groups = self._merge_new_items(
            prev_summaries=[_SummaryGroup(
                summary=s.nl_summary,
                items=[_HistoryItem(_goal(g), g.range) for g in s.children]
            ) for s in prev_summaries],
            new_items=[_HistoryItem(_goal(new_item), new_item.range)
                       for new_item in new_items],
            lvl=2
        )
        return [
            HigherLevelSummary(
                children=all_goals[start:end],
                nl_summary=summary,
            ) for start, end, summary in new_groups
        ]

    # Stateless
    def _merge_new_event(self, prev_summaries: List[GoalBasedSummary], new_items: List[EventBasedSummary]):
        all_events = [e for g in prev_summaries for e in g.events] + new_items

        new_groups = self._merge_new_items(
            prev_summaries=[_SummaryGroup(
                summary=g.explicit_goal,
                items=[_HistoryItem(e.nl_summary.replace("Action: ", ""), e.range) for e in g.events]
            ) for g in prev_summaries],
            new_items=[_HistoryItem(new_item.nl_summary.replace("Action: ", ""), new_item.range)
                       for new_item in new_items],
            lvl=1
        )
        return [
            GoalBasedSummary(
                events=all_events[start:end],
                explicit_goal=summary
            ) for start, end, summary in new_groups
        ]

    # Stateless
    def _merge_new_scene(self, prev_summaries: List[EventBasedSummary], new_items: List[SceneGraphInstant]):
        all_scenes = [s for e in prev_summaries for s in e.scenes] + new_items

        new_groups = self._merge_new_items(
            prev_summaries=[_SummaryGroup(
                summary=e.explicit_action,
                items=[_HistoryItem(self._scene_to_text(s), (s.raw.timestamp, s.raw.timestamp))
                       for s in e.scenes]
            ) for e in prev_summaries],
            new_items=[_HistoryItem(self._scene_to_text(new_item), (new_item.raw.timestamp, new_item.raw.timestamp))
                       for new_item in new_items],
            lvl=0
        )
        return [
            EventBasedSummary(
                scenes=all_scenes[start:end],
                explicit_action=summary
            ) for start, end, summary in new_groups
        ]

    def _scene_to_text(self, scene: SceneGraphInstant) -> str:
        return scene.scene_description

    def _hl_item_to_text(self, i: Union[GoalBasedSummary, HigherLevelSummary]):
        return i.forgotten_summary if is_forgotten(i) else i.nl_summary.replace('Goal: ', '')

    def _treat_as_equal(self, node1: AnyTreeNode, node2: AnyTreeNode):
        if (isinstance(node1, GoalBasedSummary) and isinstance(node2, GoalBasedSummary)
                and node1.explicit_goal and node2.explicit_goal
        ):
            # Do not check scene graph since it is hidden to the summary LLM if there is an explicit goal
            return node1.explicit_goal == node2.explicit_goal
        return node1.nl_summary == node2.nl_summary

    # Stateless
    @classmethod
    def _format_prev_and_current_items(cls, prev_summaries: List[_SummaryGroup],
                                       new_items: List[_HistoryItem],
                                       lvl: int,
                                       reduce_old_item_details_to_characters: int = None
                                       ) -> Tuple[str, str, dict[Tuple[int, int], str], int]:
        prev_scenes_str = ''
        existing_groups = {}
        max_idx = sum(len(s.items) for s in prev_summaries) + len(new_items) - 1  # -1 because of 0-based indexing
        i = max_idx
        prev_date = None
        for s in prev_summaries:
            assert isinstance(s, _SummaryGroup)
            assert len(s.items) > 0
            prev_scenes_str += f'# ({i} - {i - len(s.items) + 1}) {s.summary}\n'
            for e in s.items:
                assert isinstance(e, _HistoryItem)
                text = e.text[:reduce_old_item_details_to_characters]  # None works fine in slice
                prev_scenes_str += (f'- {i}: {format_rel_date(prev_date, e.range[0])} - '
                                    f'{format_rel_date(e.range[0], e.range[1])}: {text}\n')
                prev_date = e.range[1]
                i -= 1
            existing_groups[i + len(s.items), i + 1] = s.summary
        if not prev_scenes_str:
            prev_scenes_str = 'No previous items.'

        current_scene_str = '\n'.join(f'- {len(new_items) - i - 1}: '
                                      f'{format_rel_date(prev_date, new_item.range[0])} '
                                      f'- {format_rel_date(new_item.range[0], new_item.range[1])}'
                                      f': {new_item.text}'
                                      for i, new_item in enumerate(new_items))
        return prev_scenes_str, current_scene_str, existing_groups, max_idx

    # Stateless
    def _merge_new_items(self, prev_summaries: List[_SummaryGroup],
                         new_items: List[_HistoryItem], lvl: int) -> List[Tuple[int, int, str]]:
        initial_item_texts_merged = ', '.join(list(
            first_line(h.text)
            for h in chain((h1 for s in prev_summaries for h1 in s.items), new_items)
        ))
        existing_groups, max_idx, new_items_str = {}, -1, ''

        def _get_chain_params(trial):
            nonlocal existing_groups, max_idx, new_items_str
            prev_items_str, new_items_str, existing_groups, max_idx = self._format_prev_and_current_items(
                prev_summaries, new_items, lvl, self._reduce_old_items_characters_for_trial(trial))
            return {
                'prev_scenes': prev_items_str,
                'current_scenes': new_items_str,
                'example_selection_input': initial_item_texts_merged
            }

        trial_idx, parsed_result = 0, None
        try:
            result = invoke_chain_with_adaptive_length_content(self._receive_item_chains[lvl], _get_chain_params,
                                                               self._max_retry_reduce_length_attempts)
            while trial_idx < self._max_retry_attempts:
                parsed_result, errors = self._parse_regroup_output(result, max_idx, num_new_items=len(new_items))
                if errors:
                    result = invoke_chain_with_adaptive_length_content(
                        self._retry_receive_item_chains[lvl],
                        lambda trial: {
                            **_get_chain_params(trial),
                            'errors': '\n'.join(f' - {e}' for e in errors[:max(5, int(len(errors) * 0.9 ** trial))]),
                            'wrong_output': json.dumps(result)
                        }, self._max_retry_reduce_length_attempts)
                else:
                    break
                trial_idx += 1
        except Exception as e:
            print('Failed to merge item!', e)
            traceback.print_exc()

        if parsed_result is None:
            print('Grouping LLM did not provide valid output! Will start new group.')
            parsed_result = {
                (len(new_items) - 1, 0):
                    (self._simple_summarize_chains[lvl].invoke({'input': new_items_str})
                     if len(new_items) > 1
                     else new_items[0].text)
            }

        resulting_mapping = self._merge_group_definitions(existing_groups, parsed_result)
        for ((old_start, old_end), old_summary), ((new_start, new_end), new_summary) in zip(
                sorted(existing_groups.items(), reverse=True), sorted(resulting_mapping.items(), reverse=True)):
            if old_start == new_start and old_end != new_end and old_summary == new_summary:
                # Previous range changed, but LLM did not adjust summary => use simple summary LLM
                #  Initially tried to feed back this as an error, but this does not work well
                def _get_children_str(reduce_chars):
                    return '\n'.join(
                        [f'- {h.text[:reduce_chars]}' for s in prev_summaries for h in s.items]
                        [max_idx - new_start: max_idx - new_end + 1]
                    )

                resulting_mapping[new_start, new_end] = self._simple_summarize_with_adaptive_length(
                    _get_children_str, lvl)

        return sorted([
            (max_idx - r_high, max_idx - r_low + 1, summary)
            for (r_high, r_low), summary in resulting_mapping.items()
        ])

    def _adaptive_format_date_range(self, prev_date: datetime,
                                    date_range: Tuple[datetime, datetime],
                                    reduce_chars: Optional[int],
                                    lvl: int) -> str:
        if reduce_chars is not None:
            if reduce_chars <= self._reduce_chars_remove_date_threshold_2:
                if prev_date is not None and (date_range[0] - prev_date).total_seconds() < 30:
                    return '- '
                else:
                    return f'- {format_rel_date(prev_date, date_range[0])}: '
            elif reduce_chars <= self._reduce_chars_remove_date_threshold:
                return f'- {format_rel_date(prev_date, date_range[0])}: '
        return (f'- {format_rel_date(prev_date, date_range[0])} - '
                f'{format_rel_date(date_range[0], date_range[1])}: ')

    def _simple_summarize_with_adaptive_length(self, get_children_str: Callable[[int], str], lvl: int):
        return invoke_chain_with_adaptive_length_content(
            self._simple_summarize_chains[lvl],
            lambda trial: {
                'input': get_children_str(self._reduce_old_items_characters_for_trial(trial))
            },
            self._max_retry_reduce_length_attempts)

    def _reduce_old_items_characters_for_trial(self, trial: int):
        if trial == 0 and self._reduce_old_item_details_to_characters is None:
            return None
        reduce_chars_base = self._reduce_old_item_details_to_characters or 200
        return int(reduce_chars_base * (0.75 ** trial))

    @staticmethod
    def _merge_group_definitions(existing_groups: Dict[Tuple[int, int], str],
                                 modified_items: Dict[Tuple[int, int], str]) -> Dict[Tuple[int, int], str]:
        # Trick: Flatten list, with appended index to each of the summaries (so that same summary from different
        #  entries do not get merged). Then apply changes, group by subsequent same summary, remove appended indices.
        existing_groups = dict(existing_groups)
        modified_items = dict(modified_items)

        for i, (k, v) in enumerate(existing_groups.items()):
            existing_groups[k] = v + f'_old_{i:>5}'
        for i, (k, v) in enumerate(modified_items.items()):
            modified_items[k] = v + f'_new_{i:>5}'

        flattened: List[str] = []
        max_idx = max((start for start, end in chain(existing_groups.keys(), modified_items.keys())), default=0)
        for i in range(max_idx + 1):
            new_group = next((s for r, s in modified_items.items() if r[0] >= i >= r[1]), None)
            if new_group:
                flattened.append(new_group)
            else:
                existing_group = next(s for r, s in existing_groups.items() if r[0] >= i >= r[1])
                flattened.append(existing_group)

        result = {}
        cur_start = max_idx
        for i, summary in reversed(list(enumerate(flattened))):
            if i < max_idx and summary != flattened[i + 1]:
                result[cur_start, i + 1] = flattened[i + 1]
                cur_start = i
        result[cur_start, 0] = flattened[0]
        return {k: v[:-len(f'_old_{0:>5}')] for k, v in result.items()}

    @staticmethod
    def _parse_regroup_output(result: dict, max_idx: int, num_new_items: int = 1) -> Tuple[Optional[dict], List[str]]:
        if not isinstance(result, dict):
            return None, ['Output should be a dict']
        parsed_result = {}
        errors = []
        for key, value in result.items():
            match = re.fullmatch(r'(\d+)(?:\s*-\s*(\d+))?', key)
            if not match:
                errors.append(f'"{key}" does not match pattern "x-y" with ints x, y.')
                continue
            if not isinstance(value, str):
                errors.append(f'value of "{key}" should be str, but is {type(value)}')
                continue
            start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))
            else:
                end = start
            parsed_result[start, end] = value
            if start < end:
                errors.append(f'"{key}": start < end. Indices should be switched?')
                continue
            if start > max_idx:
                errors.append(f'"{key}": start is > the total number of items ({max_idx}).')
                continue

        for i in range(max_idx + 1):  # max_idx itself is valid and should also be checked
            ranges_including_i = sum(1 if i in range(start, end + 1) else 0
                                     for (end, start) in parsed_result.keys())
            if ranges_including_i == 0 and i < num_new_items:
                errors.append(f'New item (index {i}) is not contained in any range. Make sure some range includes '
                              f'index {i}, or list it as a separate group.')
            elif ranges_including_i > 1:
                errors.append(f'Index {i} is contained in multiple ranges.')

        return None if errors else parsed_result, errors

    @staticmethod
    def _iter_examples_from_static_db(mode: Literal['first_level', 'higher_level'] = 'first_level',
                                      example_db_name: str = 'teach') -> Generator[
        Tuple[List[_HistoryItem], List[Tuple[Tuple[int, int], str]]],
        Any, None
    ]:
        import em.llm_summary
        example_dir = Path(em.llm_summary.__file__).parent / 'config' / example_db_name
        if (example_dir / mode).is_dir():
            example_dir = example_dir / mode
        # noinspection PyProtectedMember
        example_db = list(em.llm_summary._load_example_db(example_dir))
        for sample in example_db:
            input_items = []
            for line in sample['input'].splitlines():
                match = re.match(r'^\d+.\s+([\d: .-]{55}):', line)
                if match:
                    input_items.append(_HistoryItem(line[match.end():].strip(),
                                                    tuple(datetime.fromisoformat(x.strip())
                                                          for x in match.group(1).split(' - '))))
                else:
                    input_items[-1] = _HistoryItem(input_items[-1].text + '\n' + line, input_items[-1].range)
            try:
                output_grouping = json.loads(sample['output'])
            except:
                print(sample['output'])
                raise
            output_grouping = {
                tuple(int(x) for x in group_key.split('-')): summary
                for group_key, summary in output_grouping.items()
            }
            for k, v in list(output_grouping.items()):
                if len(k) == 1:
                    output_grouping[k[0], k[0]] = output_grouping[k]
                    del output_grouping[k]

            # noinspection PyTypeChecker
            groups: List[Tuple[Tuple[int, int], str]] = sorted(output_grouping.items())
            yield input_items, groups

    def construct_simple_examples_from_static_db(self,
                                                 example_db_name: str,
                                                 mode: Literal['first_level', 'higher_level'] = 'first_level',
                                                 input_key_name='input'):
        for input_items, groups in self._iter_examples_from_static_db(mode, example_db_name):
            for (start, end), summary in groups:
                items_str = ', '.join(first_line(item.text).split('Goal:')[-1].strip()
                                      for item in input_items[start:end + 1])
                yield {input_key_name: items_str, 'output': summary}


def _propagate_parent(node: AnyTreeNode, deep=False):
    if type(node) not in type_to_children_property_map:
        return
    for child in _children(node):
        child.parent = node
        if deep:
            _propagate_parent(child, deep)


def shallow_copy_summary(node: Union[HigherLevelSummary, GoalBasedSummary]):
    c = copy(node)
    c.parent = None
    return c


def _remove_recursively(node):
    if node.parent is None:
        return
    children = _children(node.parent)
    children.remove(node)
    if len(children) == 0:
        _remove_recursively(node.parent)
    node.parent = None


def _ensure_consecutive_times(node: AnyTreeNode):
    if isinstance(node, SceneGraphInstant) or is_forgotten(node):
        return
    children = _children(node)
    assert len(children) > 0  # There should be no node without children
    for c1, c2 in zip(children[:-1], children[1:]):
        if hasattr(c1, 'range'):
            assert c1.range[1] < c2.range[0], f'{c1.range}, {c2.range}'
        else:
            assert c1.raw.timestamp <= c2.raw.timestamp, f'{c1.raw.timestamp}, {c2.raw.timestamp}'
        _ensure_consecutive_times(c1)
    _ensure_consecutive_times(children[-1])


def _children(node):
    # Returns a _mutable_ list of children

    if is_forgotten(node):
        return []
    if isinstance(node, GoalBasedSummary):
        # Here we intentionally skip nested goals and directly go to event.
        #  This avoids special treatment of nested goals elsewhere
        #  However, we cannot just use iter_nodes_of_type since modifications to the returned list must persist
        return _children_of_goal(node)

    return getattr(node, type_to_children_property_map[type(node)])


def _range(s: AnyTreeNode):
    return (s.range
            if hasattr(s, 'range')
            else (s.raw.timestamp,) * 2)


def _collect_edge_children(node: AnyTreeNode, num: int):
    if isinstance(node, SceneGraphInstant) or is_forgotten(node):
        return [[]]
    elif isinstance(node, EventBasedSummary):
        return [node.scenes[-num:]]

    edge_children = _children(node)[-num:]

    recursive_edge_children = None
    for c in reversed(edge_children):
        if is_forgotten(c):
            # Do not recurse beyond forgotten parent items to prevent regrouping items across forgotten boundaries
            if recursive_edge_children is None:
                # Add empty lists to ensure correct level (in case all lower-level nodes are forgotten)
                layers_to_add_idx = {
                    EventBasedSummary: 0,  # This forgotten child already corresponds to SceneGraphInstant
                    GoalBasedSummary: 1,  # c corresponds to event => add scene level
                    HigherLevelSummary: 2  # c might correspond to goal or higher => add event, scene level
                }
                recursive_edge_children = [[]] * layers_to_add_idx[type(node)]
            break
        deeper_edge_children = _collect_edge_children(c, num)
        if recursive_edge_children is None:
            recursive_edge_children = deeper_edge_children
        else:
            for level_existing, level_further in zip(recursive_edge_children, deeper_edge_children):
                free_slots = num - len(level_existing)
                if free_slots > 0:
                    level_existing[0:0] = level_further[-free_slots:]
            if all(len(e) == num for e in recursive_edge_children):
                break

    return [edge_children] + (recursive_edge_children or [])


# prevent unnecessary summary levels but ensure a consistently balanced tree
def _simplify_ensuring_balanced_tree(node: HigherLevelSummary):
    if not all(isinstance(c, HigherLevelSummary) for c in node.children):
        return node

    if len(node.children) == 1:
        return node.children[0]

    if all(len(c.children) == 1
           and (isinstance(c.children[0], HigherLevelSummary) or is_forgotten(c.children[0]))
           for c in node.children):
        node.children = [c if is_forgotten(c.children[0])  # ok to have unbalanced forgotten children nodes
                         else c.children[0]
                         for c in node.children]
        _propagate_parent(node)
        _simplify_ensuring_balanced_tree(node)

    return node


def _children_of_goal(goal: GoalBasedSummary):
    """
    This function produces a list of all events deeply contained in the given goal.
    The list is mutable and propagates back to the original parents, even if the given goal has nested sub-goals.
    """
    children_lists = []
    events_start_idx = None
    for i, c in enumerate(goal.events):
        if (isinstance(c, EventBasedSummary) or is_forgotten(c)) and events_start_idx is None:
            events_start_idx = i
        if isinstance(c, GoalBasedSummary):
            if events_start_idx is not None:
                children_lists.append(SliceListView(goal.events, events_start_idx, i))
                events_start_idx = None
            children_lists.append(_children_of_goal(c))
    if events_start_idx is not None:
        children_lists.append(SliceListView(goal.events, events_start_idx, len(goal.events)))
    return ConcatenatedListView(*children_lists)


_log_writer = ThreadPoolExecutor(max_workers=1, thread_name_prefix='log-tree-state-writer-')


def log_tree_state(history: HigherLevelSummary, current_msg: str, tree_state_log,
                   expand_types=(HigherLevelSummary,)):
    def prep_node(n):
        setattr(n, '_simplified_repr', True)
        setattr(n, '_use_idx_prefix', False)
        setattr(n, '_display_final', True)
        n._set_expanded(isinstance(n._wrapped, expand_types))

    from llm_emv.emv_api import make_tree_interactive
    import llm_emv.interactive_tree
    t = make_tree_interactive(history)
    llm_emv.interactive_tree.recursive_apply(t, prep_node)
    tree_repr = repr(t)

    def _print(r, m, log):
        print('\n\n=== Tree Update ===', file=log)
        print('=> Next item:', m, file=log)
        print('=> Tree:\n', file=log)
        print(r, file=log)
        print('End Tree', file=log)

    _log_writer.submit(_print, tree_repr, current_msg, tree_state_log)
