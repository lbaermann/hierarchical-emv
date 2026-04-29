import argparse
import ast
import json
import pickle
from itertools import chain
from pathlib import Path
from typing import Union, List, Literal

import tiktoken
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import SystemMessagePromptTemplate as SystemMsg, HumanMessagePromptTemplate as HumanMsg, \
    FewShotChatMessagePromptTemplate, AIMessagePromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import InMemoryVectorStore

from em.organize.forget import is_forgotten
from em.randomize_episodes import gen_random_date_from_seed
from em.teach import load_teach_episode
from lmp.setup import instantiate_llm
from .em_tree import EventBasedSummary, SceneGraphInstant, GoalBasedSummary, HigherLevelSummary, iter_nodes_of_type
from .incremental_history import IncrementalHistoryBuilder, log_tree_state, shallow_copy_summary
from .rule_based_summary import select_keyframe_indices, build_event_summaries_with_indices, \
    build_goal_summaries_with_indices


#  effectively makes no difference to offline tree building and then iterating goal children...
#  =>
#   1. build tree offline
#   2. iterate goal nodes
#   3. incrementally refine HL (recursive) summaries from goal nodes
#   open question: extra signal for episode end? probably not... (offline) llm_summary had forced boundaries.
#   however, should be easy to get from time


class TeachIncrementalHistoryBuilder(IncrementalHistoryBuilder):

    def __init__(self, llm: Union[BaseChatModel, List[BaseChatModel]], max_summary_context=100,
                 finalize_llm=None, retry_llm=None, fix_json_llm=None,
                 similarity_model: str = 'sentence-transformers/all-MiniLM-l6-v2',
                 few_shot_k=2,
                 similarity_model_device=None,
                 simple_few_shot_mode=True,
                 relevance_language_rule_file_path: Path = None,
                 ):
        if not simple_few_shot_mode:
            self._reduce_old_item_details_to_characters = 50  # inside few-shot examples

        receive_item_prompts = [(
                SystemMsg.from_template(
                    'You are given a list of grouped goals/actions pursued by a humanoid robot, and a '
                    'description of the current actions. Group the previous actions with the new ones into steps or '
                    'subtasks. Consider whether the current actions belong to the same step/subtask or starts '
                    'something new. Also consider the dates/times, do not merge items that are too far. '
                    'Do not repeat the summaries of the previous groups, each group should be distinct. '
                    'Groups should be specific, avoid too general terms like "kitchen activities", rather use concrete '
                    'steps/subtasks such as "clean the bowl", "cut the onion and put the slices on the plate" etc.'
                )
                + HumanMsg.from_template('The previous actions are already grouped and provided as a list:\n'
                                         '# (range) summary 1\n'
                                         '- n: item 1.1\n'
                                         '- n-1: item 1.2\n'
                                         '# (range) summary 2\n'
                                         '- n-2: item 2.1\n'
                                         '...\n')
                + (
                    self._create_simple_few_shot_prompt(similarity_model, few_shot_k, similarity_model_device,
                                                        mode='first_level' if i < 3 else 'higher_level')
                    if simple_few_shot_mode else
                    self._create_incremental_few_shot_prompt(similarity_model, few_shot_k, similarity_model_device,
                                                             mode='first_level' if i < 3 else 'higher_level')
                )
                + HumanMsg.from_template('Previous actions:\n{prev_scenes}')
                + HumanMsg.from_template('Current:\n {current_scenes}')
                + HumanMsg.from_template('Decide how to group the current actions with the previous ones. '
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
                SystemMsg.from_template('You are given a list of goals pursued by a humanoid robot. '
                                        'Your task is to provide a concise and objective '
                                        'one-sentence summary using first-person perspective. '
                                        + ('Make sure to consider the dates/times of the items if there are large '
                                           'gaps. Mention the timing briefly, not too specific. ' if i >= 3 else ''
                                           ) +
                                        'Examples:')
                + FewShotChatMessagePromptTemplate(input_variables=['input'],
                                                   examples=list(self.construct_simple_examples_from_static_db(
                                                       mode='first_level' if i < 3 else 'higher_level',
                                                       example_db_name='teach'
                                                   )),
                                                   example_prompt=(
                                                           HumanMsg.from_template('{input}')
                                                           + AIMessagePromptTemplate.from_template("{output}")))
                + MessagesPlaceholder("relevance_rule_msg", optional=True)
                + HumanMsg.from_template("{input}")
        ) for i in range(4)]

        super().__init__(llm, max_summary_context,
                         finalize_llm, retry_llm, fix_json_llm,
                         receive_item_prompts, simple_summary_prompts, relevance_language_rule_file_path,
                         reduce_old_item_details_to_characters=200)

    def _prepare_relevance_rule_msg(self):
        from langchain_core.messages import HumanMessage
        msgs = super()._prepare_relevance_rule_msg()
        if msgs:
            msgs.append(HumanMessage('For summarization, these rules provide additional guidance, however, each '
                                     'summary\'s main focus should be on the activities/events that '
                                     'actually happened during this time.'))
        return msgs

    def _create_incremental_few_shot_prompt(
            self, similarity_model: str = 'sentence-transformers/all-MiniLM-l6-v2', few_shot_k=2,
            similarity_model_device=None,
            mode: Literal['first_level', 'higher_level'] = 'first_level'
    ):
        embeddings = HuggingFaceEmbeddings(
            model_name=similarity_model,
            model_kwargs=dict(device=similarity_model_device)
        )
        example_db = list(self.construct_incremental_examples_from_static_db(mode))
        print('Loaded', len(example_db), 'examples')
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples=example_db,
            input_keys=['prev_scenes', 'current_scene'],
            embeddings=embeddings,
            k=few_shot_k,
            vectorstore_cls=InMemoryVectorStore,
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            input_variables=['prev_scenes', 'current_scene'],
            example_selector=example_selector,
            example_prompt=(
                    HumanMsg.from_template('Previous actions:\n{prev_scenes}')
                    + HumanMsg.from_template('Current:\n- 0: {current_scene}')
                    + AIMessagePromptTemplate.from_template("JSON: {output}")
            ),
        )
        return HumanMsg.from_template('Examples:') + few_shot_prompt

    def _create_simple_few_shot_prompt(
            self, similarity_model: str = 'sentence-transformers/all-MiniLM-l6-v2', few_shot_k=2,
            similarity_model_device=None,
            mode: Literal['first_level', 'higher_level'] = 'first_level',
    ):
        embeddings = HuggingFaceEmbeddings(
            model_name=similarity_model,
            model_kwargs=dict(device=similarity_model_device)
        )
        example_db = list(self.construct_simple_examples_from_static_db(mode=mode,
                                                                        input_key_name='example_selection_input',
                                                                        example_db_name='teach'))
        print('Loaded', len(example_db), 'examples')
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples=example_db,
            input_keys=['example_selection_input'],
            embeddings=embeddings,
            k=few_shot_k,
            vectorstore_cls=InMemoryVectorStore,
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            input_variables=['example_selection_input'],
            example_selector=example_selector,
            example_prompt=(
                    HumanMsg.from_template('Items:\n{example_selection_input}')
                    + AIMessagePromptTemplate.from_template("Summary: {output}")
            ),
        )
        return HumanMsg.from_template('The following examples show how groups and their summaries should look like. '
                                      'Consider the semantics and length of these examples.') + few_shot_prompt

    def _finalize(self, item, lvl: int):
        # Do not change predefined event/goal labels, but transfer to explicit state (if raw data is forgotten)
        if lvl == 0:  # Scene->Event
            item.explicit_action = item.latest_raw.current_action
            return item
        elif lvl == 1:  # Event->Goal
            item.explicit_goal = item.latest_raw.current_goal
            return item
        else:
            return super()._finalize(item, lvl)

    def _merge_new_scene(self, prev_summaries: List[EventBasedSummary], new_items: List[SceneGraphInstant]):
        all_scenes = [s for e in prev_summaries for s in e.scenes] + new_items
        indices = select_keyframe_indices(all_scenes)
        return build_event_summaries_with_indices(all_scenes, indices)

    def _merge_new_event(self, prev_summaries: List[GoalBasedSummary], new_items: List[EventBasedSummary]):
        all_events = [e for g in prev_summaries for e in g.events] + new_items
        goal_indices = [i for i, event in enumerate(all_events)
                        if self.is_action_event(event.latest_raw)]
        return build_goal_summaries_with_indices(all_events, goal_indices)

    def _merge_new_goal(self, prev_summaries: List[HigherLevelSummary], new_items: List[GoalBasedSummary]):
        if len(new_items) == 1 and not self.is_action_event(new_items[0].latest_raw):
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
        return super()._merge_new_goal(prev_summaries, new_items)

    @staticmethod
    def is_action_event(latest_raw):
        return (latest_raw.current_action_state == 'success'
                and '(' in latest_raw.current_action
                and latest_raw.current_action[latest_raw.current_action.index('(') + 1] != ')'
                and not latest_raw.current_action.startswith('Say'))

    def construct_incremental_examples_from_static_db(self,
                                                      mode: Literal[
                                                          'first_level', 'higher_level'] = 'first_level',
                                                      example_db_name='teach',
                                                      prev_groups_limit=3):
        from .incremental_history import _SummaryGroup
        for input_items, groups in self._iter_examples_from_static_db(mode, example_db_name):
            for i in range(len(groups)):
                # Group last item to its group and provide correct summary
                (cur_start, cur_end), cur_summary = groups[i]
                cur_constructed_summary = ', '.join(item.text.splitlines()[0].split('Goal:')[-1].strip()
                                                    for item in input_items[cur_start: cur_end])
                current_item = input_items[cur_end]
                prev_groups = [
                                  _SummaryGroup(summary, input_items[start:end + 1])
                                  for (start, end), summary in groups[max(0, i - prev_groups_limit + 1):i]
                              ] + [_SummaryGroup(cur_constructed_summary, input_items[cur_start: cur_end])]
                prev_scenes_str, current_scene_str, _, _ = self._format_prev_and_current_items(
                    prev_groups, [current_item], 2 if mode == 'first_level' else 3)
                yield dict(prev_scenes=prev_scenes_str,
                           current_scene=current_scene_str,
                           output=json.dumps({f"{cur_end - cur_start}-0": cur_summary}))

                # Group first new item separately with trivial summary
                if i + 1 < len(groups):
                    prev_groups[-1] = _SummaryGroup(cur_summary, input_items[cur_start:cur_end + 1])
                    current_item = input_items[cur_end + 1]
                    prev_scenes_str, current_scene_str, _, _ = self._format_prev_and_current_items(
                        prev_groups, [current_item], 2 if mode == 'first_level' else 3)
                    yield dict(prev_scenes=prev_scenes_str, current_scene=current_scene_str,
                               output=json.dumps({"0": current_item.text.splitlines()[0].split('Goal:')[-1].strip()}))


class FlatTeachIncrementalHistoryBuilder(TeachIncrementalHistoryBuilder):

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


def main():
    import langchain.globals
    from langchain_community.cache import SQLiteCache
    langchain.globals.set_debug(True)
    langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache-teach-tree.db"))

    parser = argparse.ArgumentParser()
    parser.add_argument('--llm', type=ast.literal_eval, default=dict(type='ChatOpenAI'))
    parser.add_argument('--max-summary-context', type=int, default=5)
    parser.add_argument('--tree-state-log', type=Path, default=None)
    parser.add_argument('--resume-from-failure', default=False, action='store_true')
    parser.add_argument('game_files', type=Path, nargs='+')
    args = parser.parse_args()

    token_count = 0
    tokenizer = tiktoken.encoding_for_model('gpt-4o-mini')

    def count_tokens(run):
        nonlocal token_count
        for msg in run.inputs['messages'][0]:
            content = msg['kwargs']['content']
            token_count += len(tokenizer.encode(content))

    llm = instantiate_llm(args.llm)
    llm = llm.with_listeners(on_end=count_tokens)
    # noinspection PyTypeChecker
    builder = TeachIncrementalHistoryBuilder(llm, max_summary_context=args.max_summary_context)

    if args.resume_from_failure:
        data = pickle.loads(Path(args.game_files[0]).read_bytes())
        result_history = pickle.loads(data['prev_state'])
        builder._tree = result_history
        scene_iter = [data['scene']]
    else:
        histories: List[HigherLevelSummary] = [
            load_teach_episode(f, start_time=gen_random_date_from_seed(f'{f.stem}_{i}'))
            for i, f in enumerate(args.game_files)]
        histories.sort(key=lambda h: h.range)
        scene_iter = chain(*(iter_nodes_of_type(h, SceneGraphInstant) for h in histories))
        result_history = HigherLevelSummary('', [])

    tree_state_log = None if args.tree_state_log is None else args.tree_state_log.open('w')
    i = 0
    for s in scene_iter:
        prev_state = pickle.dumps(builder._tree)
        try:
            result_history = builder.process(s)
            i += 1
            assert len(list(iter_nodes_of_type(result_history, SceneGraphInstant))) == i  # Sanity check
        except:
            print('Failed at item', i, s)
            Path('failure-state.pkl').write_bytes(pickle.dumps({
                'prev_state': prev_state,
                'scene': s
            }))
            raise
        if tree_state_log:  # and TeachIncrementalHistoryBuilder.is_action_event(s.raw):
            log_tree_state(result_history, s.raw.current_goal, tree_state_log)

    if tree_state_log:
        log_tree_state(result_history, 'Final state', tree_state_log)
        tree_state_log.close()

    print('~Input Token count:', token_count)
    if len(args.game_files) == 1:
        out_name = args.game_files[0].name
    else:
        out_name = '-'.join(f.stem[:8] for f in args.game_files)
    Path(out_name).with_suffix('.incremental.pkl').write_bytes(pickle.dumps(result_history))


if __name__ == '__main__':
    main()
