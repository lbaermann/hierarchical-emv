import argparse
import ast
import hashlib
import json
import pickle
from collections import OrderedDict
from collections.abc import Callable
from datetime import timedelta, datetime
from functools import partial
from itertools import islice, groupby
from pathlib import Path
from random import Random
from typing import List, Tuple, Optional, Dict, TypeVar, Type

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate as HumanMsg, \
    AIMessagePromptTemplate as AIMsg, FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from em.em_tree import GoalBasedSummary, HigherLevelSummary, iter_nodes_of_type, SceneGraphInstant, EventBasedSummary, \
    AnyTreeNode
from em.randomize_episodes import HistoryGenDateTimeSettings, randomize_datetimes
from lmp.setup import instantiate_llm


# Endless sequence generator
def generate_sequences(pkl_files: List[Path],
                       rng: Random,
                       min_seq_len=5, max_seq_len=10,
                       ensure_unique_episodes=False,
                       datetime_settings=HistoryGenDateTimeSettings()):
    histories = [pickle.loads(f.read_bytes()) for f in pkl_files]

    while True:
        seq_len = rng.randint(min_seq_len, max_seq_len)
        if ensure_unique_episodes:
            fn = rng.sample
        else:
            fn = rng.choices
        sampled_indices = fn(range(len(pkl_files)), k=seq_len)

        episodes = [histories[i] for i in sampled_indices]
        files = [pkl_files[i] for i in sampled_indices]
        yield randomize_datetimes(episodes, datetime_settings, rng), files


def _find_distant_similar_actions(history: HigherLevelSummary,
                                  min_question_distance: timedelta,
                                  # Function to reduce a str goal to its equivalence class. Return None to drop
                                  reduce_eq_goal: Callable[[str], str] = lambda g: g
                                  ):
    return _find_distant_similar_items(history, min_question_distance, GoalBasedSummary,
                                       lambda g: reduce_eq_goal(g.explicit_goal) if g.explicit_goal else None)


def _find_distant_equal_asr_events(history: HigherLevelSummary,
                                   min_question_distance: timedelta):
    return _find_distant_similar_items(history, min_question_distance, EventBasedSummary,
                                       lambda e: e.speech_events[0][1] if e.speech_events else None)


_T = TypeVar('_T', bound=AnyTreeNode)


def _find_distant_similar_items(history: HigherLevelSummary,
                                min_question_distance: timedelta,
                                item_type: Type[_T],
                                # Function to reduce a str goal to its equivalence class. Return None to drop
                                reduce_eq: Callable[[_T], str] = lambda g: str(g)
                                ):
    all_items = [x for x in iter_nodes_of_type(history, item_type)]
    all_goals = sorted((x for x in all_items if reduce_eq(x) is not None), key=reduce_eq)
    grouped_items = {
        k: list(vs)
        for k, vs in groupby(all_goals, key=reduce_eq)
        if k is not None
    }
    for item_spec, group in list(grouped_items.items()):
        distances = [x2.range[0] - x1.range[1] for x1, x2 in zip(group[:-1], group[1:])]
        # all([]) is also True, so this applies if len(group) <= 1
        if all(d < min_question_distance for d in distances):
            del grouped_items[item_spec]

    for group in grouped_items.values():
        yield group[0], group[-1]


def _nice_goal_name(evt: EventBasedSummary) -> str:
    goal = evt.latest_raw.current_goal
    if goal is None:
        return 'nothing'
    return (
            goal
            + (f'({evt.action_parameter_summary})' if evt.action_parameter_summary else '')
    )


def _params_from_goal_str(goal: str) -> Dict[str, str]:
    if '(' not in goal:
        return {}
    try:
        parts = goal.split('(')[1].split(')')[0].split(',')
        return {
            p.split('=')[0].strip(): p.split('=')[1].strip()
            for p in parts
        }
    except IndexError:
        print('Failed to parse parameters from str', goal)
        return {}


def _get_robot_location(scene: SceneGraphInstant) -> Optional[str]:
    return _get_location_of_object(scene, 'Armar7')


def _get_location_of_object(scene: SceneGraphInstant, obj: str) -> Optional[str]:
    obj_idx = [i for i, o in enumerate(scene.objects) if obj in o.obj_class]
    if len(obj_idx) != 1:
        return None
    location_idx = [o2 for o1, o2, rel in scene.relations if o1 == obj_idx[0] and rel in ('at', 'on', 'in')]
    if len(location_idx) != 1:
        return None
    return scene.objects[location_idx[0]].obj_class


def _get_objects_at_location(scene: SceneGraphInstant, loc: str) -> List[str]:
    loc_idx = [i for i, o in enumerate(scene.objects) if loc in o.obj_class]
    if len(loc_idx) != 1:
        return []
    obj_indices = [o1 for o1, o2, rel in scene.relations if o2 == loc_idx[0] and rel in ('at', 'on')]
    return [scene.objects[i].obj_class for i in obj_indices]


def _extract_times(r1, r2, episodes, min_question_distance):
    remember_q_min_time = r1.range[1] + min_question_distance
    recall_q_min_time = r2.range[1] + min_question_distance
    if remember_q_min_time > r2.range[1]:
        return None, None
    remember_q_actual_time = _locate_in_episodes(episodes, remember_q_min_time, before=r2.range[0])
    recall_q_actual_time = _locate_in_episodes(episodes, recall_q_min_time)
    return remember_q_actual_time, recall_q_actual_time


def generate_test_cases(episodes):
    t_format = '%Y/%m/%d, %H:%M:%S'
    min_question_distance = timedelta(days=1)
    full_history = HigherLevelSummary('', episodes)

    def _create_sample_impl(qac1, qac2, x1, x2, rem_time, rec_time):
        return _create_sample_from_qac_pair(qac1, qac2, rem_time, rec_time, x1.range, x2.range)

    for g1, g2 in _find_distant_similar_actions(full_history, min_question_distance):
        remember_q_actual_time, recall_q_actual_time = _extract_times(g1, g2, episodes, min_question_distance)
        _create_sample = partial(_create_sample_impl, x1=g1, x2=g2,
                                 rem_time=remember_q_actual_time, rec_time=recall_q_actual_time)

        if remember_q_actual_time is None or recall_q_actual_time is None:  # Sample too short / g2 too late in history
            continue

        nice_g1 = g1.explicit_goal
        nice_g2 = g2.explicit_goal
        yield _create_sample(
            (f"When did you first {nice_g1}?",
             f"At {g1.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {nice_g1}"),
            (f"When did you last {nice_g2}?",
             f"At {g2.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {nice_g2}")
        )

        all_locations_g1 = [_get_robot_location(s) for s in iter_nodes_of_type(g1, SceneGraphInstant)]
        all_locations_g2 = [_get_robot_location(s) for s in iter_nodes_of_type(g1, SceneGraphInstant)]
        if all_locations_g1[0] and all_locations_g2[0]:
            yield _create_sample(
                (f"Where have you been the first time you started to {nice_g1}?",
                 f"At the {all_locations_g1[0]}",
                 f"You should always remember the exact location when you start to {nice_g1}"),
                (f"Where have you been the last time you started to {nice_g2}?",
                 f"At the {all_locations_g2[0]}",
                 f"You should always remember the exact location when you start to {nice_g2}")
            )
        distinct_locations_g1 = set(loc for loc in all_locations_g1 if loc is not None)
        distinct_locations_g2 = set(loc for loc in all_locations_g2 if loc is not None)
        if distinct_locations_g1 and distinct_locations_g2 and max(len(distinct_locations_g1),
                                                                   len(distinct_locations_g2)) > 1:
            yield _create_sample(
                (f"List all locations you visited during the first time you did {nice_g1}?",
                 ', '.join(sorted(distinct_locations_g1)),
                 f"You should remember all the locations you visit while you {nice_g1}"),
                (f"List all locations you visited during the last time you did {nice_g2}?",
                 ', '.join(sorted(distinct_locations_g2)),
                 f"You should remember all the locations you visit while you {nice_g2}"),
            )

        for loc, prep in [('counter', 'on'), ('sink', 'in')]:
            objs_g1 = {o for s in iter_nodes_of_type(g1, SceneGraphInstant) for o in _get_objects_at_location(s, loc)}
            objs_g2 = {o for s in iter_nodes_of_type(g2, SceneGraphInstant) for o in _get_objects_at_location(s, loc)}
            if objs_g1 and objs_g2:
                yield _create_sample(
                    (f"What objects did you see {prep} the {loc} the first time you did {nice_g1}?",
                     ', '.join(sorted(objs_g1)),
                     f"You should remember all the objects you see {prep} the {loc} when you {nice_g1}"),
                    (f"What objects did you see {prep} the {loc} the last time you did {nice_g2}?",
                     ', '.join(sorted(objs_g2)),
                     f"You should remember all the objects you see {prep} the {loc} when you {nice_g2}"),
                )

    # more abstract matches (parameters ignored)
    reduce = lambda g: g.split('(')[0]
    for g1, g2 in _find_distant_similar_actions(full_history, min_question_distance,
                                                reduce_eq_goal=reduce):
        remember_q_actual_time, recall_q_actual_time = _extract_times(g1, g2, episodes, min_question_distance)
        _create_sample = partial(_create_sample_impl, x1=g1, x2=g2,
                                 rem_time=remember_q_actual_time, rec_time=recall_q_actual_time)
        if remember_q_actual_time is None or recall_q_actual_time is None:  # Sample too short / g2 too late in history
            continue

        nice_g1 = reduce(g1.explicit_goal)
        nice_g2 = reduce(g2.explicit_goal)
        yield _create_sample(
            (f"When did you first {nice_g1}?",
             f"At {g1.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {nice_g1}"),
            (f"When did you last {nice_g2}?",
             f"At {g2.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {nice_g2}")
        )

        params_g1 = _params_from_goal_str(g1.explicit_goal)
        params_g2 = _params_from_goal_str(g2.explicit_goal)
        shared_keys = params_g1.keys() & params_g2.keys()
        for k in shared_keys:
            yield _create_sample(
                (f"What value was the parameter {k} when you first did {nice_g1}?",
                 f"{params_g1[k]}",
                 f"You should always remember the value of {k} when you {nice_g1}"),
                (f"What value was the parameter {k} when you last did {nice_g2}?",
                 f"{params_g2[k]}",
                 f"You should always remember the value of {k} when you {nice_g2}")
            )

    min_question_distance = timedelta(hours=4)
    important_objects = ['keys', 'wallet', 'medicine', 'Leonard Baermann', 'Joana Plewnia']
    for obj in important_objects:
        yield from _make_obj_questions([obj], obj, episodes, min_question_distance, t_format)
    obj_categories = {
        'valuable item': ['keys', 'wallet', 'medicine'],
        'person': ['Leonard Baermann', 'Joana Plewnia'],
        'beverage': ['OrangeJuice', 'multivitamin-juice', 'soy-drink', 'soy-milk'],
    }
    for category, objs in obj_categories.items():
        yield from _make_obj_questions(objs, category, episodes, min_question_distance, t_format)

    important_locations = ['dishwasher', 'laundry', 'small-table']
    for loc in important_locations:
        events_at_loc = [
            e for e in iter_nodes_of_type(full_history, EventBasedSummary)
            if loc in (_get_robot_location(e.latest_scene) or '')
        ]
        if len(events_at_loc) == 0:
            continue
        e1, e2 = events_at_loc[0], events_at_loc[-1]
        remember_q_actual_time, recall_q_actual_time = _extract_times(e1, e2, episodes, min_question_distance)
        _create_sample = partial(_create_sample_impl, x1=e1, x2=e2,
                                 rem_time=remember_q_actual_time, rec_time=recall_q_actual_time)
        if remember_q_actual_time is None or recall_q_actual_time is None:
            continue

        yield _create_sample(
            (f"When have you first been at the {loc}?",
             f"At {e1.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you are at the {loc}"),
            (f"When have you last been at the {loc}?",
             f"At {e2.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you are at the {loc}")
        )

    for e1, e2 in _find_distant_equal_asr_events(full_history, min_question_distance):
        remember_q_actual_time, recall_q_actual_time = _extract_times(e1, e2, episodes, min_question_distance)
        _create_sample = partial(_create_sample_impl, x1=e1, x2=e2,
                                 rem_time=remember_q_actual_time, rec_time=recall_q_actual_time)
        if remember_q_actual_time is None or recall_q_actual_time is None:
            continue

        asr1 = e1.speech_events[0][1]
        asr2 = e2.speech_events[0][1]
        if asr1 == 'connecting123' or asr2 == 'connecting123' or e1.range[0].minute % 3 != 0:  # reduce freq of this
            continue
        yield _create_sample(
            (f"When did the user first say '{asr1}' to you?",
             f"At {e1.range[1].strftime(t_format)}",
             f"You should always remember the exact time when the user says '{asr1}'"),
            (f"When did the user last say '{asr2}' to you?",
             f"At {e2.range[1].strftime(t_format)}",
             f"You should always remember the exact time when the user says '{asr2}'")
        )
        yield _create_sample(
            (f"What were you doing the moment the first time you heard the user saying '{asr1}'?",
             f"I did {_nice_goal_name(e1)}",
             f"You should always remember what you do when you hear the user saying '{asr1}'"),
            (f"What were you doing the moment the last time you heard the user saying '{asr1}'?",
             f"I did {_nice_goal_name(e2)}",
             f"You should always remember what you do when you hear the user saying '{asr2}'")
        )
        robot_loc_1 = _get_robot_location(e1.latest_scene)
        robot_loc_2 = _get_robot_location(e2.latest_scene)
        if robot_loc_1 and robot_loc_2:
            yield _create_sample(
                (f"Where have you been the first time you heard the user saying '{asr1}'?",
                 f"At the {robot_loc_1}",
                 f"You should always remember your exact location when the user says '{asr1}'"),
                (f"Where have you been the last time you heard the user saying '{asr2}'?",
                 f"At the {robot_loc_2}",
                 f"You should always remember your exact location when the user says '{asr2}'")
            )


def _make_obj_questions(objs: List[str], obj_category: str,
                        episodes: List[HigherLevelSummary], min_question_distance: timedelta, t_format: str):
    full_history = HigherLevelSummary('', episodes)
    events_with_obj = [
        e for e in iter_nodes_of_type(full_history, EventBasedSummary)
        if any(obj in x.obj_class for x in e.latest_scene.objects for obj in objs)
    ]
    if len(events_with_obj) == 0:
        return
    e1, e2 = events_with_obj[0], events_with_obj[-1]
    remember_q_actual_time, recall_q_actual_time = _extract_times(e1, e2, episodes, min_question_distance)
    if remember_q_actual_time is None or recall_q_actual_time is None:
        return
    obj1 = [obj for x in e1.latest_scene.objects for obj in objs if obj in x.obj_class][0]  # 0 or -1 is arbitrary.
    obj2 = [obj for x in e2.latest_scene.objects for obj in objs if obj in x.obj_class][-1]
    det = 'the' if len(objs) == 1 else ('an' if obj_category[0] in 'aeiou' else 'a')

    yield _create_sample_from_qac_pair(
        (f"When did you first see the {obj1}?",
         f"At {e1.range[1].strftime(t_format)}",
         f"You should always remember the exact time when you see {det} {obj_category}"),
        (f"When did you last see the {obj2}?",
         f"At {e2.range[1].strftime(t_format)}",
         f"You should always remember the exact time when you see {det} {obj_category}"),
        remember_q_actual_time, recall_q_actual_time, e1.range, e2.range
    )
    yield _create_sample_from_qac_pair(
        (f"What did you do the first time you saw the {obj1}?",
         f"I did {_nice_goal_name(e1)}",
         f"You should always remember what you do when you see {det} {obj_category}"),
        (f"What did you do the last time you saw the {obj2}?",
         f"I did {_nice_goal_name(e2)}",
         f"You should always remember what you do when you see {det} {obj_category}"),
        remember_q_actual_time, recall_q_actual_time, e1.range, e2.range,
    )
    loc_1 = _get_location_of_object(e1.latest_scene, obj1)
    loc_2 = _get_location_of_object(e2.latest_scene, obj2)
    if loc_1 and loc_2:
        yield _create_sample_from_qac_pair(
            (f"Where did you first see the {obj1}?",
             f"{loc_1}",
             f"You should always remember the exact location where you see the {det} {obj_category}"),
            (f"Where did you last see the {obj2}?",
             f"{loc_2}",
             f"You should always remember the exact location where you see the {det} {obj_category}"),
            remember_q_actual_time, recall_q_actual_time, e1.range, e2.range,
        )


def generate_incremental_qa_histories(
        pkl_files: List[Path],
        rng_seed=42,
        min_seq_len=3, max_seq_len=10,
        num_test_cases_per_history=10,
        ensure_unique_episodes=True,
):
    rng = Random(rng_seed)
    seq_generator = generate_sequences(
        pkl_files, rng,
        min_seq_len, max_seq_len,
        ensure_unique_episodes,
        HistoryGenDateTimeSettings(
            rng_base_date=datetime(year=2025, month=1, day=1),
            skip_day_probability=0.5, max_skipped_days=20,
            min_episodes_per_day=1, max_episodes_per_day=3,
            min_distance_between_episodes=timedelta(seconds=30)
        )
    )
    for episodes, files in seq_generator:
        history = [
            {
                'episode': str(file),
                'start_date': ep.range[0].strftime('%Y-%m-%d %H:%M:%S'),
                'qa': {}
            }
            for ep, file in zip(episodes, files)
        ]

        test_cases = list(generate_test_cases(episodes))
        if len(test_cases) < num_test_cases_per_history:
            print('Episode was not useful (too few samples)')
            continue  # Not a useful sample...
        assert all(len(d) == 2 for d in test_cases)
        test_cases = rng.sample(test_cases, k=num_test_cases_per_history)
        for test_case_dict in test_cases:
            for ep_idx, qa_dict in test_case_dict.items():
                existing_qa = history[ep_idx]['qa']
                for timestamp, qa_samples in qa_dict.items():
                    existing_qa.setdefault(timestamp, []).extend(qa_samples)
        for episode in history:
            for qa_ts, qa_samples in list(episode['qa'].items()):
                if isinstance(qa_ts, tuple):
                    # Need to randomly choose one (relative) time from this range of (start, end) times
                    del episode['qa'][qa_ts]
                    start_s, end_s = (x.total_seconds() for x in qa_ts)
                    selected_s = start_s + rng.random() * (end_s - start_s)
                    episode['qa'][str(selected_s)] = qa_samples
        # Sort the qa timestamp keys in case there are multiple ones
        for episode in history:
            episode['qa'] = OrderedDict(sorted(episode['qa'].items(), key=lambda t: float(t[0])))

        yield history


def _get_episode_idx_for_timestamp(episodes: List[HigherLevelSummary], ts: datetime):
    episode_idx = [i for i, e in enumerate(episodes) if e.range[0] <= ts <= e.range[1]]
    if len(episode_idx) == 0:
        return None
    assert len(episode_idx) == 1
    return episode_idx[0]


def _locate_in_episodes(episodes: List[HigherLevelSummary],
                        at_or_after_ts: datetime,
                        before: datetime = datetime.max) -> Optional[Tuple[int, Tuple[timedelta, timedelta]]]:
    idx = _get_episode_idx_for_timestamp(episodes, at_or_after_ts)
    if idx is None:
        # Find next episode, if any.
        episodes_after_indices = [i for i, e in enumerate(episodes) if e.range[0] > at_or_after_ts]
        if episodes_after_indices:
            idx = episodes_after_indices[0]
        else:
            return None

    selected_ep = episodes[idx]
    return idx, (at_or_after_ts - selected_ep.range[0] if at_or_after_ts > selected_ep.range[0] else timedelta(0),
                 min(selected_ep.range[1], before) - selected_ep.range[0])


def _create_sample_from_qac_pair(qac1: Tuple[str, str, str], qac2: Tuple[str, str, str],
                                 remember_q_actual_time: Tuple[int, Tuple[timedelta, timedelta]],
                                 recall_q_actual_time: Tuple[int, Tuple[timedelta, timedelta]],
                                 ref_span_1: Tuple[datetime, datetime], ref_span_2: Tuple[datetime, datetime]):
    (q1, a1, c1), (q2, a2, c2) = qac1, qac2
    pair_id = hashlib.md5(f'{remember_q_actual_time}{recall_q_actual_time}{q1}{a1}{q2}{a2}'.encode(),
                          usedforsecurity=False).hexdigest()
    return {
        remember_q_actual_time[0]: {
            remember_q_actual_time[1]: [
                {
                    "question": q1,
                    "answer": a1,
                    "correction": c1,
                    "reference": [r.strftime('%Y-%m-%d %H:%M:%S') for r in ref_span_1],
                    "pairid": pair_id,
                    "pair_idx": 1,
                }
            ]
        },
        recall_q_actual_time[0]: {
            recall_q_actual_time[1]: [
                {
                    "question": q2,
                    "answer": a2,
                    "correction": c2,
                    "reference": [r.strftime('%Y-%m-%d %H:%M:%S') for r in ref_span_2],
                    "pairid": pair_id,
                    "pair_idx": 2,
                }
            ]
        }
    }


def create_rephrase_questions_chain(llm: BaseChatModel):
    lines = (Path(__file__).parent / 'question_conversion_samples.tsv').read_text().splitlines()
    headers = lines[0].split('\t')
    samples = [
        {headers[i]: cell for i, cell in enumerate(line.split('\t'))}
        for line in lines[1:]
    ]
    f = dict(template_format='jinja2')
    prompt = (
            SystemMessagePromptTemplate.from_template(
                'You are a smart assistant with strong knowledge of robotics and AI. '
                'You receive a sample containing very technical terms and expressions, and your job is to rephrase '
                'it to use normal language. It is ok to leave out some of the technical detail as long as it '
                'preserves the unambiguity of the question. Each sample consists of a question, answer and correction '
                '(that the system will receive if it fails to answer the question). The semantics of the answer must '
                'be preserved exactly.\n'
                'Also consider the following notes:\n'
                'The questions are intended for the humanoid ARMAR-7 robot, operating in a household environment.\n'
                'For rotations/directions, positive angle means counter-clockwise/left, negative clockwise/right.\n'
                'The LoadDishwasher task is actually about dishwasher unloading. The parameters open, close, grasp '
                'are bool whether to perform the corresponding action as part of the task.\n'
                'The episodic_verbalization task means that the system received and answered a question from the user '
                'about its own history (i.e. what the system did in the past).\n'
                '\n'
                'Output a JSON with question, answer and correction. Follow the provided examples.'
            )
            + FewShotChatMessagePromptTemplate(examples=samples,
                                               input_variables=[],
                                               example_prompt=(HumanMsg.from_template(
                                                   '{"question": "{{orig_q}}", '
                                                   '"answer": "{{orig_a}}", '
                                                   '"correction": "{{orig_c}}"}', **f
                                               ) + AIMsg.from_template(
                                                   '{"question": "{{mod_q}}", '
                                                   '"answer": "{{mod_a}}", '
                                                   '"correction": "{{mod_c}}"}', **f
                                               )))
            + HumanMsg.from_template('{"question": "{{question}}", '
                                     '"answer": "{{answer}}", '
                                     '"correction": "{{correction}}"}', **f)
    )
    return RunnableParallel(
        sample=RunnablePassthrough(),
        modified_values=prompt | llm | JsonOutputParser()
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--history-pickles', type=Path, nargs='+', default=[])
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--n-histories', type=int, default=10)
    parser.add_argument('--min-seq-len', type=int, default=3)
    parser.add_argument('--max-seq-len', type=int, default=10)
    parser.add_argument('--num-test-cases-per-history', type=int, default=10)
    parser.add_argument('--improve-llm', type=ast.literal_eval, default=None)
    parser.add_argument('--improve-existing-file', type=Path, default=None)
    parser.add_argument('out_file', type=Path)
    args = parser.parse_args()

    assert args.history_pickles or args.improve_existing_file
    assert not (args.history_pickles and args.improve_existing_file)
    assert not args.improve_existing_file or args.improve_llm

    if args.history_pickles:
        samples = {
            f'history-{i}': h
            for i, h in enumerate(islice(generate_incremental_qa_histories(
                args.history_pickles, args.seed,
                args.min_seq_len, args.max_seq_len,
                args.num_test_cases_per_history
            ), args.n_histories))
        }
    else:
        samples = json.loads(args.improve_existing_file.read_text())['data']
    if args.improve_llm:
        import langchain.globals
        from langchain_community.cache import SQLiteCache
        langchain.globals.set_llm_cache(SQLiteCache(database_path="langchain-cache.db"))

        llm = instantiate_llm(args.improve_llm)
        # noinspection PyTypeChecker
        chain = create_rephrase_questions_chain(llm)
        all_qs = [q for h in samples.values() for e in h for s in e['qa'].values() for q in s]
        output = chain.batch(all_qs)
        for o in output:  # Modify the original samples in-place
            o['sample']['original_q'] = o['sample']['question']
            o['sample']['original_a'] = o['sample']['answer']
            o['sample']['original_c'] = o['sample']['correction']
            o['sample']['question'] = o['modified_values']['question']
            o['sample']['answer'] = o['modified_values']['answer']
            o['sample']['correction'] = o['modified_values']['correction']

    output = {
        'config': {k: str(v) for k, v in args.__dict__.items()},
        'data': samples
    }
    args.out_file.write_text(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
