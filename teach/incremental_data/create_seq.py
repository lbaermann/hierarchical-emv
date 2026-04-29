import argparse
import hashlib
import json
import re
from datetime import timedelta, datetime
from itertools import islice
from pathlib import Path
from random import Random
from typing import Literal, List, Tuple, Optional

from em.em_tree import HigherLevelSummary, iter_nodes_of_type, GoalBasedSummary, SceneGraphInstant
from em.randomize_episodes import randomize_datetimes, HistoryGenDateTimeSettings
from em.teach import load_teach_episode, TEACH_ACTIONS_WITH_INDIRECT_OBJECT

TeachSplit = Literal['train', 'valid_seen', 'valid_unseen']


# Endless sequence generator
def generate_sequences(teach_home: Path,
                       split: TeachSplit,
                       rng: Random,
                       min_seq_len=5, max_seq_len=10,
                       datetime_settings=HistoryGenDateTimeSettings()):
    game_dir = teach_home / 'games' / split
    game_ids = [f.name.split('.')[0] for f in game_dir.glob('*.game.json')]

    while True:
        seq_len = rng.randint(min_seq_len, max_seq_len)
        sampled_game_ids = rng.choices(game_ids, k=seq_len)

        episodes_with_ts_corrections = [
            load_teach_episode(game_dir / f'{game_id}.game.json', return_initial_ts_correction=True)
            for game_id in sampled_game_ids
        ]
        episodes = [e for e, ts in episodes_with_ts_corrections]
        ts_corrections = [ts for e, ts in episodes_with_ts_corrections]
        yield randomize_datetimes(episodes, datetime_settings, rng), ts_corrections, sampled_game_ids


def _extract_obj_from_goal(g):
    g = g.latest_raw.current_goal
    params = g[g.index('(') + 1:g.index(')')]  # Action(Object_5_Slice_3, Place_3)
    return _obj_id_to_display_str(params.split(',')[0])


def _extract_location_from_goal(g):
    g = g.latest_raw.current_goal
    params = g[g.index('(') + 1:g.index(')')]  # Action(Object_5_Slice_3, Place_3)
    return _obj_id_to_display_str(params.split(',')[1].strip())


def _obj_id_to_display_str(obj_id: str):
    parts = obj_id.split('_')
    name = parts[0].lower()
    if len(parts) > 1 and not re.fullmatch(r'\d+', parts[1]):
        name += ' ' + parts[1].lower()  # Sink_Basin
    if 'Sliced' in parts:
        name += ' slice'
    return name


def _get_objects_in(scene: SceneGraphInstant, container_display_name: str):
    container_candidates = [i for i, o in enumerate(scene.objects)
                            if _obj_id_to_display_str(o.obj_class) == container_display_name]
    assert len(container_candidates) == 1
    container_idx = container_candidates[0]
    obj_indices_in_container = [from_idx for from_idx, to_idx, rel in scene.relations
                                if to_idx == container_idx and 'in' in rel]
    return [_obj_id_to_display_str(scene.objects[i].obj_class)
            for i in obj_indices_in_container]


def _find_interaction_goals(episodes: List[HigherLevelSummary],
                            action: str):
    for e in episodes:
        for g in iter_nodes_of_type(e, GoalBasedSummary):
            if g.latest_raw.current_goal.startswith(action):
                yield g


def _find_transport_goals(episodes: List[HigherLevelSummary]):
    for e in episodes:
        prev_starting_from_pickup = []
        for g in iter_nodes_of_type(e, GoalBasedSummary):
            if prev_starting_from_pickup:
                prev_starting_from_pickup.append(g)
                prev_pickup = prev_starting_from_pickup[0]
                if (
                        g.latest_raw.current_goal.startswith('Place')
                        and g.latest_raw.current_goal_state == 'success'
                        and _extract_obj_from_goal(g) == _extract_obj_from_goal(prev_pickup)
                ):
                    yield GoalBasedSummary(events=prev_starting_from_pickup,
                                           explicit_goal=f'Transport({_extract_obj_from_goal(prev_pickup)}, '
                                                         f'{_extract_location_from_goal(g)})')
                    prev_starting_from_pickup = []
            if g.latest_raw.current_goal.startswith('Pickup'):
                prev_starting_from_pickup = [g]


def _find_distant_same_tasks(episodes: List[HigherLevelSummary],
                             min_question_distance: timedelta):
    group_by_task = {}
    for e in episodes:
        summary = e.nl_summary.lower().strip('. ')
        group_by_task.setdefault(summary, []).append(e)

    for task, group in list(group_by_task.items()):
        distances = [g2.range[0] - g1.range[1] for g1, g2 in zip(group[:-1], group[1:])]
        if all(d < min_question_distance for d in distances):
            del group_by_task[task]

    for group in group_by_task.values():
        yield group[0], group[-1]


def _find_distant_actions_with_same_param(goals: List[GoalBasedSummary],
                                          min_question_distance: timedelta,
                                          param_type: Literal['obj', 'loc', 'both'] = 'obj'):
    extract_fns = {
        'obj': _extract_obj_from_goal,
        'loc': _extract_location_from_goal,
        'both': lambda g: (_extract_obj_from_goal(g), _extract_location_from_goal(g))
    }
    objects = [extract_fns[param_type](g) for g in goals]
    group_by_obj = {}
    for o, g in zip(objects, list(goals)):
        group_by_obj.setdefault(o, []).append(g)
    for o in list(group_by_obj.keys()):
        group = group_by_obj[o]
        distances = [g2.range[0] - g1.range[1] for g1, g2 in zip(group[:-1], group[1:])]
        # all([]) is also True, so this applies if len(group) <= 1
        if all(d < min_question_distance for d in distances):
            del group_by_obj[o]

    for group in group_by_obj.values():
        yield group[0], group[-1]


def _get_episode_idx_for_timestamp(episodes: List[HigherLevelSummary], ts: datetime):
    episode_idx = [i for i, e in enumerate(episodes) if e.range[0] <= ts <= e.range[1]]
    if len(episode_idx) == 0:
        return None
    assert len(episode_idx) == 1
    return episode_idx[0]


def _locate_in_episodes(episodes: List[HigherLevelSummary],
                        ts_corrections: List[float],
                        at_or_after_ts: datetime,
                        return_multiple_choices_within_episode=True) -> Optional[Tuple[int, Tuple[str, ...]]]:
    # Returns (episode idx, timestamp for export) identifying the given timestamp.
    idx = _get_episode_idx_for_timestamp(episodes, at_or_after_ts)
    if idx is None:
        # Find next episode, if any.
        episodes_after_indices = [i for i, e in enumerate(episodes) if e.range[0] > at_or_after_ts]
        if episodes_after_indices:
            idx = episodes_after_indices[0]
        else:
            return None

    random_choice_from = []
    for scene in iter_nodes_of_type(episodes[idx], SceneGraphInstant):
        ts = scene.raw.timestamp
        if ts >= at_or_after_ts:
            time_spec = str((ts - episodes[idx].range[0] + timedelta(seconds=ts_corrections[idx])).total_seconds())
            if return_multiple_choices_within_episode:
                random_choice_from.append(time_spec)
            else:
                return idx, (time_spec,)
    if return_multiple_choices_within_episode:
        return idx, tuple(random_choice_from)
    assert False


def _gen_task_test_cases(episodes: List[HigherLevelSummary], ts_corrections: List[float],
                         t1: HigherLevelSummary, t2: HigherLevelSummary,
                         min_question_distance: timedelta):
    remember_q_min_time = t1.range[1] + min_question_distance
    remember_q_actual_time = _locate_in_episodes(episodes, ts_corrections, remember_q_min_time)
    recall_q_min_time = t2.range[1] + min_question_distance
    recall_q_actual_time = _locate_in_episodes(episodes, ts_corrections, recall_q_min_time)
    if remember_q_actual_time is None or recall_q_actual_time is None:
        return []

    task = t1.nl_summary.lower().strip('. ')
    t_format = '%Y/%m/%d'

    qac_pairs = [
        (
            (f"At what day did you first {task}?",
             f"At {t1.range[1].strftime(t_format)}",
             f"You should always remember the date when you {task}"),
            (f"At what day did you last {task}?",
             f"At {t2.range[1].strftime(t_format)}",
             f"You should always remember the date when you {task}"),
            t1.range, t2.range
        ),
        (
            (f"What was the first step you performed the first time you did the task '{task}'?",
             _format_display_goal(t1.children[0]),
             f"You should always remember the detailed steps you perform during the task '{task}'"),
            (f"What was the first step you performed the last time you did the task '{task}'?",
             _format_display_goal(t2.children[0]),
             f"You should always remember the detailed steps you perform during the task '{task}'"),
            t1.children[0].range, t2.children[0].range
        )
    ]

    return [_create_sample_from_qac_pair(qac1, qac2, remember_q_actual_time, recall_q_actual_time, r1, r2)
            for qac1, qac2, r1, r2 in qac_pairs]


def _gen_same_location_test_cases(episodes: List[HigherLevelSummary], ts_corrections: List[float],
                                  g1: GoalBasedSummary, g2: GoalBasedSummary,
                                  action_name: str, min_question_distance: timedelta,
                                  preposition='to'):
    remember_q_min_time = g1.range[1] + min_question_distance
    remember_q_actual_time = _locate_in_episodes(episodes, ts_corrections, remember_q_min_time)
    recall_q_min_time = g2.range[1] + min_question_distance
    recall_q_actual_time = _locate_in_episodes(episodes, ts_corrections, recall_q_min_time)
    if remember_q_actual_time is None or recall_q_actual_time is None:
        return []

    place = _extract_location_from_goal(g1)
    obj1 = _extract_obj_from_goal(g1)
    obj2 = _extract_obj_from_goal(g2)
    action_spec = f'{action_name} {preposition} the {place}'
    action_spec_sm = f'{action_name} something {preposition} the {place}'
    t_format = '%Y/%m/%d, %H:%M:%S'

    qac_pairs = [
        (
            (f"Which object did you first {action_spec}?",
             f"The {obj1}",
             f"You should always remember which object you {action_spec}"),
            (f"Which object did you last {action_spec}?",
             f"The {obj2}",
             f"You should always remember which object you {action_spec}"),
            g1.range, g2.range
        ),
        (
            (f"When did you first {action_spec_sm}?",
             f"At {g1.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {action_spec_sm}"),
            (f"When did you last {action_spec_sm}?",
             f"At {g2.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {action_spec_sm}"),
            g1.range, g2.range
        ),
    ]

    return [_create_sample_from_qac_pair(qac1, qac2, remember_q_actual_time, recall_q_actual_time, r1, r2)
            for qac1, qac2, r1, r2 in qac_pairs]


def _gen_test_cases(episodes: List[HigherLevelSummary], ts_corrections: List[float],
                    g1: GoalBasedSummary, g2: GoalBasedSummary,
                    action_name: str, indirect_obj: bool, min_question_distance: timedelta):
    remember_q_min_time = g1.range[1] + min_question_distance
    remember_q_actual_time = _locate_in_episodes(episodes, ts_corrections, remember_q_min_time)
    recall_q_min_time = g2.range[1] + min_question_distance
    recall_q_actual_time = _locate_in_episodes(episodes, ts_corrections, recall_q_min_time)
    if remember_q_actual_time is None or recall_q_actual_time is None:
        # Sample too short / g2 too late in history. Just generate new sample
        return []

    is_compound_goal = all(isinstance(c, GoalBasedSummary) for c in g1.events + g2.events)
    time_specifier = 'finish to ' if is_compound_goal else ''
    obj_1 = _extract_obj_from_goal(g1)
    obj_2 = _extract_obj_from_goal(g2)
    det = lambda o: 'an' if o[0] in 'aeiou' else 'a'
    t_format = '%Y/%m/%d, %H:%M:%S'
    objs_g1 = set(_obj_id_to_display_str(o.obj_class) for o in g1.latest_scene.objects if o.obj_class != 'agent hand')
    objs_g2 = set(_obj_id_to_display_str(o.obj_class) for o in g2.latest_scene.objects if o.obj_class != 'agent hand')
    qac_pairs = []
    qac_pairs += [
        (
            (f"When did you first {time_specifier}{action_name} {det(obj_1)} {obj_1}?",
             f"At {g1.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {time_specifier}{action_name} {det(obj_1)} {obj_1}"),
            (f"When did you last {time_specifier}{action_name} {det(obj_2)} {obj_2}?",
             f"At {g2.range[1].strftime(t_format)}",
             f"You should always remember the exact time when you {time_specifier}{action_name} {det(obj_2)} {obj_2}"),
            g1.range, g2.range
        ),
        (
            (f"What objects did you see the first time you did {time_specifier}{action_name} {det(obj_1)} {obj_1}?",
             ', '.join(objs_g1),
             f"You should always remember all the objects you see when you {time_specifier}{action_name} {det(obj_1)} {obj_1}"),
            (f"What objects did you see the last time you did {time_specifier}{action_name} {det(obj_2)} {obj_2}?",
             ', '.join(objs_g2),
             f"You should always remember all the objects you see when you {time_specifier}{action_name} {det(obj_2)} {obj_2}"),
            g1.range, g2.range
        )
    ]
    if indirect_obj:
        # This means that the actual object of the current goal is the place.
        place_1 = _extract_location_from_goal(g1)
        place_2 = _extract_location_from_goal(g2)
        where = 'To where' if action_name == 'transport' else 'Where'
        qac_pairs.append((
            (f"{where} did you first {action_name} {det(obj_1)} {obj_1}?",
             f"At the {place_1}",
             f"You should always remember the location {where.lower()} you {action_name} {det(obj_1)} {obj_1}"),
            (f"{where} did you last {action_name} {det(obj_2)} {obj_2}?",
             f"At the {place_2}",
             f"You should always remember the location {where.lower()} you {action_name} {det(obj_2)} {obj_2}"),
            g1.range, g2.range
        ))
    if action_name == 'pour' and 'sink' in objs_g1 and 'sink' in objs_g2:
        # Objects from TEACh simulation are sometimes inside "Sink" and sometimes inside "Sink_Basin"
        objs_in_sink_g1 = _get_objects_in(g1.latest_scene, 'sink')
        if not objs_in_sink_g1 and 'sink basin' in objs_g1:
            objs_in_sink_g1 = _get_objects_in(g1.latest_scene, 'sink basin')
        objs_in_sink_g2 = _get_objects_in(g2.latest_scene, 'sink')
        if not objs_in_sink_g2 and 'sink basin' in objs_g2:
            objs_in_sink_g2 = _get_objects_in(g2.latest_scene, 'sink basin')
        if objs_in_sink_g1 and objs_in_sink_g2:
            qac_pairs.append((
                (f"What objects did you see inside the sink the first time you poured the {obj_1}?",
                 ', '.join(set(objs_in_sink_g1)),
                 f"You should always remember all the objects you see in the sink when you pour the {obj_1}"),
                (f"What objects did you see inside the sink the last time you poured the {obj_2}?",
                 ', '.join(set(objs_in_sink_g2)),
                 f"You should always remember all the objects you see in the sink when you pour the {obj_2}"),
                g1.range, g2.range
            ))
    if is_compound_goal:
        # This is an artificially created compound goal
        qac_pairs.append((
            (f"What steps did you perform during {action_name} of the {obj_1}?",
             ', '.join(_format_display_goal(c) for c in g1.events),
             f"You should always remember the detailed steps you perform during {action_name} of the {obj_1}"),
            (f"What steps did you perform during {action_name} of the {obj_1}?",
             ', '.join(_format_display_goal(c) for c in g1.events),
             f"You should always remember the detailed steps you perform during {action_name} of the {obj_2}"),
            g1.range, g2.range
        ))

    return [_create_sample_from_qac_pair(qac1, qac2, remember_q_actual_time, recall_q_actual_time, r1, r2)
            for qac1, qac2, r1, r2 in qac_pairs]


def _create_sample_from_qac_pair(qac1: Tuple[str, str, str], qac2: Tuple[str, str, str],
                                 remember_q_actual_time: Tuple[int, Tuple[str, ...]],
                                 recall_q_actual_time: Tuple[int, Tuple[str, ...]],
                                 ref_span_1: Tuple[datetime, datetime], ref_span_2: Tuple[datetime, datetime],
                                 ):
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


def _format_display_goal(g):
    goal = g.latest_raw.current_goal
    if '(' not in goal:
        return goal
    action = goal[:goal.index('(')]
    indirect_obj = action in TEACH_ACTIONS_WITH_INDIRECT_OBJECT
    obj = _extract_obj_from_goal(g)
    if indirect_obj:
        place = _extract_location_from_goal(g)
        return f'{action} the {obj} at the {place}'
    else:
        return f'{action} the {obj}'


def generate_importance_test_cases(episodes: List[HigherLevelSummary],
                                   ts_corrections: List[float]):
    for simple_action in ['Pickup', 'Slice', 'Place', 'Pour']:
        indirect_obj = simple_action in TEACH_ACTIONS_WITH_INDIRECT_OBJECT
        min_question_distance = timedelta(days=1)
        actions = list(_find_interaction_goals(episodes, simple_action))
        for g1, g2 in _find_distant_actions_with_same_param(actions, min_question_distance):
            test_cases = _gen_test_cases(episodes, ts_corrections, g1, g2, simple_action.lower(), indirect_obj,
                                         min_question_distance)
            yield from iter(test_cases)
    transports = list(_find_transport_goals(episodes))
    min_question_distance = timedelta(days=1)
    for g1, g2 in _find_distant_actions_with_same_param(transports, min_question_distance):
        test_cases = _gen_test_cases(episodes, ts_corrections, g1, g2, action_name='transport',
                                     indirect_obj=True, min_question_distance=min_question_distance)
        yield from iter(test_cases)
    for g1, g2 in _find_distant_actions_with_same_param(transports, min_question_distance, param_type='loc'):
        test_cases = _gen_same_location_test_cases(episodes, ts_corrections, g1, g2, action_name='transport',
                                                   min_question_distance=min_question_distance)
        yield from iter(test_cases)
    for g1, g2 in _find_distant_actions_with_same_param(list(_find_interaction_goals(episodes, 'place')),
                                                        min_question_distance, param_type='loc'):
        test_cases = _gen_same_location_test_cases(episodes, ts_corrections, g1, g2, action_name='place',
                                                   min_question_distance=min_question_distance, preposition='at')
        yield from iter(test_cases)

    min_question_distance = timedelta(days=2)
    for t1, t2 in _find_distant_same_tasks(episodes, min_question_distance):
        test_cases = _gen_task_test_cases(episodes, ts_corrections, t1, t2, min_question_distance)
        yield from iter(test_cases)


def generate_incremental_qa_histories(
        teach_base: Path, split: TeachSplit,
        rng_seed=42, num_test_cases_per_history=4,
        min_seq_len=3, max_seq_len=10,
):
    rng = Random(rng_seed)
    seq_generator = generate_sequences(
        teach_base, split, rng,
        min_seq_len, max_seq_len,
        HistoryGenDateTimeSettings(
            skip_day_probability=0.6, max_skipped_days=5,
            min_episodes_per_day=1, max_episodes_per_day=2,
            min_distance_between_episodes=timedelta(seconds=30)  # Just to ensure there is no overlapping episode error
        )
    )
    for episodes, ts_corrections, game_ids in seq_generator:
        history = [
            {
                'game_id': f'{split}/{game_id}',
                'start_date': ep.range[0].strftime('%Y-%m-%d %H:%M:%S'),
                'qa': {}
            }
            for ep, game_id in zip(episodes, game_ids)
        ]
        test_cases = list(generate_importance_test_cases(episodes, ts_corrections))
        if len(test_cases) < num_test_cases_per_history:
            continue  # Not a useful sample...
        test_cases = rng.sample(test_cases, k=min(len(test_cases), num_test_cases_per_history))
        for test_case_dict in test_cases:
            for ep_idx, qa_dict in test_case_dict.items():
                existing_qa = history[ep_idx]['qa']
                for timestamp, qa_samples in qa_dict.items():
                    existing_qa.setdefault(timestamp, []).extend(qa_samples)
        for episode in history:
            for qa_ts, qa_samples in list(episode['qa'].items()):
                if isinstance(qa_ts, tuple):
                    # Need to randomly choose one key from this list of options
                    del episode['qa'][qa_ts]
                    episode['qa'][rng.choice(qa_ts)] = qa_samples
        yield history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--teach-base', type=Path, required=True)
    parser.add_argument('--teach-split', choices=TeachSplit.__args__, default='train')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--n-histories', type=int, required=True)
    parser.add_argument('--num-test-cases-per-history', type=int, default=4)
    parser.add_argument('--min-seq-len', type=int, default=3)
    parser.add_argument('--max-seq-len', type=int, default=10)
    parser.add_argument('out_file', type=Path)
    args = parser.parse_args()

    samples = {
        f'history-{i}': h
        for i, h in enumerate(islice(generate_incremental_qa_histories(
            args.teach_base, args.teach_split, args.seed, args.num_test_cases_per_history,
            args.min_seq_len, args.max_seq_len,
        ), args.n_histories))
    }
    output = {
        'config': {k: str(v) for k, v in args.__dict__.items()},
        'data': samples
    }
    args.out_file.write_text(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
