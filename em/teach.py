import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import torch

from em.em_tree import HigherLevelSummary, RawDataInstant, SceneGraphInstant, ObjectNode
from em.em_util import LazyLoadPILImage
from em.rule_based_summary import select_keyframe_indices, build_event_summaries_with_indices, \
    build_goal_summaries_with_indices

RELEVANT_ACTION_TYPES = ['Motion', 'ObjectInteraction', 'Keyboard']
ACTION_ID_DIALOG = 100
COMMANDER_AGENT_ID = 0
FOLLOWER_AGENT_ID = 1
RELEVANT_OBJECT_STATES = {
    # maps to internal state name. Mapping to the same name means the properties are treated interchangeably
    'isToggled': 'toggled', 'isBroken': 'broken', 'isDirty': 'dirty', 'isCooked': 'cooked', 'isOpen': 'open',
    'simbotIsFilledWithWater': 'filled', 'isFilledWithLiquid': 'filled'
}


class _TeachNamingAndStateTrackingHandler:

    def __init__(self, game_data: dict):
        super().__init__()
        self._action_id_to_name = {
            a['action_id']: a['action_name'].replace(' ', '')  # CamelCase
            for a in game_data['definitions']['actions']
            if a['action_type'] in RELEVANT_ACTION_TYPES
        }
        self._objects_per_class = defaultdict(list)
        self._object_states = defaultdict(dict)
        for obj in game_data['tasks'][0]['episodes'][0]['initial_state']['objects']:
            obj_id = obj['objectId']
            states = self._object_states[obj_id]
            self._objects_per_class[obj['objectType']].append(obj_id)
            for state_key, internal_key in RELEVANT_OBJECT_STATES.items():
                states[internal_key] = obj.get(state_key, False) or states.get(internal_key, False)

    def update_object_states_from_diff(self, state_diff: dict):
        for obj_id, state in state_diff.items():
            current_states = self._object_states[obj_id]
            for state_key, internal_key in RELEVANT_OBJECT_STATES.items():
                # If there are two state_keys mapping to the same internal_key, and both are present in the same
                #  state_diff, the later one wins. But this should be rare and not contradict each other.
                if state_key in state:
                    current_states[internal_key] = state[state_key]

    def is_relevant_action(self, action_id: int):
        return action_id in self._action_id_to_name

    def format_action(self, action: dict) -> str:
        action_id = action['action_id']
        agent = action['agent_id']
        if action_id == ACTION_ID_DIALOG:
            if agent == FOLLOWER_AGENT_ID:
                return f'Say("{action.get("corrected_utterance", action["utterance"])}")'
            elif agent == COMMANDER_AGENT_ID:
                return 'Noop'
            else:
                raise AssertionError(agent)

        action_name = self._action_id_to_name[action_id]
        params = []
        if 'oid' in action:
            params.append(self.obj_id_to_name(action['oid']) if action['oid'] else 'None')

        return f'{action_name}({", ".join(params)})'

    def obj_id_to_name(self, obj_id: str):
        split = obj_id.split('|')
        obj_class = split[0]
        normal_obj_id = '|'.join(split[:4])
        if obj_class not in self._objects_per_class or normal_obj_id not in self._objects_per_class[obj_class]:
            return obj_class

        if len(self._objects_per_class[obj_class]) == 1:
            unique_name = obj_class  # Avoid unnecessary ids if there is only one of that type
        else:
            obj_idx = self._objects_per_class[obj_class].index(normal_obj_id)
            unique_name = f'{obj_class}_{obj_idx}'
        if len(split) > 4:  # This can be something like PotatoSlice_3
            simplified_sub_name = split[4].replace(obj_class, '')  # Avoid duplicate information
            return f"{unique_name}_{simplified_sub_name}"
        return unique_name

    def to_obj_node(self, obj_id: str) -> ObjectNode:
        active_states = []
        for key, state in self._object_states[obj_id].items():
            if state:
                active_states.append(key)
        return ObjectNode(self.obj_id_to_name(obj_id), obj_id,
                          state=', '.join(active_states) if active_states else None)


def load_teach_episode(teach_game_file: Path, start_time: datetime = None) -> HigherLevelSummary:
    if start_time is None:
        start_time = datetime.now()

    episode_name = teach_game_file.name[:-len('.game.json')]
    split = teach_game_file.parent.name
    teach_base_dir = teach_game_file.parent.parent.parent
    img_dir = teach_base_dir / 'images' / split / episode_name

    game = json.loads(teach_game_file.read_text())
    helper = _TeachNamingAndStateTrackingHandler(game)
    scenes = []
    interaction_timestamps = []

    # Teach episodes have some empty time in the beginning, where nothing happens (commander/follower reading the
    #  instructions). We want start_time as the time at which the first action happens, not some point in time before
    #  where nothing is happening. Thus, always subtract initial_ts_seconds
    initial_ts_seconds = game['tasks'][0]['episodes'][0]['interactions'][0]['time_start']

    for step in game['tasks'][0]['episodes'][0]['interactions']:
        action_id = step['action_id']
        agent = step['agent_id']
        if not helper.is_relevant_action(action_id) or (agent == COMMANDER_AGENT_ID and action_id != ACTION_ID_DIALOG):
            continue  # Skip irrelevant actions such as "check progress"
        ts = step['time_start']
        timestamp = start_time + timedelta(seconds=ts - initial_ts_seconds)
        objs_state_diff = json.loads((img_dir / f'statediff.{ts}.json').read_text())['objects']
        helper.update_object_states_from_diff(objs_state_diff)
        if 'oid' in step and step['success']:  # This seems to be a non-navigation interaction
            interaction_timestamps.append(timestamp)
        action = helper.format_action(step)
        success = 'success' if step['success'] else 'failure'
        objects = [
            helper.to_obj_node(obj_id)
            for obj_id, current_obj_state in objs_state_diff.items()
            if current_obj_state.get('visible')
        ]

        def _find_or_add_obj_idx(object_id: str, allow_add=True):
            idx = [i for i, o in enumerate(objects) if o.instance_id == object_id]
            assert len(idx) <= 1, f'{idx}, {object_id}, {objects}'
            if len(idx) == 0:
                if allow_add:
                    objects.append(helper.to_obj_node(object_id))
                    return len(objects) - 1
                else:
                    return -1
            return idx[0]

        relations = []
        for obj_id, current_obj_state in objs_state_diff.items():
            if current_obj_state.get('isPickedUp', False):
                objects.append(ObjectNode('agent hand', ''))
                hand_idx = len(objects) - 1
                relations.append((_find_or_add_obj_idx(obj_id), hand_idx, 'inside'))
            if current_obj_state.get('simbotLastParentReceptacle'):
                dst_idx = _find_or_add_obj_idx(current_obj_state['simbotLastParentReceptacle'])
                relations.append((_find_or_add_obj_idx(obj_id), dst_idx, 'in/on'))
            if current_obj_state.get('receptacleObjectIds'):
                for receptacle_id in current_obj_state.get('receptacleObjectIds'):
                    receptacle_idx = _find_or_add_obj_idx(receptacle_id, allow_add=False)
                    if receptacle_idx > -1:
                        relations.append((receptacle_idx, _find_or_add_obj_idx(obj_id), 'in/on'))
        # Since we follow both parent and child "receptacle" relations in the code above,
        #  we need to make sure there are no duplicate relations
        relations = list(set(relations))

        # noinspection PyTypeChecker
        scenes.append(SceneGraphInstant(
            objects=objects,
            relations=relations,
            raw=RawDataInstant(
                timestamp=timestamp,
                image=LazyLoadPILImage(img_dir / f'driver.frame.{ts}.jpeg'),
                asr_recognition=(
                    step.get("corrected_utterance", step["utterance"])
                    if action_id == ACTION_ID_DIALOG and agent == COMMANDER_AGENT_ID
                    else None),
                current_action=action,
                current_action_state=success,
                current_goal=action,
                current_goal_state=success
            )
        ))

    return _build_tree(scenes, interaction_timestamps, task_summary=game['tasks'][0]['desc'])


TEACH_INTERACTION_ACTIONS = ['Close', 'Open', 'Pickup', 'Place', 'Pour', 'Slice', 'ToggleOff', 'ToggleOn']


def load_teach_episode_no_gt(teach_trial_image_dir: Path,
                             obj_det_dir: Path,
                             action_inference_dir: Path,
                             start_time: datetime = None,
                             obj_det_threshold=0.1,
                             ignore_non_existing_action_files=False,
                             enable_in_hand_by_bbox=False,
                             use_speech=True):
    """
    Loads the TEACh episode without using object or action GT states.
    Still loads the observed dialog from the teach_image_dir / keyboard.*.json files (if use_speech is True)
    """
    if start_time is None:
        start_time = datetime.now()

    def _load_action_file():
        if asr_reco.get('agent_id') == FOLLOWER_AGENT_ID and use_speech:
            action_data = {
                'action': 'Say',
                'params': [asr_reco.get("utterance")],
            }
        else:
            action_file = action_inference_dir / f'{ts}.json'
            if not action_file.is_file():
                if ignore_non_existing_action_files:
                    return None, None
                else:
                    raise FileNotFoundError(action_file)
            action_data = json.loads(action_file.read_text())
        if not action_data:
            return None, None, None
        a = action_data['action']
        if a and action_data.get('params'):
            a += f'({", ".join(action_data["params"])})'
        s = 'success' if action_data.get('success', True) else 'failure'
        return a, action_data['action'], s

    img_files = sorted(
        (float(f.name[13:-5]), f)  # Convert to (timestamp, file) tuples
        for f in teach_trial_image_dir.glob('driver.frame.*.jpeg')
        if 'end' not in f.name
    )
    scenes = []
    interaction_timestamps = []
    for ts, img_f in img_files:
        obj_det_file = obj_det_dir / f'driver.frame.{ts}.json'
        obj_detections = json.loads(obj_det_file.read_text())
        objects = []
        relations = []
        hand_idx = None
        for detection in obj_detections['detections']:
            obj_name = detection['class']
            if detection['confidence'] >= obj_det_threshold:
                instance_idx = sum(1 for x in objects if x.obj_class == obj_name)
                objects.append(ObjectNode(obj_name, f'{obj_name}_{instance_idx}'))

                if not enable_in_hand_by_bbox:
                    continue
                bbox_xyxy = torch.tensor(detection['xyxy'], dtype=torch.float).reshape(2, 2)
                teach_img_dim = 900
                rel_center_point = bbox_xyxy.mean(dim=0) / teach_img_dim
                rel_bbox_len = (bbox_xyxy[1] - bbox_xyxy[0]) / teach_img_dim
                if (
                        0.47 <= rel_center_point[0] <= 0.53
                        and 0.67 <= rel_center_point[1] <= 0.73
                        and torch.all(0.05 <= rel_bbox_len)
                        and torch.all(rel_bbox_len <= 0.4)
                ):
                    obj_idx = len(objects) - 1
                    if hand_idx is None:
                        objects.append(ObjectNode('agent hand', ''))
                        hand_idx = len(objects) - 1
                    relations.append((obj_idx, hand_idx, 'inside'))

        keyboard_file = list(teach_trial_image_dir.glob(f'keyboard.*.{ts}.json'))
        if keyboard_file and use_speech:
            asr_reco = json.loads(keyboard_file[0].read_text())
        else:
            asr_reco = {}

        timestamp = start_time + timedelta(seconds=ts)
        action, action_category, success = _load_action_file()
        if action and success and action_category in TEACH_INTERACTION_ACTIONS:
            interaction_timestamps.append(timestamp)

        # noinspection PyTypeChecker
        scenes.append(SceneGraphInstant(
            objects=objects,
            relations=relations,
            raw=RawDataInstant(
                timestamp=timestamp,
                image=LazyLoadPILImage(img_f),
                asr_recognition=(
                    asr_reco['utterance']
                    if asr_reco and asr_reco['agent_id'] == COMMANDER_AGENT_ID
                    else None),
                current_action=action,
                current_action_state=success,
                current_goal=action,
                current_goal_state=success
            )
        ))

    return _build_tree(scenes, interaction_timestamps, task_summary='')


def _build_tree(scenes, interaction_timestamps, task_summary):
    event_indices = select_keyframe_indices(scenes)
    events = build_event_summaries_with_indices(scenes, event_indices)
    goal_indices = [i for i, event in enumerate(events)
                    if event.range[-1] in interaction_timestamps]
    goals = build_goal_summaries_with_indices(events, goal_indices)
    return HigherLevelSummary(
        nl_summary=task_summary,
        children=goals
    )
