import json
import re
from pathlib import Path
from typing import Union, List, Tuple, Optional

from langchain.output_parsers import OutputFixingParser
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import FewShotChatMessagePromptTemplate, HumanMessagePromptTemplate, \
    AIMessagePromptTemplate, SystemMessagePromptTemplate, PromptTemplate

from em.em_tree import HigherLevelSummary, HighestPredefinedSummaryLevel

ItemsToSummarize = Union[HighestPredefinedSummaryLevel, HigherLevelSummary]


def _load_example_db(example_dir: Path):
    for input_file in example_dir.glob('*.input'):
        output_file = input_file.with_suffix('.output')
        if output_file.is_file():
            yield dict(input=input_file.read_text().strip(),
                       output=output_file.read_text().strip())


_FIX_JSON_PROMPT = PromptTemplate.from_template("""
This output is not a valid JSON object.
--------------
{completion}
--------------
Error: {error}

Fix the error. Respond with only a copy of the above JSON object, with errors fixed:""".strip())


class LLMBasedSummarizer:

    def __init__(self,
                 llm: BaseChatModel,
                 similarity_model: str = 'sentence-transformers/all-MiniLM-l6-v2',
                 few_shot_k=2,
                 example_db_name='teach',
                 min_summary_factor_to_allow_single_item_summary=1.5
                 ):
        super().__init__()

        json_fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=JsonOutputParser(), prompt=_FIX_JSON_PROMPT)
        self.min_summary_factor_to_allow_single_item_summary = min_summary_factor_to_allow_single_item_summary
        self._group_and_summarize_chain_first_summary = self._create_group_and_summarize_template(
            few_shot_k, similarity_model, example_db_name, higher_level_summary_mode=False) | llm | json_fixing_parser
        self._group_and_summarize_chain_higher_level = self._create_group_and_summarize_template(
            few_shot_k, similarity_model, example_db_name, higher_level_summary_mode=True) | llm | json_fixing_parser

        simple_prompt = (
                SystemMessagePromptTemplate.from_template(
                    'You are a smart humanoid robot that is supposed to summarize its own actions. '
                    'You receive a list of items that represent what you did in the past. '
                    'Your task is to provide a concise 1-2 sentence summary of your past, '
                    'using first-person perspective.'
                )
                + HumanMessagePromptTemplate.from_template("{input}")
        )
        self._simple_summarize_chain = simple_prompt | llm | StrOutputParser()

        retry_prompt = (
                AIMessagePromptTemplate.from_template('{wrong_output}') +
                HumanMessagePromptTemplate.from_template(
                    'The given output is not valid:\n'
                    '{errors}\n'
                    'Carefully consider the input indices, and the erroneous output. '
                    'Provide an improved JSON that fixes all errors, no other output.'
                )
        )
        self._retry_first_level_chain = (self._create_group_and_summarize_template(
            few_shot_k=0, similarity_model='', example_db_name='',
            higher_level_summary_mode=False) + retry_prompt) | llm | json_fixing_parser
        self._retry_higher_level_chain = (self._create_group_and_summarize_template(
            few_shot_k=0, similarity_model='', example_db_name='',
            higher_level_summary_mode=True) + retry_prompt) | llm | json_fixing_parser

    @staticmethod
    def _create_group_and_summarize_template(few_shot_k: int, similarity_model: str,
                                             example_db_name: str, higher_level_summary_mode: bool):
        example_dir = Path(__file__).parent / 'config' / example_db_name
        lvl_dir_name = 'higher_level' if higher_level_summary_mode else 'first_level'
        if (example_dir / lvl_dir_name).is_dir():
            example_dir = example_dir / lvl_dir_name
        system_template_file = example_dir / 'system_prompt.txt'
        if few_shot_k > 0:
            embeddings = HuggingFaceEmbeddings(
                model_name=similarity_model
            )
            example_db = list(_load_example_db(example_dir))
            print('Loaded', len(example_db), 'examples')
            example_selector = SemanticSimilarityExampleSelector.from_examples(
                examples=example_db,
                input_keys=['input'],
                embeddings=embeddings,
                k=few_shot_k,
                vectorstore_cls=Chroma,
                collection_name='LLMBasedSummarizer'  # To not clash with other (in-memory) usages of Chroma
            )
            few_shot_prompt = FewShotChatMessagePromptTemplate(
                input_variables=["input"],
                example_selector=example_selector,
                example_prompt=(
                        HumanMessagePromptTemplate.from_template("{input}")
                        + AIMessagePromptTemplate.from_template("{output}")
                ),
            )
        else:
            few_shot_prompt = []
        if system_template_file.is_file():
            system_template = system_template_file.read_text().strip()
        else:
            system_template = (
                    'You are a smart humanoid robot that is supposed to summarize its own actions. '
                    'You receive a numbered list of items that represent what you did in the past. ' +
                    (
                        'Each item is a previously generated summary. '
                        if higher_level_summary_mode else
                        'Each item is a high-level action. '
                    ) +
                    'Your task is to identify ranges of items that belong together, and provide a summary for each. ' +
                    (
                        'Consider the dates and times when grouping items, e.g. prefer to group items that happened '
                        'close to each other or in the same hour / on the same day. '
                        if higher_level_summary_mode else ''
                    ) +
                    'The summaries must be consecutive, i.e. there should be no gaps between summaries. '
                    'Respond as JSON with keys "x-y" mapped to string values that contain the corresponding summary. '
                    'Example structure: {"0-6" : "...", "7-9": ..., ...}'
            )
        return (
                SystemMessagePromptTemplate.from_template(
                    system_template,
                    template_format='jinja2'  # Since template contains {}
                )
                + few_shot_prompt
                + HumanMessagePromptTemplate.from_template("{input}")
        )

    @staticmethod
    def _parse_group_and_summarize_output(result: dict, num_items: int) -> Tuple[Optional[dict], List[str]]:
        if not isinstance(result, dict):
            return None, ['Output should be a dict']
        parsed_result = {}
        errors = []
        for key, value in result.items():
            match = re.fullmatch(r'(\d+)(?:\s*-\s*(\d+))?', key)
            if not match:
                errors.append(f'"{key}" does not match pattern "x-y" with ints x, y.')
                continue
            start = int(match.group(1))
            if match.group(2):
                end = int(match.group(2))
            else:
                end = start
            parsed_result[start, end] = value
            if start > end:
                errors.append(f'"{key}": start > end')
                continue
            if end >= num_items:
                errors.append(f'"{key}": end is >= the total number of items ({num_items}).')
                continue

        for i in range(num_items):
            ranges_including_i = sum(1 if i in range(start, end + 1) else 0
                                     for (start, end) in parsed_result.keys())
            if ranges_including_i == 0:
                errors.append(f'Index {i} is not contained in any range.')
            elif ranges_including_i > 1:
                errors.append(f'Index {i} is contained in multiple ranges.')

        return None if errors else parsed_result, errors

    def group_and_summarize(
            self, items: List[ItemsToSummarize]
    ) -> List[HigherLevelSummary]:
        context = self.format_context(items)
        higher_lvl_mode = isinstance(items[0], HigherLevelSummary)
        if higher_lvl_mode:
            result = self._group_and_summarize_chain_higher_level.invoke({'input': context})
        else:
            result = self._group_and_summarize_chain_first_summary.invoke({'input': context})
        print(self, 'group and summarize (higher level:', higher_lvl_mode, ') output:', result)

        parsed_result, errors = self._parse_group_and_summarize_output(result, len(items))
        i = 1
        while errors and i < 3:
            print(self, 'Errors:', errors)
            if higher_lvl_mode:
                chain = self._retry_higher_level_chain
            else:
                chain = self._retry_first_level_chain
            result = chain.invoke({'input': context,
                                   'errors': '\n'.join(f' - {e}' for e in errors),
                                   'wrong_output': json.dumps(result)})
            print(self, 'retry group and summarize (higher level:', higher_lvl_mode, ') output:', result)
            i += 1
            parsed_result, errors = self._parse_group_and_summarize_output(result, len(items))

        if parsed_result is None:
            print('LLM group_and_summarize failed too often!', errors)
            return [self.simple_summarize(items)]

        return [
            (
                HigherLevelSummary(summary, items[start:end + 1])
                if start != end or len(items[start].nl_summary) / len(
                    summary) > self.min_summary_factor_to_allow_single_item_summary
                else items[start]  # Avoid nested structures without any summarization
            )
            for (start, end), summary in parsed_result.items()
        ]

    def simple_summarize(self, items: List[ItemsToSummarize]):
        context = self.format_context(items)
        summary = self._simple_summarize_chain.invoke({'input': context})
        print(self, 'simple summary output', summary)
        return HigherLevelSummary(
            summary, items
        )

    def recursively_summarize(self, items: List[ItemsToSummarize]) -> HigherLevelSummary:
        prev_len = -1
        result = items
        while len(result) > 1:
            if len(result) == prev_len:
                result = [self.simple_summarize(result)]
            else:
                prev_len = len(result)
                result = self.group_and_summarize(result)
        if isinstance(result[0], HigherLevelSummary):
            return result[0]
        else:
            # This is a rare edge case when group_and_summarize has mostly empty events and returns one GoalBasedSummary
            return self.simple_summarize(result)

    @staticmethod
    def format_context(items):
        return '\n'.join(
            f'{i}.\t{item.range[0]} - {item.range[1]}: ' + item.nl_summary.replace("\n", "\n\t")
            for i, item in enumerate(items)
        )
