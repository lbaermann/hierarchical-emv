import math
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, Tuple

from armarx_memory.ltm.base.entity_instance import EntityInstance
from armarx_memory.ltm.memory_server import MemoryServer
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate as HumanMsg, \
    AIMessagePromptTemplate as AIMsg
from langchain_core.runnables import RunnableParallel
from tqdm import tqdm

from .em_tree import HigherLevelSummary, RawDataInstant, SceneGraphInstant, ObjectNode, GoalBasedSummary
from .llm_summary import LLMBasedSummarizer
from .rule_based_summary import select_keyframe_indices, build_event_summaries_with_indices, \
    build_goals_from_hierarchical_goal_items


def _iter_all_instances(
        mem_server: MemoryServer,
        memory_name: str,
        core_segment_name: str,
        provider_name=None,
        start_from_timestamp_s_since_epoch: float = None,
) -> Iterator[EntityInstance]:
    start_from_timestamp_microseconds = int(start_from_timestamp_s_since_epoch * 1e6)
    core_segment = mem_server.memories[memory_name].coreSegments[core_segment_name]
    if provider_name:
        provider_segments = [core_segment.providerSegments[provider_name]]
    else:
        provider_segments = core_segment.providerSegments.values()
    for p in provider_segments:
        for e in p.entities.values():
            for s in e.snapshots.values():
                for i in s.instances:
                    if i.metadata.timeReferenced >= start_from_timestamp_microseconds:
                        i.load()
                        yield i


def _create_summarize_parameters_chain(llm: BaseChatModel):
    # Since template contains {}
    f = dict(template_format='jinja2')
    prompt = (
            SystemMessagePromptTemplate.from_template(
                'You are a smart humanoid robot that is supposed to summarize its own actions. '
                'You receive a record of an executed skill. Each skill has a name and a dictionary of parameters. '
                'Some parameters are very low-level and not interesting to the user, while others are important to '
                'understand what action was actually executed. Your job is to filter the given parameters to only keep '
                'the essential ones. It is ok to simplify the parameter names and values as appropriate.\n'
                'Respond with a comma-separated mapping of key=value pairs of only the '
                'essential parameters of the skill. If there is no relevant parameter, respond with "-".'
            )
            + HumanMsg.from_template(
        "LoadDishwasher\n{'graspObjectAtLocation': '', 'includeClosingDishwasher': True, 'includeOpeningDishwasher': "
        "True, 'includePlaceObjectInDishwasher': True, 'motionGenerationMethod': 1, 'navigateToDishwasherLocation': "
        "'MobileKitchen/Kitchen/mobile-dishwasher/OpenDishwasher:0', 'navigateToHandoverLocation': '', "
        "'objectPlacementMethod': 0, 'objectRetrievalMethod': 3}",
        **f)
            + AIMsg.from_template("close=True, open=True, placeObject=True, "
                                  "dishwasherLocation=mobile-dishwasher/OpenDishwasher:0")
            + HumanMsg.from_template("HandOverObjectToHuman\n{'arm': 0}", **f)
            + AIMsg.from_template("arm=0")
            + HumanMsg.from_template("LookAhead\n{'agent': 'Armar7', 'frame': 'root', 'priority': 1.0}", **f)
            + AIMsg.from_template("-")
            + HumanMsg.from_template(
        "Introduction.MoveJointsToNamedConfiguration\n{'accuracy': 0.05000000074505806, 'accuracyOverride': {"
        "'LeftHandFingers': 0.10000000149011612, 'LeftHandIndex': 0.10000000149011612, 'LeftHandThumbCircumduction': "
        "0.10000000149011612, 'LeftHandThumbFlexion': 0.10000000149011612, 'RightHandFingers': 0.10000000149011612, "
        "'RightHandIndex': 0.10000000149011612, 'RightHandThumbCircumduction': 0.10000000149011612, "
        "'RightHandThumbFlexion': 0.10000000149011612}, 'configuration': 'Introduction_WavePose1', 'disabledJoints': "
        "[], 'enableHead': false, 'enableLeftArm': true, 'enableLeftHand': true, 'enableRightArm': true, "
        "'enableRightHand': true, 'enableTorso': false, 'inSimulation': false, 'simulationJointSpeed': "
        "0.3499999940395355, 'simulationJointSpeedOverride': {}}",
        **f)
            + AIMsg.from_template("configuration=Introduction_WavePose1")
            + HumanMsg.from_template("{action}\n{params}")
    )
    return RunnableParallel({
        'action': lambda evt: evt.latest_raw.current_action,
        # not using json to handle np array
        'params': lambda evt: (repr(evt.latest_raw.current_action_parameters.get('parameters', {}))
                               if evt.latest_raw.current_action_parameters else '{}'),
    }) | prompt | llm | StrOutputParser()


def _parse_location_to_obj_id_and_rel_name(location_name: str) -> Tuple[str, str]:
    at_parts = location_name.split('/')
    if len(at_parts) == 2:  # pure location, e.g. MobileKitchen/fridge:0 or R007/center
        return at_parts[1].replace(':', '_'), 'at'

    # object-relative locations, e.g.
    # Kitchen/mobile-kitchen-counter/in-sink:0
    # Kitchen/mobile-kitchen-counter/on-counter:0
    # MobileKitchen/Kitchen/fridge/inFrontOf:0
    final_parts = at_parts[-1].split(':')
    obj_inst_idx = final_parts[-1] if len(final_parts) > 1 else 0
    tgt_obj_class = at_parts[-2]
    if '-' in final_parts[0]:
        relation_split = final_parts[0].split('-')
        if relation_split[1] in tgt_obj_class:
            relation_name = relation_split[0]  # -> on mobile-kitchen-counter
        else:
            relation_name = f'{relation_split[0]} {relation_split[1]} of'  # -> in sink of mobile-kitchen-counter
    else:
        relation_name = final_parts[0]
    return f'{tgt_obj_class}_{obj_inst_idx}', relation_name


def _parse_obj_name_to_id(obj_name: str) -> str:
    id_parts = obj_name.split('/')
    if len(id_parts) > 2:
        obj_cls = id_parts[-2]
        instance_idx = id_parts[-1]
    else:
        obj_cls = id_parts[-1]
        instance_idx = 0
    return f'{obj_cls}_{instance_idx}'


def _parse_symbolic_scene(scene: dict):
    objects, relations = [], []

    def _find_or_add_obj(_obj_id):
        found_obj_idx = None
        for i, existing_obj in enumerate(objects):
            if existing_obj.instance_id == _obj_id:
                return i
        if found_obj_idx is None:
            objects.append(ObjectNode(_obj_id.split('_')[0], instance_id=_obj_id))
            return len(objects) - 1

    # First find all objects
    for obj in scene['objects'].values():
        obj_id = _parse_obj_name_to_id(obj['id'])
        _find_or_add_obj(obj_id)

    # Then add relations
    for obj in scene['objects'].values():
        if not obj.get('objectAt') or obj['objectAt'] == '(unknown)':
            continue
        obj_id, rel_name = _parse_location_to_obj_id_and_rel_name(obj['objectAt'])
        relations.append((_find_or_add_obj(_parse_obj_name_to_id(obj['id'])), _find_or_add_obj(obj_id), rel_name))

    # Robot location also added as relation
    for robot in scene['robots'].values():
        obj_id, rel_name = _parse_location_to_obj_id_and_rel_name(robot['robotAt'])
        relations.append((_find_or_add_obj(robot['name']), _find_or_add_obj(obj_id), rel_name))

    return objects, relations


def _is_end_state(state: str):
    return state in ['Succeeded', 'Aborted', 'Failed']


def load_episode_from_armarx_lt_mem(
        mem_export_dir: Path,
        action_param_summarizer_llm: BaseChatModel = None,
        start_from_timestamp: datetime = None,
) -> HigherLevelSummary:
    if start_from_timestamp is None:
        start_from_timestamp = float('-inf')
    else:
        start_from_timestamp = start_from_timestamp.timestamp()
    memory = MemoryServer(str(mem_export_dir.parent), mem_export_dir.name)
    memory.loadReferences()
    asr_entries = list(_iter_all_instances(memory, 'Speech', 'SpeechToText',
                                           start_from_timestamp_s_since_epoch=start_from_timestamp))
    tts_entries = list(_iter_all_instances(memory, 'Speech', 'TextToSpeech',
                                           start_from_timestamp_s_since_epoch=start_from_timestamp))
    skill_events = list(_iter_all_instances(memory, 'Skill', 'SkillEvent',
                                            start_from_timestamp_s_since_epoch=start_from_timestamp))
    sym_scene_snapshots = list(_iter_all_instances(memory, 'SymbolicScene', 'SymbolicSceneDescription',
                                                   start_from_timestamp_s_since_epoch=start_from_timestamp))
    sym_scene_snapshots.sort(key=lambda evt: evt.metadata.timeReferenced)
    skill_events.sort(key=lambda evt: evt.metadata.timeReferenced)
    used_sym_scene_indices = []

    scenes = []
    running_goal = ''  # This is only there to handle actions with no executorName provided
    for skill_evt_inst in skill_events:
        skill_evt = skill_evt_inst.data.to_primitive()
        ts = datetime.fromtimestamp(skill_evt_inst.metadata.timeReferenced / 1e6)
        action = skill_evt['skillId']['skillName']
        if action == 'ResetGazeTargets':
            continue  # ResetGazeTargets is only a hack that is frequently called by other skills
        action_state = skill_evt['status']
        if action_state in ['Constructing', 'Initializing']:
            continue  # Ignore these uninformative states, they are sometimes even missing
        executor_path = skill_evt['executorName'].split('->')
        for i, e in enumerate(executor_path):
            if i == 0 and e.startswith('Armar7Demo'):
                executor_path[0] = 'user speech command'
            elif i == 0 and e.startswith('Skills.Manager GUI'):
                executor_path[0] = 'GUI'
            elif '/' in e:
                executor_path[i] = e.split('/')[1]
        if len(executor_path) >= 1 and executor_path[0].strip():
            current_path = executor_path[1:] + [action]
            running_goal = '.'.join(current_path)
            goal = running_goal
        else:
            goal = running_goal + '.' + action
        executor_name = '->'.join(executor_path)
        prev_sym_scene_idx = max((i for i, s in enumerate(sym_scene_snapshots)
                                  if s.metadata.timeReferenced <= ts.timestamp() * 1e6),
                                 default=None)
        if prev_sym_scene_idx is None:
            objects, relations = [], []
        else:
            prev_sym_scene = sym_scene_snapshots[prev_sym_scene_idx]
            used_sym_scene_indices.append(prev_sym_scene_idx)
            objects, relations = _parse_symbolic_scene(prev_sym_scene.data.to_primitive())
        scenes.append(SceneGraphInstant(
            objects=objects,
            relations=relations,
            raw=RawDataInstant(
                ts, current_action=f"{action}",
                current_action_state=action_state,
                current_action_parameters={'parameters': skill_evt['parameters'],
                                           'trigger': executor_name},
                current_goal=goal,
                current_goal_state=action_state
            )
        ))

    for j, scene_snap in enumerate(sym_scene_snapshots):
        if j in used_sym_scene_indices:
            continue
        ts = datetime.fromtimestamp(scene_snap.metadata.timeReferenced / 1e6)

        if len(scenes) == 0:
            prev_scene_idx = None
        elif scenes[-1].raw.timestamp < ts:  # scene_snap is after all existing entries
            prev_scene_idx = len(scenes) - 1
        elif ts < scenes[0].raw.timestamp:  # scene_snap is before all existing entries
            prev_scene_idx = None
        else:  # scene_snap is somewhere in between
            prev_scene_idx = max(i for i, s in enumerate(scenes) if s.raw.timestamp < ts)

        if prev_scene_idx is None:
            raw = RawDataInstant(ts)  # Nothing to copy from
            prev_scene_idx = 0
        else:
            prev_scene = scenes[prev_scene_idx]
            copy = dict(prev_scene.raw.__dict__) if prev_scene else {}
            if prev_scene.raw.current_action_state and _is_end_state(prev_scene.raw.current_action_state):
                copy.update(current_action=None, current_action_state=None, current_action_parameters={})
            if prev_scene.raw.current_goal_state and _is_end_state(prev_scene.raw.current_goal_state):
                new_goal, new_state = None, None
                if prev_scene.raw.current_goal:
                    parts = prev_scene.raw.current_goal.split('.')
                    if parts[-1] == prev_scene.raw.current_action and len(parts) > 1:  # Hierarchical sub-goal finished
                        new_goal = '.'.join(parts[:-1])
                        new_state = 'Running'
                copy.update(current_goal=new_goal, current_goal_state=new_state)
            copy['timestamp'] = ts
            raw = RawDataInstant(**copy)
        objects, relations = _parse_symbolic_scene(scene_snap.data.to_primitive())
        scenes.insert(prev_scene_idx, SceneGraphInstant(
            objects=objects, relations=relations, raw=raw,
        ))

    scenes.sort(key=lambda s: s.raw.timestamp)  # Should already be sorted, but just to make sure

    # ASR entries are either mapped to close existing scene, or create a new scene copying the previous contents
    max_delta_to_merge_asr_into_scene = timedelta(seconds=1)
    max_delta_to_copy_action_goal_to_asr = timedelta(seconds=10)
    for speech_recognition in asr_entries:
        ts = datetime.fromtimestamp(speech_recognition.metadata.timeReferenced / 1e6)
        text = speech_recognition.data.to_primitive()['text']
        subsequent_scene_idx = min((i for i, scene in enumerate(scenes)
                                    if scene.raw.timestamp >= ts),
                                   default=None)
        if (subsequent_scene_idx is None
                or scenes[subsequent_scene_idx].raw.timestamp - ts > max_delta_to_merge_asr_into_scene):
            prev_scene = scenes[max(0, subsequent_scene_idx - 1)] if subsequent_scene_idx is not None else scenes[-1]
            if ts - prev_scene.raw.timestamp > max_delta_to_copy_action_goal_to_asr:
                copy = dict()
            else:
                copy = dict(prev_scene.raw.__dict__)
            copy['timestamp'] = ts
            copy['asr_recognition'] = text
            scenes.append(SceneGraphInstant(
                objects=prev_scene.objects, relations=prev_scene.relations,
                raw=RawDataInstant(**copy),
            ))
            scenes.sort(key=lambda s: s.raw.timestamp)
        else:
            scenes[subsequent_scene_idx].raw.asr_recognition = text

    # TTS entries might already be present as Say(...) skill invocations. Add them if not.
    # There should not be more than 5 ms between Say skill event and TTS event
    max_delta_to_count_as_same_tts = timedelta(microseconds=5000)
    for tts_entry in tts_entries:
        ts = datetime.fromtimestamp(tts_entry.metadata.timeReferenced / 1e6)
        text = tts_entry.data.to_primitive()['text']
        if not text:
            continue
        found_tts = False
        for scene in scenes:
            if (
                    scene.raw.current_action == "Say"
                    and scene.raw.current_action_parameters.get('text') == text
                    and abs(scene.raw.timestamp - ts) <= max_delta_to_count_as_same_tts
            ):
                found_tts = True
                break
        if found_tts:
            continue
        prev_scene_idx = max((i for i, scene in enumerate(scenes)
                              if scene.raw.timestamp < ts),
                             default=None)
        if prev_scene_idx is None:
            objects, relations, goal, goal_state = [], [], "Say", "Succeeded"
        else:
            prev_scene = scenes[prev_scene_idx]
            objects, relations = prev_scene.objects, prev_scene.relations
            goal, goal_state = prev_scene.raw.current_goal, prev_scene.raw.current_goal_state
        scenes.append(SceneGraphInstant(
            objects=objects, relations=relations,
            raw=RawDataInstant(timestamp=ts, current_action="Say", current_action_state="Succeeded",
                               current_action_parameters={'parameters': {'text': text}},
                               current_goal=goal, current_goal_state=goal_state),
        ))
        scenes.sort(key=lambda s: s.raw.timestamp)

    event_indices = select_keyframe_indices(scenes)
    events = build_event_summaries_with_indices(scenes, event_indices)

    if action_param_summarizer_llm is not None:
        summarizer = _create_summarize_parameters_chain(action_param_summarizer_llm)
        # Since many action/parameters might repeat, use smaller batch size to get cache hits (in case llm is cached)
        #  This also enables using a progress bar
        results = []
        bsz = 32
        with tqdm(range(math.ceil(len(events) / bsz))) as pbar:
            for i in pbar:
                results += summarizer.batch(events[i * bsz:(i + 1) * bsz])
        for event, summary in zip(events, results):
            if event.latest_raw.current_action and event.latest_raw.current_action_parameters:  # Ignore No-op events
                event.action_parameter_summary = summary.strip('-')

    goals = build_goals_from_hierarchical_goal_items(events)

    return HigherLevelSummary(
        nl_summary='',
        children=goals
    )


def extend_existing_history_from_memory_snapshots(
        existing_history: HigherLevelSummary,
        mem_export_dir: Path,
        action_param_summarizer_llm: BaseChatModel = None,
        llm_history_summarizer: LLMBasedSummarizer = None,
) -> HigherLevelSummary:
    # This method has the following assumptions:
    #   1. the top level summary has no / non-informative text
    #   2. there is one top-level child for each day.
    #   3. the last top-level child is the summary of the current day.
    #   4. New L3 nodes are loaded from the given mem export dir (starting from the end of the existing history).
    #      These are assumed to be on the same and/or a new day. This method will split them up and append same-day L3
    #      nodes to the existing last top-level child, and new-day L3 nodes will be appended to a newly created
    #      top-level child. It will then optionally summarize the previous one, if llm_history_summarizer is given.
    #   4. the last top-level node for the current day has no informative text.

    existing_history = deepcopy(existing_history)
    current_end_ts = existing_history.range[1]

    new_l3_nodes = load_episode_from_armarx_lt_mem(mem_export_dir, action_param_summarizer_llm,
                                                   start_from_timestamp=current_end_ts).children
    assert all(n.range[0].date() == n.range[1].date() for n in new_l3_nodes), 'L3 nodes may not span day boundary'
    same_day = [n for n in new_l3_nodes if n.range[0].date() == current_end_ts.date()]
    new_day = [n for n in new_l3_nodes if n.range[0].date() > current_end_ts.date()]
    assert len(set(n.range[0].date() for n in new_day)) == 1, 'Adding more than one day at once is not supported'

    if same_day:
        assert isinstance(existing_history.children[-1], HigherLevelSummary), (
            'Last child must be summary')
        assert existing_history.children[-1].range[0].date() == current_end_ts.date(), (
            'Last child may not span multiple days')
        existing_history.children[-1].children += same_day

    if new_day:
        # Only summarize previous day if
        #   1) summarizer is given and
        #   2) the previous last top-level child is not already a summarized history,
        #      as indicated by it having higher level children
        prev_day_nodes = existing_history.children[-1].children
        if llm_history_summarizer and all(isinstance(n, GoalBasedSummary) for n in prev_day_nodes):
            prev_day_summary = llm_history_summarizer.recursively_summarize(prev_day_nodes)
            existing_history.children[-1] = prev_day_summary

        existing_history.children.append(HigherLevelSummary(
            nl_summary='',
            children=new_day
        ))

    return existing_history
