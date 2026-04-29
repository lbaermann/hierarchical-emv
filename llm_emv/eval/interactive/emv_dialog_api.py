from typing import Dict, Callable

from em.organize.language_rule_relevance import LanguageRuleManager
from lmp.api_visibility_wrapper import group
from lmp.namespace import comment


class EmvDialogAPI:

    def __init__(
            self,
            wait_for_trigger: Callable[[], Dict[str, str]],
            tts: Callable[[str], None],
            emv_model: Callable[[str], str],
            language_rule_manager: LanguageRuleManager
    ) -> None:
        self._tts = tts
        self._wait_for_trigger = wait_for_trigger
        self._emv_model = emv_model
        self._language_rule_manager = language_rule_manager

    @comment('always call this to wait for next command or end the interaction')
    @group('dialog')
    def wait_for_trigger(self) -> Dict[str, str]:
        return self._wait_for_trigger()

    @group('dialog')
    def ask(self, question: str):
        self.say(question)
        while True:
            trigger = self.wait_for_trigger()
            if trigger['type'] == 'dialog':
                return trigger['text']

    @group('dialog')
    def say(self, text: str):
        return self._tts(text)

    @comment("Processes a question about the robot's history and returns an answer. "
             "Make sure to call this instead of hallucinating an answer.")
    @group('dialog')
    def process_history_question(self, question: str) -> str:
        try:
            return self._emv_model(question)
        except:
            return 'ERROR'

    @comment("Processes user feedback about the robot remembering or forgetting some past event not as intended. "
             "Call this if the user complains after an insufficiently/falsely answered history question.")
    @group('dialog')
    def process_forgetting_feedback(self, feedback: str):
        self._language_rule_manager.incorporate_feedback(feedback)
