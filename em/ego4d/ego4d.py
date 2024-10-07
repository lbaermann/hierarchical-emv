import json
import pickle
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal, Union, List, Tuple

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate as SystemMsg, HumanMessagePromptTemplate as HumanMsg, \
    AIMessagePromptTemplate as AIMsg
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

from ..em_tree import HigherLevelSummary, EventBasedSummary, SceneGraphInstant, RawDataInstant
from ..em_util import move_history_to_start_date, LazyVideoFramePILImage
from ..rule_based_summary import select_goal_indices, build_goal_summaries_with_indices

_tag_re = re.compile(r'#[a-zA-Z]+')


def _clear_narration_text(t: str):
    return _tag_re.sub('', t).strip()


def _create_convert_to_first_person_chain(llm: BaseChatModel):
    return RunnableParallel({
        'input': lambda d: _clear_narration_text(d['input'])
    }) | (
            SystemMsg.from_template(
                'Convert the following narrations from Ego4D to a first-person past-tense sentences,'
                ' where the camera wearer C is the first person.'
            )
            + HumanMsg.from_template("C rotates round the metal railing")
            + AIMsg.from_template("I rotated round the metal railing")
            + HumanMsg.from_template("man V touches the phone")
            + AIMsg.from_template("man V touched the phone")
            + HumanMsg.from_template("C was in a house and grinded steel balustrade with a angle grinder")
            + AIMsg.from_template("I was in a house and grinded steel balustrade with a angle grinder")
            + HumanMsg.from_template("C looks around the house")
            + AIMsg.from_template("I looked around the house")
            + HumanMsg.from_template("C was in a room with a man X. C and man X played a checkers board game. "
                                     "Man X gave red and blue marble pieces to C.")
            + AIMsg.from_template("I was in a room with a man X. I and man X played a checkers board game. "
                                  "Man X gave red and blue marble pieces to me.")
            + HumanMsg.from_template("{input}")
    ) | llm | StrOutputParser() | RunnableLambda(lambda s: s.strip())


def load_history_from_narrations(ego4d_base_dir: Path, video_id: str,
                                 convert_to_first_person_llm=None,
                                 start_time: datetime = None,
                                 narration_pass: Union[Literal['1', '2']] = '1',
                                 treat_id_as_clip_uid=False) -> HigherLevelSummary:
    if start_time is None:
        start_time = datetime.now()

    video_file = ego4d_base_dir / ('clips' if treat_id_as_clip_uid else 'full_scale') / f'{video_id}.mp4'
    video_narrations, summaries = _get_narrations_and_summaries_for_id(video_id, ego4d_base_dir, narration_pass,
                                                                       clip_mode=treat_id_as_clip_uid)

    if convert_to_first_person_llm is not None:
        first_person_chain = _create_convert_to_first_person_chain(convert_to_first_person_llm)
        chain_narrations = (RunnablePassthrough.assign(input=lambda d: d['narration_text'])
                            | RunnablePassthrough.assign(narration_text=first_person_chain))
        chain_summaries = (RunnablePassthrough.assign(input=lambda d: d['summary_text'])
                           | RunnablePassthrough.assign(summary_text=first_person_chain))
        video_narrations = chain_narrations.batch(video_narrations)
        summaries = chain_summaries.batch(summaries)

    events = []
    for narration in video_narrations:
        ts = narration['timestamp_sec']
        while len(summaries) > 0 and ts > summaries[0]['end_sec']:
            summaries.pop(0)
        # noinspection PyTypeChecker
        events.append(EventBasedSummary(scenes=[SceneGraphInstant(objects=[], relations=[], raw=RawDataInstant(
            timestamp=start_time + timedelta(seconds=ts),
            image=LazyVideoFramePILImage(video_file, frame_second=ts),
            current_action=_clear_narration_text(narration['narration_text']),
            current_goal=_clear_narration_text(summaries[0]['summary_text']) if summaries else None,
        ))]))

    goal_indices = select_goal_indices(events)
    goals = build_goal_summaries_with_indices(events, goal_indices)

    hcap_dir = ego4d_base_dir.parent / 'Ego4D-HCap'
    summary = ''
    if hcap_dir.is_dir():
        hcap_train = json.loads((hcap_dir / 'videos_train.json').read_text())
        hcap_val = json.loads((hcap_dir / 'videos_train.json').read_text())
        for annotation in hcap_train + hcap_val:
            if annotation['vid'] == video_id and annotation['narration_pass'] == narration_pass:
                summary = annotation['video_summary']
                break
        if summary and convert_to_first_person_llm:
            # noinspection PyUnboundLocalVariable
            summary = first_person_chain.invoke({'input': summary})

    return HigherLevelSummary(
        nl_summary=summary,
        children=goals
    )


def _get_narrations_and_summaries_for_id(video_or_clip_uid: str,
                                         ego4d_base_dir: Path,
                                         narration_pass='1',
                                         clip_mode=False) -> Tuple[List[dict], List[dict]]:
    narration_pass = f'narration_pass_{narration_pass}'
    narrations_file = ego4d_base_dir / 'annotations' / 'narration.json'
    narrations = json.loads(narrations_file.read_text())

    if clip_mode:
        clip_id = video_or_clip_uid
        metadata_file = ego4d_base_dir / 'ego4d.json'
        metadata = json.loads(metadata_file.read_text())
        clip = [c for c in metadata['clips'] if c['clip_uid'] == clip_id][0]
        video_id = clip['video_uid']
        start_sec, end_sec = clip['video_start_sec'], clip['video_end_sec']
    else:
        video_id = video_or_clip_uid
        start_sec, end_sec = 0, float('inf')

    video_narrations = narrations[video_id][narration_pass]['narrations']
    summaries = list(narrations[video_id][narration_pass]['summaries'])

    video_narrations = [n for n in video_narrations if start_sec <= n['timestamp_sec'] <= end_sec]
    summaries = [s for s in summaries
                 if s['start_sec'] <= start_sec <= s['end_sec']
                 or s['start_sec'] <= end_sec <= s['end_sec']
                 or start_sec <= s['start_sec'] <= end_sec
                 or start_sec <= s['end_sec'] <= end_sec]  # Any overlap with summary is fine

    summaries.sort(key=lambda x: x['start_sec'])

    # Timestamps always refer to videos. Clips need relative adjustment
    for n in video_narrations:
        n['timestamp_sec'] -= start_sec
    for s in summaries:
        s['start_sec'] -= start_sec
        s['end_sec'] -= start_sec

    return video_narrations, summaries


def load_history_from_video_recap_pickle(pickle_history_file: Path,
                                         convert_to_first_person_llm=None,
                                         start_time: datetime = None):
    first_person_history_file = pickle_history_file.with_suffix('.first_person.pkl')
    if convert_to_first_person_llm is not None and first_person_history_file.is_file():
        history: HigherLevelSummary = pickle.loads(first_person_history_file.read_bytes())
    else:
        history: HigherLevelSummary = pickle.loads(pickle_history_file.read_bytes())

    if convert_to_first_person_llm is not None and not first_person_history_file.is_file():
        captions = [{
            'input': e.latest_raw.current_action,
            'obj': e
        } for g in history.children for e in g.events]
        summaries = [{
            'input': g.latest_raw.current_goal,
            'obj': g
        } for g in history.children]

        first_person_chain = RunnablePassthrough.assign(
            output=_create_convert_to_first_person_chain(convert_to_first_person_llm)
        )
        captions = first_person_chain.batch(captions)
        summaries = first_person_chain.batch(summaries)

        for e in captions:
            e['obj'].latest_raw.current_action = e['output']
        for g in summaries:
            g['obj'].latest_raw.current_goal = g['output']

        history.nl_summary = first_person_chain.invoke({'input': history.nl_summary})['output']

        first_person_history_file.write_bytes(pickle.dumps(history))

    if start_time is not None:
        history = move_history_to_start_date(history, start_time)

    return history


