from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from itertools import chain
from typing import List, Tuple, Optional, Union

import numpy as np
from PIL.Image import Image

from lmp.repl.semantic_hint_errror import SemanticHintError


@dataclass
class RawDataInstant:  # L0
    timestamp: datetime

    # Perception
    image: Optional[Image] = None
    sound: Optional[np.ndarray] = None
    asr_recognition: Optional[str] = None

    # Proprioception
    current_action: Optional[str] = None
    current_action_state: Optional[str] = None
    current_action_parameters: Optional[dict] = None
    current_goal: Optional[str] = None
    current_goal_state: Optional[str] = None
    # TODO add more here...


_original_repr = RawDataInstant.__repr__


def _repr_without_img_details(self: RawDataInstant):
    r = _original_repr(self)
    if self.image is None:
        return r
    img_start = r.find('image=')
    img_end = r.find(', sound=')
    return r[:img_start + len('image=')] + '<PIL.Image.Image ...>' + r[img_end:]


RawDataInstant.__repr__ = _repr_without_img_details


@dataclass(frozen=True)  # To make this hashable
class ObjectNode:
    obj_class: str
    instance_id: str
    state: Optional[str] = None


@dataclass
class SceneGraphInstant:  # L1
    objects: List[ObjectNode]
    relations: List[Tuple[int, int, str]]  # (from idx, to idx, type)
    raw: RawDataInstant

    @property
    def nl_graph_summary(self):
        objects = [f'{o.obj_class} [{o.state}]' if o.state else o.obj_class for o in self.objects]
        # Collect same relations to the same target to compatify representation
        grouped_relations = defaultdict(list)
        for o1, o2, rel in self.relations:
            grouped_relations[o2, rel].append(o1)
        relations = [(
                         f'{self.objects[objs1[0]].obj_class} is'
                         if len(objs1) == 1 else
                         ', '.join(self.objects[o].obj_class for o in objs1) + ' are'
                     ) + f' {rel} {self.objects[o2].obj_class}'
                     for (o2, rel), objs1 in grouped_relations.items()]
        relations_str = '\n'.join(relations)
        if relations_str:
            relations_str = '\n' + relations_str
        if objects or relations_str:
            return (f"Visual observation: {', '.join(objects)}"
                    f"{relations_str}")
        else:
            return ''

    @property
    def index_content(self) -> List[str]:
        return [
            o.obj_class for o in self.objects
        ] + [
            # Objects with state appear twice, to still enable very close match to the object name without state
            f'{o.obj_class} [{o.state}]' for o in self.objects if o.state
        ] + [self.raw.current_action, self.raw.current_goal, self.raw.asr_recognition]

    @property
    def image(self):
        return self.raw.image


@dataclass
class EventBasedSummary:  # L2
    scenes: List[SceneGraphInstant]  # from oldest to newest. the last element is the moment of the event
    audio_description: Optional[str] = None
    action_parameter_summary: Optional[str] = None

    @property
    def latest_scene(self):
        return self.scenes[-1]

    @property
    def latest_raw(self):
        return self.latest_scene.raw

    @property
    def speech_events(self):
        return [(self.latest_raw.timestamp, self.latest_raw.asr_recognition)] if self.latest_raw.asr_recognition else []

    @property
    def image(self):
        return self.latest_raw.image

    @property
    def nl_summary(self):
        action = self.latest_raw.current_action
        action_state = self.latest_raw.current_action_state
        graph = self.latest_scene.nl_graph_summary
        if graph:
            graph = '\n' + graph
        audio = '\nAudio: ' + self.audio_description if self.audio_description else ''
        asr = '\nSpeech: ' + self.latest_raw.asr_recognition if self.latest_raw.asr_recognition else ''
        action_param_str = f'({self.action_parameter_summary})' if self.action_parameter_summary else ''
        action_state_str = f' <{action_state}>' if action_state else ''
        return (f"Action: {action}{action_param_str}{action_state_str}"
                f"{graph}{audio}{asr}.")

    @property
    def range(self):
        return (self.scenes[0].raw.timestamp,
                self.latest_raw.timestamp)

    @property
    def index_content(self) -> List[str]:
        return list(chain(*(s.index_content for s in self.scenes))) + [self.audio_description,
                                                                       self.action_parameter_summary]


@dataclass
class GoalBasedSummary:  # L3
    # from oldest to newest. the last element is where the goal was reached/failed
    events: List[Union[EventBasedSummary, 'GoalBasedSummary']]

    # This is optional and will "overwrite" the current_goal from the latest RawDataInstant
    explicit_goal: Optional[str] = None

    @property
    def latest_event(self):
        return self.events[-1]

    @property
    def latest_scene(self):
        return self.latest_event.latest_scene

    @property
    def latest_raw(self):
        return self.latest_scene.raw

    @property
    def speech_events(self):
        return list(chain(*(
            child.speech_events for child in self.events
        )))

    def __getattr__(self, item):
        if item == 'image':
            raise SemanticHintError('Goal summaries do not have an image. '
                                    'Use its child nodes to access observed images.')
        raise AttributeError(f"'GoalBasedSummary' object has no attribute '{item}'")

    @property
    def nl_summary(self):
        goal = self.explicit_goal or self.latest_raw.current_goal
        audio = '\n'.join(e.audio_description for e in self.events
                          if hasattr(e, 'audio_description') and e.audio_description)
        asr = '\n'.join(f'{ts}: {speech}'
                        for ts, speech in self.speech_events)
        result = f"Goal: {goal}"
        goal_state = self.latest_raw.current_goal_state
        if goal_state and not goal_state.lower().startswith('succe'):  # successful, succeeded etc
            result += f' <{goal_state}>'
        graph = self.latest_scene.nl_graph_summary
        if graph:
            result += '\n' + graph
        if audio:
            result += '\n' + audio
        if asr:
            result += '\nSpeech:\n' + asr
        return result

    @property
    def range(self):
        return (self.events[0].range[0],
                self.events[-1].range[-1])

    @property
    def index_content(self) -> List[str]:
        return list(chain(*(e.index_content for e in self.events))) + [self.explicit_goal]


HighestPredefinedSummaryLevel = GoalBasedSummary


@dataclass
class HigherLevelSummary:
    nl_summary: str
    children: List[Union[HighestPredefinedSummaryLevel, 'HigherLevelSummary']]

    @property
    def range(self):
        return (self.children[0].range[0],
                self.children[-1].range[-1])

    @property
    def index_content(self) -> List[str]:
        return [self.nl_summary] + list(chain(*(c.index_content for c in self.children)))

    def __getattr__(self, item):
        if item == 'image':
            raise SemanticHintError('Higher level summaries do not have an image. '
                                    'Use its lower-level child nodes to access observed images.')
        raise AttributeError(f"'HigherLevelSummary' object has no attribute '{item}'")


type_to_children_property_map = {
    HigherLevelSummary: 'children',
    GoalBasedSummary: 'events',
    EventBasedSummary: 'scenes'
}

AnyTreeNode = Union[
    HigherLevelSummary,
    GoalBasedSummary,
    EventBasedSummary,
    SceneGraphInstant
]
