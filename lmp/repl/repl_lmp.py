import ast
import traceback
from typing import Union, List, Optional

from langchain.schema.language_model import BaseLanguageModel

from .code_execution import ReplExecutionEnvironment
from .dynamic_prompt import DynamicPromptBuilder, END_OF_TASK
from .error_handlers import ErrorHandler
from .fgen_handler import ReplFunctionGenerationHandler
from .learn_from_interaction import LearnFromInteractionModule
from .llm_to_python_console import LlmToPythonConsoleHelper
from .semantic_hint_errror import SemanticHintError
from .util import ExecutionHistory
from ..lmp import LMPBase


class ReplLMP(LMPBase):

    def __init__(self, llm: BaseLanguageModel,
                 code_execution_env: ReplExecutionEnvironment,
                 prompt_builder: DynamicPromptBuilder,
                 error_handlers: List[ErrorHandler],
                 learn_from_interaction_module: Optional[LearnFromInteractionModule] = None,
                 fgen_lmp=None,
                 llm_to_python_args: dict = None,
                 exclude_imports=(),  # Useful when some dynamic import (e.g. nested LMP) cannot be excluded via api
                 trigger_query_type='dialog',
                 trigger_query_content_key='text',
                 after_first_trigger_force_command=None,  # after initial trigger, this command is executed and inserted
                 max_rounds=100,
                 reset_state_on_result_fn=True,
                 allow_learn_from_interaction_without_user_request=False,
                 verbose=True) -> None:
        super().__init__(llm, code_execution_env)
        self.exec_hist = ExecutionHistory()
        self._fgen_handler = (lambda x: None) if fgen_lmp is None else ReplFunctionGenerationHandler(fgen_lmp)
        self._trigger_query_content_key = trigger_query_content_key
        self._trigger_query_type = trigger_query_type
        self._llm_to_python_helper = LlmToPythonConsoleHelper(self.llm, self.exec_hist, self._build_prompt, verbose,
                                                              **(llm_to_python_args or {}))
        self._exclude_imports = exclude_imports
        self._max_rounds = max_rounds
        self._error_handlers = error_handlers
        self._prompt_builder = prompt_builder
        self._verbose = verbose
        self._reset_state_on_result_fn = reset_state_on_result_fn
        self._allow_learn_from_interaction_without_user_request = allow_learn_from_interaction_without_user_request
        self._after_first_trigger_force_command = after_first_trigger_force_command
        self._learn_from_interaction_handler = learn_from_interaction_module
        if learn_from_interaction_module:
            self.code_execution_env.namespace.predefined_globals[
                'learn_from_interaction'] = self._learn_from_interaction
        self._interrupted = False
        self._currently_executed_statement = None

    def _build_prompt(self, loop_detected=False):
        variable_vars_imports_str = self._create_import_statements()
        base = self._prompt_builder(f'{END_OF_TASK}\n{self.exec_hist}\n', loop_detected)
        base = base.replace('{variable_vars_imports}', variable_vars_imports_str)
        assert base.endswith(END_OF_TASK)
        prompt = (f'{base}\n'
                  f'{self.exec_hist}')
        return prompt

    def _create_import_statements(self):
        variable_vars_imports_str = self.code_execution_env.namespace.build_import_statement(
            use_defs=True, line_separator='\ndef ', exclude=self._exclude_imports)
        return variable_vars_imports_str

    def reset(self):
        self.exec_hist = ExecutionHistory()
        self._interrupted = False
        self.code_execution_env.namespace.clear()  # This only deletes the locals.
        for handler in self._error_handlers:
            handler.reset()

    def interrupt(self):
        if self._currently_executed_statement == END_OF_TASK or self._currently_executed_statement is None:
            return
        self._interrupted = True

    @property
    def currently_executed_statement(self) -> Optional[str]:
        return self._currently_executed_statement

    def __call__(self, query: Union[str, dict]):
        # query str may also be repr of a dict. code below handles this.
        if isinstance(query, str):
            if query.startswith('{'):
                query = ast.literal_eval(query)
            else:
                query = {
                    'type': self._trigger_query_type,
                    self._trigger_query_content_key: query
                }

        query = repr(query)
        self.exec_hist.items.append(ExecutionHistory.ExecutionResult(query))
        if self._after_first_trigger_force_command:
            self.exec_hist.items.append(ExecutionHistory.Command(self._after_first_trigger_force_command))
            results = self.code_execution_env(self._after_first_trigger_force_command)
            for r in results:
                if r is None:
                    continue
                self.exec_hist.items.append(ExecutionHistory.ExecutionResult(repr(r)))
        self.exec_hist.items.append(ExecutionHistory.InputPrompt())
        loop_detected = False
        generation_history = []

        while True:
            if len(generation_history) >= self._max_rounds:
                raise StopIteration('Max rounds reached.')
            if self._interrupted:
                self._interrupted = False
                self.exec_hist.items.append(ExecutionHistory.Command(END_OF_TASK))
                return  # Interrupt does not clear the exec hist. It just causes top-level wait_for_trigger again.

            if isinstance(self.exec_hist.items[-1], ExecutionHistory.InputPrompt):
                code_str, expected_output_str = self._llm_to_python_helper(loop_detected)
                generation_history.append(code_str)
                should_insert_cmd_into_history = True
            elif isinstance(self.exec_hist.items[-1], ExecutionHistory.Command):
                if self._verbose:
                    print('Executing already scheduled code without querying LLM')
                code_str = self.exec_hist.items[-1].code
                should_insert_cmd_into_history = False
            else:
                raise TypeError(type(self.exec_hist.items[-1]))

            if self._detect_generation_loop(generation_history):
                if loop_detected:  # Second time loop => reset and cancel
                    self.reset()
                    self._say('Sorry, I do not know how to proceed.')
                    break
                loop_detected = True
                self.exec_hist.items.append(ExecutionHistory.InputPrompt())  # was just popped before
                continue
            else:
                loop_detected = False

            if should_insert_cmd_into_history:
                # The executed code is added *after* loop detection, since loop detection changes the prompt without
                #  executing the code. If it was inserted earlier, this would look like a statement having no return
                #  value, which the LLM could misunderstand as successful execution
                self.exec_hist.items.append(ExecutionHistory.Command(code_str))

            if len(code_str.splitlines()) == 1 and code_str.strip().startswith('#'):
                self.exec_hist.items.append(ExecutionHistory.InputPrompt())
                continue

            try:
                if self._fgen_handler:
                    self._fgen_handler(self.exec_hist)
                self._currently_executed_statement = code_str
                results = self.code_execution_env(code_str)
                if self._verbose:
                    print('Results:', results)
                for handler in self._error_handlers:
                    handler.reset()
            except StopIteration as e:
                if isinstance(e.value, tuple) and e.value[0] == ReplExecutionEnvironment.RETURN_FN_SIGNAL:
                    if self._reset_state_on_result_fn:
                        self.reset()  # Nested REPL shell should not keep state over different invocations
                    return e.value[1]
                else:
                    raise
            except BaseException as e:
                traceback.print_exc()
                error_message = None
                for handler in self._error_handlers:
                    if handler.can_handle(e):
                        error_message = handler.handle(e)
                        break
                if error_message is not None:
                    self.exec_hist.items.append(ExecutionHistory.ExecutionResult(error_message))
                    self.exec_hist.items.append(ExecutionHistory.InputPrompt())
                    continue
                else:
                    raise

            for r in results:
                if r is None:
                    continue
                self.exec_hist.items.append(ExecutionHistory.ExecutionResult(repr(r)))
            self.exec_hist.items.append(ExecutionHistory.InputPrompt())

    @staticmethod
    def _detect_generation_loop(generation_history):
        if len(generation_history) < 2:
            return False
        most_recent = [generation_history[-1]]
        exact_duplicates = 0
        duplicate_idx = 0
        for x in reversed(generation_history[:-1]):
            if duplicate_idx == len(most_recent):
                duplicate_idx = 0
                exact_duplicates += 1
            if x == most_recent[duplicate_idx]:
                duplicate_idx += 1
            else:
                if duplicate_idx > 0:
                    break  # No subsequent duplicate detected
                else:
                    most_recent.append(x)

        if len(most_recent) == 1 and any(x in most_recent[0] for x in ('say', 'ask')):
            return exact_duplicates >= 1
        else:
            return exact_duplicates >= 2

    def _learn_from_interaction(self, **kwargs):
        directly_following_user_request = (
                isinstance(self.exec_hist.items[-1], ExecutionHistory.Command)  # learn_from_interaction()
                and isinstance(self.exec_hist.items[-2], ExecutionHistory.ExecutionResult)  # user input
                and isinstance(self.exec_hist.items[-3], ExecutionHistory.Command)  # wait_for_trigger()
                and self.exec_hist.items[-3].code.endswith(END_OF_TASK)
        )
        if not self._allow_learn_from_interaction_without_user_request and not directly_following_user_request:
            raise SemanticHintError('Ignoring learn_from_interaction call since it did not happen on explicit user '
                                    'request.')

        interaction = f'>>> {END_OF_TASK}\n{self.exec_hist}'
        if not hasattr(self, '_learn_from_interaction_handler'):
            print('Ignoring learn_from_interaction call since it is not configured properly!')
            return

        improved = self._learn_from_interaction_handler(interaction, self._create_import_statements())
        if improved and isinstance(self._prompt_builder, DynamicPromptBuilder):
            print('Remembering', improved)
            self._prompt_builder.remember_interaction(improved, **kwargs)
            self._say('Thanks, I will try to remember that.')

    def _say(self, msg):
        if hasattr(self.code_execution_env.namespace.api, 'say'):
            self.code_execution_env.namespace.api.say(msg)
        else:
            print('SAY not available! Message:', msg)
