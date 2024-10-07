from datetime import datetime, timedelta
from typing import Dict

from .em_tree import HigherLevelSummary, SceneGraphInstant, RawDataInstant, ObjectNode
from .rule_based_summary import select_keyframe_indices, build_event_summaries_with_indices, select_goal_indices, \
    build_goal_summaries_with_indices


def load_armarx_emv_episode(episode: Dict, episode_start_time: datetime = None) -> HigherLevelSummary:
    if episode_start_time is None:
        episode_start_time = datetime.now()

    # We mainly use the HistoryGenerator from emv-research repo in order to convert from old episode format
    from emv.data_gen.gen_histories import HistoryGenerator, HistoryGenDateTimeSettings
    from emv.data_gen.domain_defs import Episode
    gen = HistoryGenerator([Episode.parse(episode)], max_history_length_in_episodes=1,
                           empty_history_probability=0, incomplete_episode_probability=0,
                           datetime_settings=HistoryGenDateTimeSettings(
                               rng_base_date=episode_start_time,
                               max_start_date_distance=timedelta(minutes=0)
                           ))
    history = next(gen)

    scenes = []
    grasped_objs = {}
    running_action = None
    for timestamp, keyframe in history.items():
        if keyframe.actions:
            running_action = keyframe.actions[0].name
        raw_data = RawDataInstant(
            timestamp=timestamp, image=None, sound=None, asr_recognition=None,
            current_action=running_action,
            current_action_state=keyframe.actions[0].status if keyframe.actions else (
                'started' if running_action else None),
            current_goal=keyframe.current_goal,
            current_goal_state=keyframe.current_planner_status
        )
        if keyframe.actions and keyframe.actions[0].status != 'started':
            running_action = None

        objects = [ObjectNode(o.name, o.name) for o in keyframe.objects]

        if raw_data.current_action:
            # example current_action: putdown Armar3 handleft3a roundtable multivitaminjuice
            parts = raw_data.current_action.split()
            if parts[0] == 'grasp' and raw_data.current_action_state == 'success':
                grasped_objs[parts[2]] = parts[4]
            elif parts[0] == 'putdown' and raw_data.current_action_state == 'success':
                del grasped_objs[parts[2]]

        def _find_or_add_obj(obj_name: str) -> int:
            obj_idx_candidates = [i for i, o in enumerate(objects) if o.obj_class == obj_name]
            if obj_idx_candidates:
                return obj_idx_candidates[0]
            else:
                objects.append(ObjectNode(obj_name, obj_name))
                return len(objects) - 1

        relations = []
        for hand, obj in grasped_objs.items():
            hand_idx = _find_or_add_obj(hand)
            obj_idx = _find_or_add_obj(obj)
            relations.append((obj_idx, hand_idx, 'inside'))

        scenes.append(SceneGraphInstant(
            objects=objects,
            relations=relations,
            raw=raw_data
        ))

    event_indices = select_keyframe_indices(scenes)
    events = build_event_summaries_with_indices(scenes, event_indices)

    goal_indices = select_goal_indices(events)
    goals = build_goal_summaries_with_indices(events, goal_indices)

    return HigherLevelSummary(
        nl_summary='',
        children=goals
    )
