import argparse
import ast
import pickle
import re
from datetime import datetime
from pathlib import Path
from typing import Union, List, Literal, Tuple, Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import SystemMessagePromptTemplate as SystemMsg, HumanMessagePromptTemplate as HumanMsg, \
    FewShotChatMessagePromptTemplate, AIMessagePromptTemplate, MessagesPlaceholder

from .organize.forget import is_forgotten
from .armarx_lt_mem import create_summarize_parameters_chain
from .em_tree import SceneGraphInstant, HigherLevelSummary, EventBasedSummary, GoalBasedSummary, iter_nodes_of_type
from .incremental_history import IncrementalHistoryBuilder, log_tree_state, shallow_copy_summary, _SummaryGroup, \
    _HistoryItem
from .rule_based_summary import select_keyframe_indices, build_event_summaries_with_indices, \
    build_goals_from_hierarchical_goal_items


class ArmarXMemoryIncrementalTreeBuilder(IncrementalHistoryBuilder):
    """
    Incremental tree building for ArmarX data.
    This class does _not_ handle:
     - the actual loading of data from ArmarX
     - the merging of multimodal asynchronous events into scene graph instant. It assumes to receive
       ready-built "full" scene graphs and just performs the grouping to events/goals.
    """

    def __init__(self, llm: Union[BaseChatModel, List[BaseChatModel]],
                 context_window=3, finalize_llm=None,
                 retry_llm=None, fix_json_llm=None,
                 action_param_summarizer_llm=None,
                 relevance_language_rule_file_path: Path = None,
                 reduce_old_item_details_to_characters=None):
        levels: List[Literal['first_level', 'higher_level']] = ['first_level', 'higher_level']
        few_shot_templates = {
            level: FewShotChatMessagePromptTemplate(
                input_variables=[],
                examples=list(self.construct_simple_examples_from_static_db(
                    mode=level,
                    example_db_name='armarx_lt_mem_inc'
                )),
                example_prompt=(
                        HumanMsg.from_template('{input}')
                        + AIMessagePromptTemplate.from_template("{output}")))
            for level in levels
        }

        receive_item_prompts = [(
                SystemMsg.from_template(
                    'You are given a list of grouped goals pursued by the humanoid robot ARMAR-7, and a description of '
                    'the current goals. Group the previous goals with the new ones into semantic steps or '
                    'subtasks. Consider whether the current goals belong to the same step/subtask or starts '
                    'something new. Also consider the dates/times, do not merge items that are too far. '
                    'Do not repeat the summaries of the previous groups, each group should be distinct. '
                    'Groups should be specific, avoid too general terms like "kitchen activities", rather use concrete '
                    'steps/subtasks such as "wipe the table", "bring milk and chocolate to the human" etc.'
                )
                + HumanMsg.from_template('The previous goals are already grouped and provided as a list:\n'
                                         '# (range) summary 1\n'
                                         '- n: item 1.1\n'
                                         '- n-1: item 1.2\n'
                                         '# (range) summary 2\n'
                                         '- n-2: item 2.1\n'
                                         '...\n\n'
                                         'Examples:')
                + few_shot_templates['first_level' if i < 3 else 'higher_level']
                + HumanMsg.from_template('Your task:\n\n'
                                         'Previous goals:\n{prev_scenes}')
                + HumanMsg.from_template('Current:\n {current_scenes}')
                + HumanMsg.from_template('Decide how to group the current goals with the previous ones. '
                                         'Produce a JSON map of "item range": "short summary" for the items that should'
                                         ' be modified. E.g. {"4-0": "..."} to merge the newest item (0) into the '
                                         'existing group, or {"0": "..."} if the newest item (0) starts a new '
                                         'group, or {"5-3": "...", "2-0": "..."} to re-group some items (2 and 1) '
                                         'together with the newest one (0). When modifying existing groups, make sure '
                                         'to properly adjust the summary to match only the items that '
                                         'are now in that group. '
                                         'Merge previous groups that represent the same step/subtask. '
                                         'Groups should be no larger than a handful of items, '
                                         'each group should focus on a single subtask. '
                                         'The summaries should be concise and focus on the main activity/observation of'
                                         ' the humanoid robot. Use first-person perspective of the robot.',
                                         template_format='jinja2')
                + MessagesPlaceholder("relevance_rule_msg", optional=True)
                + HumanMsg.from_template('Answer like this:\nReasoning: ...\nJSON: ...')
        ) for i in range(4)]  # idx 0, 1 is actually unused (simple_summary overwritten below). 2 is goal->HL, 3 is HL+
        simple_summary_prompts = [(
                SystemMsg.from_template('You are given a list of goals pursued by the humanoid robot ARMAR-7. '
                                        'Your task is to provide a concise and objective '
                                        'one-sentence summary using first-person perspective. '
                                        + ('Make sure to consider the dates/times of the items if there are large '
                                           'gaps. Mention the timing briefly, not too specific. ' if i >= 3 else ''
                                           ) +
                                        'Examples:')
                + few_shot_templates['first_level' if i < 3 else 'higher_level']
                + MessagesPlaceholder("relevance_rule_msg", optional=True)
                + HumanMsg.from_template("{input}")
        ) for i in range(4)]
        super().__init__(llm, context_window, finalize_llm, retry_llm, fix_json_llm, receive_item_prompts,
                         simple_summary_prompts, relevance_language_rule_file_path,
                         reduce_old_item_details_to_characters)
        self._action_summarize_cache = {}
        if action_param_summarizer_llm:
            self.action_param_summarize_chain = create_summarize_parameters_chain(action_param_summarizer_llm)
        else:
            self.action_param_summarize_chain = None

    def _summarize_action_params(self, events: List[EventBasedSummary]):
        if self.action_param_summarize_chain is None:
            return

        new_summary_events = []
        for e in events:
            params = e.latest_raw.current_action_parameters
            if e.latest_raw.current_action and params:
                key = str(params)
                if key in self._action_summarize_cache:
                    e.action_parameter_summary = self._action_summarize_cache[key]
                else:
                    new_summary_events.append(e)

        summaries = self.action_param_summarize_chain.batch(new_summary_events)
        for e, s in zip(new_summary_events, summaries):
            s = s.strip('-')
            e.action_parameter_summary = s
            key = str(e.latest_raw.current_action_parameters)
            self._action_summarize_cache[key] = s

    def _batch_scenes(self, scenes: List[SceneGraphInstant], batch_size_hint: int):
        """
        Do smart batching to avoid splitting up scenes that would not produce any keyframe
        (i.e. if nothing changes and the robot is just standing around)
        """
        keyframe_indices = select_keyframe_indices(scenes)
        events = build_event_summaries_with_indices(scenes, keyframe_indices)
        for i in range(0, len(events), batch_size_hint):
            yield [
                scene
                for evt in events[i:i + batch_size_hint]
                for scene in iter_nodes_of_type(evt, SceneGraphInstant)
            ]

    def _merge_new_scene(self, prev_summaries: List[EventBasedSummary], new_items: List[SceneGraphInstant]):
        all_scenes = [s for e in prev_summaries for s in e.scenes] + new_items
        indices = select_keyframe_indices(all_scenes)
        events = build_event_summaries_with_indices(all_scenes, indices)
        self._summarize_action_params(events)
        return events

    def _merge_new_event(self, prev_summaries: List[GoalBasedSummary], new_items: List[EventBasedSummary]):
        idx_with_forgotten = None
        for i in reversed(range(len(prev_summaries))):
            if any(is_forgotten(e) for e in prev_summaries[i].events):
                idx_with_forgotten = i
                break
        if idx_with_forgotten is None:
            hidden_parents = []
            visible_parents = prev_summaries
        else:
            hidden_parents = prev_summaries[:idx_with_forgotten + 1]
            visible_parents = prev_summaries[idx_with_forgotten + 1:]
        all_events = [e for g in visible_parents for e in iter_nodes_of_type(g, EventBasedSummary)] + new_items
        goals = build_goals_from_hierarchical_goal_items(all_events)
        # Propagate the top-level parent to all contained events,
        #  as the incremental history builder views the nested goals as one single layer
        for g in goals:
            for e in iter_nodes_of_type(g, EventBasedSummary):
                e.parent = g
        return [shallow_copy_summary(p) for p in hidden_parents] + goals

    def _merge_new_goal(self, prev_summaries: List[HigherLevelSummary], new_items: List[GoalBasedSummary]):
        if len(new_items) == 1 and len((new_items[0].latest_raw.current_goal or '').split('.')) > 1:
            simple_goal = new_items[0].nl_summary.splitlines()[0][len('Goal: '):]
            prev_summaries_flat_copy = [
                shallow_copy_summary(h)
                for h in prev_summaries
            ]
            return prev_summaries_flat_copy + [
                self._simple_summarize_items(new_items, lvl=2)
                if new_items[0].speech_events
                else HigherLevelSummary(simple_goal, new_items)
            ]
        last_forgotten_idx = max(
            (i for i, p in enumerate(prev_summaries) if any(is_forgotten(c) for c in p.children)),
            default=None)
        if last_forgotten_idx is not None:
            hidden_result = [shallow_copy_summary(p) for p in prev_summaries[:last_forgotten_idx + 1]]
            visible_result = super()._merge_new_goal(prev_summaries[last_forgotten_idx + 1:], new_items)
            return hidden_result + visible_result
        else:
            return super()._merge_new_goal(prev_summaries, new_items)

    def _adaptive_format_date_range(self, prev_date: datetime, date_range: Tuple[datetime, datetime],
                                    reduce_chars: Optional[int], lvl: int) -> str:
        return _hide_seconds_for_higher_lvl(super()._adaptive_format_date_range(
            prev_date, date_range, reduce_chars, lvl), lvl)

    @classmethod
    def _format_prev_and_current_items(cls, prev_summaries: List[_SummaryGroup], new_items: List[_HistoryItem],
                                       lvl: int, reduce_old_item_details_to_characters: int = None
                                       ) -> tuple[str, str, dict[tuple[int, int], str], int]:
        prev_scenes_str, current_scene_str, existing_groups, max_idx = super()._format_prev_and_current_items(
            prev_summaries, new_items, lvl, reduce_old_item_details_to_characters)
        prev_scenes_str = _hide_seconds_for_higher_lvl(prev_scenes_str, lvl)
        current_scene_str = _hide_seconds_for_higher_lvl(current_scene_str, lvl)
        return prev_scenes_str, current_scene_str, existing_groups, max_idx

    def _finalize(self, item, lvl: int):
        # Do not change predefined event/goal labels, but transfer to explicit state (if raw data is forgotten)
        if lvl == 0:  # Scene->Event
            if isinstance(item, EventBasedSummary) and item.explicit_action is None:
                item.explicit_action = item.latest_raw.current_action
            return item
        elif lvl == 1:  # Event->Goal
            if isinstance(item, GoalBasedSummary) and item.explicit_goal is None:
                item.explicit_goal = item.latest_raw.current_goal
            return item
        else:
            return super()._finalize(item, lvl)


def _hide_seconds_for_higher_lvl(str_with_times: str, lvl: int):
    if lvl > 2:
        return re.sub(r'(\d{2}:\d{2}):\d{2}', r'\1', str_with_times)
    return str_with_times


class FlatArmarXIncrementalTreeBuilder(ArmarXMemoryIncrementalTreeBuilder):

    def __init__(self):
        from langchain_core.language_models import FakeListChatModel
        super().__init__(FakeListChatModel(responses=['']))

    def _merge_new_goal(self, prev_summaries: List[HigherLevelSummary], new_items: List[GoalBasedSummary]):
        return [
            HigherLevelSummary('', [g for s in prev_summaries for g in s.children] + new_items)
        ]

    def _merge_new_summary(self, prev_summaries: List[HigherLevelSummary], new_items: List[HigherLevelSummary],
                           lvl: int):
        all_summaries = [h for s in prev_summaries for h in s.children] + new_items
        return all_summaries

    def _finalize(self, item, lvl: int):
        if lvl <= 1:
            return super()._finalize(item, lvl)
        else:
            return item

    def _simple_summarize_items(self, items: List[Union[GoalBasedSummary, HigherLevelSummary]], lvl: int):
        if all(isinstance(i, GoalBasedSummary) or is_forgotten(i) for i in items):
            return HigherLevelSummary('', items)
        elif all(isinstance(i, HigherLevelSummary) or is_forgotten(i) for i in items):
            return HigherLevelSummary('', [g for s in items for g in s.children])
        else:
            raise AssertionError(items)


def test():
    parser = argparse.ArgumentParser()
    parser.add_argument('--llm', type=ast.literal_eval, default=dict(type='ChatOpenAI'))
    parser.add_argument('input_file', type=Path,
                        help='Can be one pickle file with state failure state dict, '
                             'or one pickle files with history, '
                             'or one armarx memory directory where to load history from.')
    args = parser.parse_args()

    if args.llm == 'fake':
        from langchain_community.chat_models import FakeListChatModel
        llm = FakeListChatModel(responses=['{"0": "I performed a task."}'])
        finalize_llm = FakeListChatModel(responses=['I performed some tasks.'])
        action_llm = FakeListChatModel(responses=['-'])
    else:
        import langchain.globals
        from langchain_community.cache import SQLiteCache
        langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))
        langchain.globals.set_debug(True)
        from lmp.setup import instantiate_llm
        # noinspection PyTypeChecker
        llm: BaseChatModel = instantiate_llm(args.llm)
        action_llm = finalize_llm = llm
    builder = ArmarXMemoryIncrementalTreeBuilder(
        llm, finalize_llm=finalize_llm, action_param_summarizer_llm=action_llm
    )

    input_file = Path(args.input_file)
    if input_file.is_dir():
        from .armarx_lt_mem import load_episode_from_armarx_lt_mem
        ep = load_episode_from_armarx_lt_mem(input_file)
        scene_iter = iter_nodes_of_type(ep, SceneGraphInstant)
    else:
        data = pickle.loads(input_file.read_bytes())
        if isinstance(data, dict):
            # Resume from failure mode
            builder._tree = pickle.loads(data['prev_state'])
            scene_iter = [data['scene']]
            print('Resuming scene', scene_iter)
        else:
            scene_iter = iter_nodes_of_type(data, SceneGraphInstant)

    with Path('tree-states.log').open('w') as log:
        for scene in scene_iter:
            if isinstance(scene, list):
                name = str(scene[-1].raw.timestamp)
                print('Processing', name)
                for history in builder.process_batch(scene):
                    print('Got', history.range)
            else:
                name = str(scene.raw.timestamp)
                print('Processing', name)
                history = builder.process(scene)
            log_tree_state(history, name, log, (HigherLevelSummary, GoalBasedSummary))
    Path('final-tree.pkl').write_bytes(pickle.dumps(history))


if __name__ == '__main__':
    test()
