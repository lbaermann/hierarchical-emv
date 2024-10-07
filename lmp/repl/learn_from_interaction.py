from pathlib import Path

from langchain.chains import ConversationChain
from langchain.chat_models.base import BaseChatModel
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate, \
    MessagesPlaceholder

from ..util import load_chat_messages_from_txt


class LearnFromInteractionModule:

    def __call__(self, interaction_code: str, api_spec: str) -> str:
        raise NotImplementedError


class ChatLearnFromInteractionModule(LearnFromInteractionModule):

    def __init__(self, llm: BaseChatModel, few_shot_example_file: Path):
        self.llm = llm
        self.few_shot_examples = load_chat_messages_from_txt(few_shot_example_file) if few_shot_example_file else []

    def __call__(self, interaction_code: str, api_spec: str):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                'You are a helpful assistant that improves python console transcripts used to control a humanoid '
                'household robot, given the requests or corrections provided by a user.'),
            *self.few_shot_examples,
            HumanMessagePromptTemplate.from_template(f'These are the available APIs:\n\n{api_spec}'),
            HumanMessagePromptTemplate(prompt=PromptTemplate(
                input_variables=[], validate_template=False, template_format='jinja2',
                template=f'I had the following interaction with the robot:\n\n{interaction_code}')),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template('{input}'),
        ])
        chain = ConversationChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
            memory=ConversationBufferMemory(return_messages=True)
        )
        problem_statement = chain.predict(input='What is the problem in this interaction? '
                                                'Answer with a single sentence.')
        print(problem_statement)
        if 'no problem' in problem_statement:
            return None
        print(chain.predict(input='How can the robot do better next time? '
                                  'Answer with a single explanation sentence, no code.'))
        improved_version = chain.predict(
            input='Provide an improved version of the interaction transcript. Your output should be a '
                  'copy of the above interaction (including the python shell syntax) with only slight '
                  'modifications to adjust the behavior appropriately. Do not include another learn_from_interaction '
                  'call. Remember to fix the identified problem.')
        if '```' in improved_version:
            print('Removing non-code parts', improved_version)
            assert improved_version.count('```') == 2
            improved_version = improved_version[improved_version.find('```') + 3:improved_version.rfind('```')].strip()
            print('Removed non-code parts', improved_version)
        if improved_version.splitlines() == interaction_code.splitlines()[:-1]:  # w/o trailing learn_from_interaction()
            print('Improved code is identical to input, ignoring...')
            return None  # Nothing improved.
        return improved_version
