import re
from datetime import datetime
from typing import Literal, Union

from langchain_core.language_models import BaseLanguageModel

from em.em_tree import HigherLevelSummary, EventBasedSummary, GoalBasedSummary
from llm_emv.emv_api import find_all_predefined_summary_nodes, find_all_parents_of_predefined_summary_nodes
from llm_emv.interactive_tree import format_datetime_range, indent_following_lines
from lmp.util import llm_predict

_zs_flat_prompt = '''You are a humanoid robot agent.
You are given a history that contains information on what the robot did in the past.
Carefully inspect the content of the history to answer the given question.

History: {history}

Question: {question}

Answer:'''

_zs_ego_schema_prompt = '''Answer the given multiple-choice question based on the history of actions.
You are given a history that contains information on what the user did in the past.
Carefully inspect the content of the history to answer the given question.

History:
{history}
Current time: {now}

Question:
{question}

Answer in the following format:
Reasoning: <1-2 sentences>
Answer: <one letter (A, B, C, D or E)>'''

_zs_teach_prompt = '''You are a smart humanoid robot answering user question about your past actions.
You are given a history that contains information on what you did in the past.
Carefully inspect the content of the history to answer the given question.

History:
{history}
Current time: {now}

Question:
{question}

Reasoning: <1-2 sentences>
Answer: <compact answer>'''

_zs_ego4d_prompt = '''You are a smart assistant answering questions about your user's past actions.
You are given a history that contains information on what the user did in the past.
All information is derived automatically from visual input and detections can be noisy, so apply common sense.
Carefully inspect the content of the history to answer the given question.

History:
{history}
Current time: {now}

Question:
{question}

Reasoning: <1-2 sentences>
Answer: <compact answer>'''


class ZeroShotFlatHistoryQA:

    def __init__(self, llm: BaseLanguageModel):
        super().__init__()
        self.llm = llm

    def __call__(self, history_info: str, question: str):
        return llm_predict(self.llm,
                           _zs_flat_prompt.format(history=history_info, question=question))


class ZeroShotOnePassSemiFlatQA:

    def __init__(self, llm: BaseLanguageModel,
                 prompt_name: str = 'ego_schema',
                 now_time: datetime = None,
                 history_levels: Literal[0, 1, 2] = 2,
                 include_lowest_level_details=False,
                 **kwargs):
        super().__init__()
        assert history_levels in [0, 1, 2], str(history_levels)
        self.include_lowest_level_details = include_lowest_level_details
        self.now_time = now_time or datetime.now()
        self.history_levels = history_levels
        self.llm = llm
        self.prompt = {
            'teach': _zs_teach_prompt,
            'ego_schema': _zs_ego_schema_prompt,
            'ego4d': _zs_ego4d_prompt,
            # could add more here
        }[prompt_name]
        self.multiple_choice_mode = {
            'teach': False,
            'ego_schema': True,
            'ego4d': False,
        }[prompt_name]

    def _format_history_l0(self, history: HigherLevelSummary):
        events = _iter_events(history)
        result = ''
        prev = None
        for event in events:
            if prev:
                result += '\n'
            if prev is None or event.range[0].date() != prev.range[1].date():
                result += event.range[0].strftime('%Y/%m/%d %H:%M:%S') + ': '
            elif event.range[0].time().replace(microsecond=0) != prev.range[1].time().replace(microsecond=0):
                result += event.range[0].strftime('%H:%M:%S') + ': '

            if self.include_lowest_level_details:
                result += indent_following_lines(event.nl_summary, 2)
            else:
                result += event.nl_summary.splitlines()[0]
            prev = event

        return result

    def _format_history_l1(self, history: HigherLevelSummary):
        history_str = ''
        for goal in find_all_predefined_summary_nodes(history):
            range_str = format_datetime_range(*goal.range)
            history_str += range_str + ': ' + goal.nl_summary.splitlines()[0] + '\n'
            for event in goal.events:
                if self.include_lowest_level_details:
                    history_str += ' - ' + indent_following_lines(event.nl_summary, 3) + '\n'
                else:
                    history_str += ' - ' + event.nl_summary.splitlines()[0] + '\n'
        return history_str

    def _format_history_l2(self, history: HigherLevelSummary):
        history_str = ''
        for l2_summary in find_all_parents_of_predefined_summary_nodes(history):
            range_str = format_datetime_range(*l2_summary.range)
            history_str += range_str + ': ' + l2_summary.nl_summary + '\n'
            for goal in l2_summary.children:
                range_str = format_datetime_range(*goal.range)
                history_str += ' - ' + range_str + ': ' + goal.nl_summary.splitlines()[0] + '\n'
                for event in goal.events:
                    if self.include_lowest_level_details:
                        history_str += ' -- ' + indent_following_lines(event.nl_summary, 4) + '\n'
                    else:
                        history_str += ' -- ' + event.nl_summary.splitlines()[0] + '\n'
        return history_str

    def __call__(self, history: HigherLevelSummary, question: str):
        if self.history_levels == 0:
            history_str = self._format_history_l0(history)
        elif self.history_levels == 1:
            history_str = self._format_history_l1(history)
        else:
            history_str = self._format_history_l2(history)
        history_str = (history_str
                       .replace('Goal: ', '')
                       .replace('Action: ', ''))

        prompt = self.prompt.format(history=history_str, question=question, now=self.now_time)

        if 'ChatGoogleGenerativeAI' in self.llm.__class__.__name__:
            token_count = self.llm.client.count_tokens({
                'model': self.llm.model,
                'contents': [{'parts': [{
                    'text': prompt
                }]}]
            })
            print('Manual token count estimate:', token_count.total_tokens)

        print('\n==== Prompting: ==== \n', prompt, '\n===============\n')
        response = llm_predict(self.llm, prompt)
        print('LLM Response:\n', response, '\n\n')

        answer_idx = response.rfind('Answer: ')
        if self.multiple_choice_mode:
            match = re.match(r'Answer: ([A-E])', response[answer_idx:])
            if match:
                return match.group(1)
            else:
                return '### No response ###'
        else:
            return response[answer_idx + len('Answer: '):]


def _iter_events(h: Union[HigherLevelSummary, GoalBasedSummary]):
    if isinstance(h, HigherLevelSummary):
        for g in find_all_predefined_summary_nodes(h):
            yield from _iter_events(g)
    else:
        for c in h.events:
            if isinstance(c, EventBasedSummary):
                yield c
            else:
                yield from _iter_events(c)
