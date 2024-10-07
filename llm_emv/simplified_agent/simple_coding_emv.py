import traceback
from typing import List

import tiktoken
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

from llm_emv.interactive_tree import ExpandableList, recursive_apply
from llm_emv.simplified_agent.few_shot_retrieval import SimpleFewShotRetriever
from lmp.code_execution import CodeExecutionEnvironment
from lmp.repl.code_execution import ReplExecutionEnvironment
from lmp.repl.error_handlers import ErrorHandler
from lmp.repl.llm_to_python_console import LlmToPythonConsoleHelper
from lmp.repl.util import ExecutionHistory


class SimplifiedCodingEMV:

    def __init__(
            self,
            llm: BaseChatModel,
            prompt_cfg: dict,
            code_exec_env: CodeExecutionEnvironment,
            error_handlers: List[ErrorHandler],
            max_rounds=10,
            exclude_imports=None,
            force_initial_command=None
    ):
        super().__init__()
        self._force_initial_command = force_initial_command
        self._prompt_cfg = prompt_cfg
        self._exclude_imports = exclude_imports or []
        self._max_rounds = max_rounds
        self._error_handlers = error_handlers
        self.llm = llm
        self.code_execution_env = code_exec_env
        self._exec_hist = ExecutionHistory()
        self._tokenizer = tiktoken.encoding_for_model(llm.model_name) if isinstance(llm, ChatOpenAI) else None

        self._retriever = SimpleFewShotRetriever(prompt_db=prompt_cfg.pop('prompt_db', []),
                                                 **prompt_cfg.get('retrieval', {}))
        # noinspection PyTypeChecker
        self._llm_to_python_console_helper = LlmToPythonConsoleHelper(self.llm, self._exec_hist,
                                                                      self._build_prompt_message,
                                                                      enforce_python_console_stop_token=False)

        def _set_simplified_repr(node):
            node._simplified_repr = True

        self._history = self.code_execution_env.namespace.api.history
        recursive_apply(self._history, _set_simplified_repr)

    def _build_prompt_message(self, loop_detected=False):
        question = self._exec_hist.items[0]
        assert isinstance(question, ExecutionHistory.ExecutionResult)

        history_msgs = []
        for i, item in enumerate(self._exec_hist.items[1:]):
            if isinstance(item, ExecutionHistory.Command):
                history_msgs.append(AIMessage(item.code))
            elif isinstance(item, ExecutionHistory.ExecutionResult):
                if not isinstance(item.content, ExpandableList):
                    history_msgs.append(HumanMessage(repr(item.content)))

        user_question_msg = HumanMessage(
            self._prompt_cfg['user_question_prompt'].format(question=question.content)
        )
        state_msg = HumanMessage(
            self._prompt_cfg['history_prompt'].format(history=repr(self._history))
        )
        result = [
            SystemMessage(self._prompt_cfg['final_try_prompt']),
            user_question_msg,
            state_msg,
        ] if loop_detected else [
            SystemMessage(self._prompt_cfg['system_prompt']),
            HumanMessage(
                self.code_execution_env.namespace.build_import_statement(
                    use_defs=True, line_separator='\ndef ', exclude=self._exclude_imports)
            ),
            HumanMessage(self._prompt_cfg['usage_prompt']),
            *self._retriever(question.content),
            user_question_msg,
            *history_msgs,
            state_msg,
        ]
        if self._tokenizer:
            token_count = 3  # every reply is primed with <|start|>assistant<|message|>
            for message in result:
                token_count += 3  # tokens per message
                token_count += len(self._tokenizer.encode(message.content))
            print('Manual token count estimate:', token_count)

        return result

    def __call__(self, question: str):
        self._history.collapse_deep()
        self._exec_hist.items.clear()
        self._exec_hist.items.append(ExecutionHistory.ExecutionResult(question))

        if self._force_initial_command:
            self._exec_hist.items.append(ExecutionHistory.Command(self._force_initial_command))
            results = self.code_execution_env(self._force_initial_command)
            for r in results:
                if r is None:
                    continue
                self._exec_hist.items.append(ExecutionHistory.ExecutionResult(r))

        steps = 0
        no_change_counter = 0
        while True:
            steps += 1
            if steps > self._max_rounds:
                raise StopIteration('Max rounds reached.')

            try:
                self._exec_hist.items.append(ExecutionHistory.InputPrompt())
                code, _ = self._llm_to_python_console_helper(loop_detected_flag=steps == self._max_rounds)
                self._exec_hist.items.append(ExecutionHistory.Command(code))

                previous_history = repr(self._history)
                results = self.code_execution_env(code)
                if (len(results) == 1 and isinstance(results[0], ExpandableList)
                        and repr(self._history) == previous_history):
                    no_change_counter += 1
                    if no_change_counter > 2:
                        results = [
                            'Loop detected. history was reset to expanded state. '
                            'Find the information the user is looking for, and then answer the question.'
                        ]
                        self._history.collapse_deep()
                        self._history.expand()
                    else:
                        results = [
                            'Nothing changed. Ensure the node you are accessing itself is expanded,'
                            ' try a different selector, or expand() without'
                            ' arguments to see all children. Find the information the user is'
                            ' looking for and then answer the question.'
                        ]
                else:
                    no_change_counter = 0

                for handler in self._error_handlers:
                    handler.reset()
            except StopIteration as e:
                if isinstance(e.value, tuple) and e.value[0] == ReplExecutionEnvironment.RETURN_FN_SIGNAL:
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
                    self._exec_hist.items.append(ExecutionHistory.ExecutionResult(error_message))
                    continue
                else:
                    raise

            for r in results:
                if r is None:
                    continue
                self._exec_hist.items.append(ExecutionHistory.ExecutionResult(r))
