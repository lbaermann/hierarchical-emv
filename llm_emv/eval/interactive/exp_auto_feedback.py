from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate as SystemMsg, HumanMessagePromptTemplate as HumanMsg, \
    AIMessagePromptTemplate as AIMsg, FewShotChatMessagePromptTemplate
from langchain_core.runnables import RunnableLambda

from .exp_feedback import ExperimentFeedback
from ..qa_eval import EpisodicQAModelOutput


class AlwaysAutoFeedbackProvider:

    def __call__(self, sample: EpisodicQAModelOutput):
        return ExperimentFeedback(proceed=True, feedback=sample.meta['auto_correction'])


class OnlyIfForgottenLLMAutoFeedbackProvider:

    def __init__(self, llm: BaseChatModel):
        super().__init__()
        samples = [
            ("I have already forgotten the specific objects I saw the first time I picked up a bread sliced slice.",
             "FORGOTTEN"),
            ("I did not see any objects the last time I transported a soap bottle.",
             "OTHER"),
            ("I first placed a tomato sliced slice on December 6, 2023, between 11:34 and 11:45.",
             "OTHER"),
            ("The first time I placed a spoon was during kitchen reorganization on November 13th, 2023, but I have "
             "forgotten the exact placement details.",
             "FORGOTTEN"),
            ("I first placed a tomato sliced slice on December 6, 2023, between 11:34 and 11:45.",
             "FORGOTTEN"),
            ("I do not have information about the steps I performed during transport of the bowl, as the relevant "
             "details are either not present or have already been forgotten.",
             "FORGOTTEN"),
            ("I do not know what objects I saw the first time I placed a dishsponge",
             "OTHER"),
        ]
        prompt = (
                SystemMsg.from_template(
                    'We want to classify whether a model response states that certain information was '
                    'forgotten or not. Respond with either FORGOTTEN or OTHER to classify the given output.'
                    'No other output.')
                + FewShotChatMessagePromptTemplate(examples=[dict(input=i, output=o) for i, o in samples],
                                                   example_prompt=(
                                                           HumanMsg.from_template('{input}')
                                                           + AIMsg.from_template('{output}')))
                + HumanMsg.from_template('{input}')
        )
        self.chain = prompt | llm | StrOutputParser() | RunnableLambda(
            lambda s: s.strip()
        )

    def __call__(self, sample: EpisodicQAModelOutput):
        classification = self.chain.invoke(dict(input=sample.hypothesis))
        print(f'Classified "{sample.hypothesis}" as {classification}')
        if classification == 'FORGOTTEN':
            return ExperimentFeedback(proceed=True, feedback=sample.meta['auto_correction'])
        else:
            return ExperimentFeedback(proceed=True, feedback=None)
