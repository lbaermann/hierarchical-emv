import re
from types import SimpleNamespace
from typing import List, Callable

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from lmp.setup import instantiate_llm


def _parse_example_db(examples: List[str]):
    for example in examples:
        question = re.search('User question: (.*)\n', example).group(1)
        yield dict(question=question,
                   sample=example)


class SimpleFewShotRetriever:

    def __init__(self, top_k=2,
                 sentence_similarity_model='sentence-transformers/all-MiniLM-l6-v2',
                 prompt_db: List[str] = (),
                 question_modifier_llm: dict = None):
        super().__init__()

        example_db = list(_parse_example_db(prompt_db))
        print('Got', len(example_db), 'examples')
        if len(prompt_db) == 0:
            self.example_selector = SimpleNamespace(k=0, select_examples=lambda *args: [])
        else:

            if question_modifier_llm is not None:
                system_prompt = question_modifier_llm.pop('system_prompt')
                prompt = (
                        SystemMessagePromptTemplate.from_template(system_prompt.strip())
                        + HumanMessagePromptTemplate.from_template('{q}')
                )
                self.question_modifier_chain = prompt | instantiate_llm(question_modifier_llm) | StrOutputParser()
                modified_questions = self.question_modifier_chain.batch([
                    dict(q=sample['question']) for sample in example_db
                ])
                for example, mod_q in zip(example_db, modified_questions):
                    example['modified_question'] = mod_q
            else:
                self.question_modifier_chain = None

            embeddings = HuggingFaceEmbeddings(
                model_name=sentence_similarity_model
            )
            self.example_selector = SemanticSimilarityExampleSelector.from_examples(
                examples=example_db,
                input_keys=['question' if question_modifier_llm is None else 'modified_question'],
                embeddings=embeddings,
                k=top_k,
                vectorstore_cls=Chroma,
                collection_name='SimpleFewShotRetriever'  # To not clash with other (in-memory) usages of Chroma
            )

    def __call__(self, question: str) -> List[BaseMessage]:
        if self.example_selector.k == 0:
            return []

        if self.question_modifier_chain is None:
            selector_input = dict(question=question)
        else:
            selector_input = dict(modified_question=self.question_modifier_chain.invoke(question))
        samples = self.example_selector.select_examples(selector_input)

        result = 'Example interactions:\n'
        for sample in samples:
            result += sample["sample"]

        return [HumanMessage(result)]
