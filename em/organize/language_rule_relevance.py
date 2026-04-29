import json
import traceback
from datetime import datetime
from pathlib import Path
from threading import RLock
from typing import Optional, List

from langchain.output_parsers import OutputFixingParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseOutputParser, NumberedListOutputParser
from langchain_core.output_parsers.base import T
from langchain_core.prompts import SystemMessagePromptTemplate as SystemMsg, HumanMessagePromptTemplate as HumanMsg, \
    PromptTemplate
from wrapt import synchronized

from llm_emv.interactive_tree import format_datetime_range
from .forget import RelevanceEstimator, AnyTreeNodeInclRaw
from ..em_tree import AnyTreeNode, RawDataInstant, SceneGraphInstant


class _RelevanceNumberOutputParser(BaseOutputParser[float]):
    number_keyword: str = 'Number:'

    def parse(self, text: str) -> T:
        text = text.strip()
        start_idx = text.find(self.number_keyword)
        if start_idx > -1:
            text = text[start_idx + len(self.number_keyword):].strip()
        try:
            result = float(text)
        except ValueError:
            raise OutputParserException('Not a valid number', text)
        if result != float('inf') and result != int(result):
            raise OutputParserException('Not a valid integer number', text)
        return result

    def get_format_instructions(self) -> str:
        return f'{self.number_keyword} <int>'


_FIX_RELEVANCE_NUMBER_PROMPT = PromptTemplate.from_template("""
This following output does not follow the format "Reasoning: ... Relevance: <number>" or it is not a valid relevance number.
--------------
{completion}
--------------
Error: {error}

Fix the error. Respond with a valid relevance number, i.e. an integer >= 0 or "inf". 
No other output except valid "Relevance: ..." statement:""".strip())


def _format_dt(dt: datetime):
    return dt.strftime('%Y/%m/%d %H:%M:%S')


class LanguageRuleManager:
    _lock_per_rule_file_path = {}

    def __init__(self,
                 rule_file_path: Path,
                 rule_modifier_llm: BaseChatModel,
                 default_rules=("Do not be reluctant to forget items. If there is no specific rule telling you to "
                                "keep it, or the item is of particular importance, answer with '0'.",),
                 ):
        super().__init__()
        self._default_rules = list(default_rules)
        self._rule_file_path = rule_file_path
        with synchronized(LanguageRuleManager):
            LanguageRuleManager._lock_per_rule_file_path.setdefault(
                str(rule_file_path.resolve()), RLock())

        rule_prompt = (
                SystemMsg.from_template(
                    "You are a smart assistant keeping a history of what happened. The history is limited and old items"
                    " will be forgotten. To value the relevance of what to remember and what to forget, you keep a set"
                    " of rules based on your user's feedback. Currently, you just received some new feedback. Modify"
                    " the rule set according to the feedback by adding, modifying or removing rules. Summarize or"
                    " merge rules that are very similar, without hallucinating too general rules. Rules should be"
                    " simple and concise, following the user feedback, without hallucinating details. Simply copy"
                    " rules that are not related to the feedback (they might still be relevant in another context)."
                )
                + HumanMsg.from_template('Existing set of rules:\n{rules}')
                + HumanMsg.from_template('User feedback: "{feedback}"')
                + HumanMsg.from_template('Produce a modified set of rules as a numbered'
                                         ' list with each item on a new line.')
        )
        self._rule_chain = rule_prompt | rule_modifier_llm | OutputFixingParser.from_llm(
            rule_modifier_llm, NumberedListOutputParser())

    def load_rule_str(self, include_default=True):
        if self._rule_file_path.is_file():
            rules = json.loads(self._rule_file_path.read_text())
            if include_default:
                rules = self._default_rules + rules
        else:
            rules = []
        if rules:
            return '\n\n'.join(f'{i + 1}. {r}' for i, r in enumerate(rules))
        else:
            return '<no rules (yet)>'

    def incorporate_feedback(self, nl_feedback: str):
        with synchronized(LanguageRuleManager):
            lock = LanguageRuleManager._lock_per_rule_file_path[str(self._rule_file_path.absolute())]
        with lock:
            rule_str = self.load_rule_str(include_default=False)
            rules = self._rule_chain.invoke(dict(rules=rule_str, feedback=nl_feedback))
            self._rule_file_path.write_text(json.dumps(rules))


class LanguageRuleBasedRelevanceEstimator(RelevanceEstimator):

    def __init__(self,
                 estimation_llm: BaseChatModel,
                 rule_manager: LanguageRuleManager,
                 forever_time_factor=1e6,
                 ignore_raw_data=False,
                 ):
        super().__init__()
        self._ignore_raw_data = ignore_raw_data
        self._forever_time_factor = forever_time_factor
        self._rule_manager = rule_manager
        value_prompt = (
                SystemMsg.from_template(
                    'You are a smart assistant keeping a history of what happened. The history is limited and old items'
                    ' will be forgotten. Your task is to value the relevance of an item that is expired, in order to'
                    ' decide whether it needs to be retained or can be forgotten. It is important to follow the rules'
                    ' provided by your user to decide on the relevance of an item.'
                    ' The parent item is provided as context only.'
                    ' The default action is to forget (Relevance: 0) if there is no specific rule to keep it.'
                )
                + HumanMsg.from_template('Rules about what is relevant and what not:\n{rules}')
                + HumanMsg.from_template('Item for which the relevance needs to be estimated:\n{item}.\n'
                                         'Additional Context:\n{context}')
                + HumanMsg.from_template('Estimate the relevance of the mentioned experience, i.e. whether it should be'
                                         ' retained longer. A relevance of 0 means that it can be forgotten now.'
                                         ' Higher integer values keep the item for longer. If the item should be kept'
                                         ' forever, answer with "inf".')
                + HumanMsg.from_template('Answer like this:\nReasoning: ...\nRelevance: <number>')
        )
        relevance = OutputFixingParser.from_llm(llm=estimation_llm, prompt=_FIX_RELEVANCE_NUMBER_PROMPT,
                                                parser=_RelevanceNumberOutputParser(number_keyword='\nRelevance:'))
        self._value_relevance_chain = value_prompt | estimation_llm | relevance

    def value(self, node: AnyTreeNodeInclRaw, parent_path: List[AnyTreeNode], now: datetime) -> Optional[int]:
        if self._ignore_raw_data and isinstance(node, RawDataInstant):
            return 0

        rule_str = self._rule_manager.load_rule_str(include_default=True)

        node_str = self._format_node(node)
        parent_node_summary = self._format_node(parent_path[0])
        context_str = f'Parent item: {parent_node_summary}.\nNow: {_format_dt(now)}'

        try:
            result = self._value_relevance_chain.invoke(dict(
                rules=rule_str,
                item=node_str,
                context=context_str,
            ))
        except OutputParserException as e:
            print('Could not parse relevance output for', node_str, context_str, ':', e)
            traceback.print_exc()
            return None
        if result == float('inf'):
            result = self._forever_time_factor
        return int(result)

    async def async_batch_value(self, nodes: List[AnyTreeNodeInclRaw],
                                shared_parent_path: List[AnyTreeNode],
                                now: datetime) -> List[Optional[int]]:
        if len(nodes) == 0:
            return []
        if any(isinstance(n, RawDataInstant) for n in nodes):
            return await super().async_batch_value(nodes, shared_parent_path, now)

        rule_str = self._rule_manager.load_rule_str(include_default=True)
        parent_node_summary = self._format_node(shared_parent_path[0]) if shared_parent_path else '-'
        context_str = f'Parent item: {parent_node_summary}.\nNow: {_format_dt(now)}'

        try:
            results = await self._value_relevance_chain.abatch([dict(
                rules=rule_str,
                item=self._format_node(node),
                context=context_str,
            ) for node in nodes])
        except OutputParserException as e:
            print('Could not parse relevance output for', nodes, context_str, ':', e)
            traceback.print_exc()
            return [None] * len(nodes)
        for i, result in enumerate(results):
            if result == float('inf'):
                results[i] = self._forever_time_factor
        return [int(result) for result in results]

    @staticmethod
    def _format_node(node: AnyTreeNodeInclRaw) -> str:
        if isinstance(node, RawDataInstant):
            items = []
            if node.image is not None:
                items.append('image')
            if node.sound is not None:
                items.append('sound')
            if node.current_action_parameters is not None:
                items.append('detailed action parameters')
            return f'Raw data ({", ".join(items)}) from {_format_dt(node.timestamp)}'

        if isinstance(node, SceneGraphInstant):
            result = f'Scene information at {_format_dt(node.raw.timestamp)}: '
            if node.scene_description:
                result += f'{node.scene_description}. '
            if node.objects or node.relations:
                result += f'{node.nl_graph_summary}. '
            if node.raw.current_action:
                result += f'Ongoing action: {node.raw.current_action}'
                if node.raw.current_action_state:
                    result += f' <{node.raw.current_action_state}>'
                result += '. '
            if node.raw.current_goal:
                result += f'Ongoing goal: {node.raw.current_goal}'
                if node.raw.current_goal_state:
                    result += f' <{node.raw.current_goal_state}>'
                result += '. '
            if node.raw.asr_recognition:
                result += f'ASR: "{node.raw.asr_recognition}". '
            return result.strip()

        return f'{format_datetime_range(*node.range)}: {node.nl_summary}'
