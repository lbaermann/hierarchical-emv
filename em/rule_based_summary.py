from datetime import timedelta
from typing import List, Sequence, Union

from em.em_tree import SceneGraphInstant, EventBasedSummary, GoalBasedSummary
from lmp.util import safe_equals as np_safe_equals


def build_event_summaries_with_indices(
        frames: List[SceneGraphInstant],
        event_indices: Sequence[int],  # Indices in frame list, inclusive
) -> List[EventBasedSummary]:
    events = []
    prev_idx = 0
    for index in event_indices:
        events.append(EventBasedSummary(
            scenes=frames[prev_idx:index + 1],
            audio_description=None
        ))
        prev_idx = index + 1
    if prev_idx < len(frames):
        events.append(EventBasedSummary(
            scenes=frames[prev_idx:],
            audio_description=None
        ))
    return events


def build_goal_summaries_with_indices(
        events: List[EventBasedSummary],
        goal_indices: Sequence[int],  # Indices in event list, inclusive
) -> List[GoalBasedSummary]:
    goals = []
    prev_idx = 0
    for index in goal_indices:
        goals.append(GoalBasedSummary(
            events=events[prev_idx:index + 1]
        ))
        prev_idx = index + 1
    if prev_idx < len(events):
        goals.append(GoalBasedSummary(
            events=events[prev_idx:]
        ))
    return goals


_MAX_TIME_DISTANCE_BETWEEN_KEY_FRAMES = timedelta(minutes=2)


def select_keyframe_indices(scenes: List[SceneGraphInstant]) -> List[int]:
    scenes.sort(key=lambda s: s.raw.timestamp)
    keyframe_indices = []
    for i, scene in enumerate(scenes):
        if i + 1 == len(scenes):
            continue
        if (
                # Scene graph change
                set(scene.objects) != set(scenes[i + 1].objects)
                or set(scene.relations) != set(scenes[i + 1].relations)
                # Action change
                or scene.raw.current_action != scenes[i + 1].raw.current_action
                or not np_safe_equals(scene.raw.current_action_parameters, scenes[i + 1].raw.current_action_parameters)
                # ASR event
                or scene.raw.asr_recognition
                # too big time difference
                or scenes[i + 1].raw.timestamp - scene.raw.timestamp > _MAX_TIME_DISTANCE_BETWEEN_KEY_FRAMES
                # add sound
        ):
            keyframe_indices.append(i)
    return keyframe_indices


def select_goal_indices(events: List[EventBasedSummary]) -> List[int]:
    goal_indices = []
    for i, event in enumerate(events):
        if i + 1 == len(events):
            continue
        if event.latest_raw.current_goal != events[i + 1].latest_raw.current_goal:
            goal_indices.append(i)
    return goal_indices


def build_goals_from_hierarchical_goal_items(
        events: List[EventBasedSummary],
) -> List[GoalBasedSummary]:
    return [
        # 10000 to just include the full name for such top-level events
        GoalBasedSummary(events=[g], explicit_goal=_format_hierarchical_goal(g, 10000))
        if isinstance(g, EventBasedSummary)
        else g
        for g in _build_hierarchical_goals(events, 0)
    ]


_MAX_TIME_DISTANCE_TO_GROUP_EVENTS = timedelta(minutes=5)


def _format_hierarchical_goal(item: Union[GoalBasedSummary, EventBasedSummary], stack_idx: int) -> str:
    if item.latest_raw.current_goal is None:
        return None
    goal_name = '.'.join(item.latest_raw.current_goal.split('.')[:stack_idx + 1])
    evt = item.latest_event if isinstance(item, GoalBasedSummary) else item
    if evt.action_parameter_summary:
        param_str = f'({evt.action_parameter_summary})'
    else:
        param_str = ''
    return goal_name + param_str


def _build_hierarchical_goals(
        events: List[EventBasedSummary],
        stack_idx: int,
) -> List[Union[GoalBasedSummary, EventBasedSummary]]:
    goal_stacks = [
        e.latest_raw.current_goal.split('.') if e.latest_raw.current_goal else [] for e in events
    ]
    assert all(stack[:stack_idx] == goal_stacks[0][:stack_idx] for stack in goal_stacks)
    groups = []
    prev_goal_at_idx = None
    for i, event in enumerate(events):
        if len(goal_stacks[i]) <= stack_idx:
            current_goal_at_idx = None
        else:
            current_goal_at_idx = goal_stacks[i][stack_idx]

        if (
                len(groups) == 0
                or prev_goal_at_idx != current_goal_at_idx

                # Events that belong together should not be far away, this is most likely an error
                or event.range[0] - events[i - 1].range[1] > _MAX_TIME_DISTANCE_TO_GROUP_EVENTS
        ):
            groups.append([event])
        else:
            groups[-1].append(event)
        prev_goal_at_idx = current_goal_at_idx

    if len(groups) > 1:
        sub_goals = [
            _build_hierarchical_goals(g, stack_idx + 1)
            for g in groups
        ]
    else:
        sub_goals = groups

    return [
        g[0]
        if len(g) == 1
        else GoalBasedSummary(
            events=g,
            explicit_goal=_format_hierarchical_goal(g[0], stack_idx),
        )
        for g in sub_goals
    ]
