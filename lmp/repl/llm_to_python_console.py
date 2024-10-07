from copy import deepcopy
from typing import Tuple, Dict, Any, Callable

from langchain_core.language_models import BaseLanguageModel

from lmp.repl.util import ExecutionHistory
from .dynamic_prompt import WAIT_FOR_USER_INPUT, END_OF_TASK
from ..util import print_prompt, llm_predict, cleanup_model_output, llm_predict_stream


class LlmToPythonConsoleHelper:

    def __init__(self,
                 llm: BaseLanguageModel,
                 exec_hist: ExecutionHistory,
                 build_prompt_fn: Callable[[bool], str],
                 verbose=True,
                 llm_kwargs=None,
                 increase_llm_temp_on_empty_reply=0.3,
                 enforce_python_console_stop_token=True,

                 # Uses stream and cuts output at certain special tokens
                 # that are not represented in a normal "generate" string
                 cut_on_streaming_special_tokens=(),
                 ):
        super().__init__()
        self.llm = llm
        self.exec_hist = exec_hist
        self.build_prompt = build_prompt_fn
        self._llm_kwargs = llm_kwargs or {}
        self._verbose = verbose
        self._cut_on_streaming_special_tokens = cut_on_streaming_special_tokens

        if enforce_python_console_stop_token:
            if 'stop' in self._llm_kwargs:
                if '>>>' not in self._llm_kwargs['stop']:
                    self._llm_kwargs['stop'].append('>>>')
            else:
                self._llm_kwargs['stop'] = ['>>>']

        self._increase_llm_temp_on_empty_reply = increase_llm_temp_on_empty_reply

    def __call__(self, loop_detected_flag=False) -> Tuple[str, str]:  # (code, expected output)
        code_str_with_expected_reply = self._context_length_adaptive_generate(loop_detected_flag)
        code_str, expected_output_str = self._split_llm_output(code_str_with_expected_reply)
        return code_str, expected_output_str

    def _context_length_adaptive_generate(self, loop_detected):
        def _prepare_and_gen():
            prompt = self.build_prompt(loop_detected)
            if self._verbose:
                print_prompt(prompt)
            return self._generate(prompt)

        max_retry = 10
        j = 0
        try:
            while j < max_retry:
                j += 1
                try:
                    return _prepare_and_gen()
                except Exception as e:
                    if 'context_length_exceeded' in str(e):
                        found_any = False
                        for i, item in enumerate(self.exec_hist.items):
                            if (isinstance(item, ExecutionHistory.ExecutionResult)
                                    and item.content != '...'
                                    and isinstance(self.exec_hist.items[i - 1], ExecutionHistory.Command)
                                    and not WAIT_FOR_USER_INPUT.fullmatch(self.exec_hist.items[i - 1].code)):
                                print('Contracting previous execution result', i)
                                item.content = '...'
                                found_any = True
                                break
                        if not found_any:
                            raise ValueError('prompt too long')
                    else:
                        raise
            raise ValueError('prompt too long')
        finally:
            self.exec_hist.items.pop()  # Remove the trailing InputPrompt

    def _generate(self, prompt: str):
        kwargs: Dict[str, Any] = dict(text=prompt, **deepcopy(self._llm_kwargs))

        result = self._generate_increasing_temperature(kwargs)
        if cleanup_model_output(result) == '' and '>>>' in self._llm_kwargs.get('stop', []):
            result = self._generate_relaxing_stop_token(kwargs)

        if cleanup_model_output(result) == '':
            print(f'LLM generated empty reply, substituting this with {END_OF_TASK}')
            return END_OF_TASK
        return result

    def _generate_relaxing_stop_token(self, kwargs):
        print(f'LLM generated empty reply, relaxing stop token')
        kwargs['temperature'] = 0.01
        kwargs['stop'].remove('>>>')
        return self._llm_predict_and_sanitize_code_with_python_console_artifacts(kwargs)

    def _llm_predict_and_sanitize_code_with_python_console_artifacts(self, kwargs):
        print({k: v for k, v in kwargs.items() if k != 'text'})
        if self._cut_on_streaming_special_tokens:
            result = ''.join(llm_predict_stream(self.llm, **kwargs))
            for special_token in self._cut_on_streaming_special_tokens:
                idx = result.find(special_token)
                if idx >= 0:
                    result = result[:idx]
        else:
            result = llm_predict(self.llm, **kwargs).strip()
        result = result.replace('>>>', '', 1)  # Only replace the first one, which is likely the initial statement
        if result.find('>>>') > -1:  # Trim away later statements
            result = result[:result.find('>>>')]
        return result

    def _generate_increasing_temperature(self, kwargs):
        result = ''
        while cleanup_model_output(result) == '':
            if kwargs.get('temperature', 0) > 1:
                break
            result = self._llm_predict_and_sanitize_code_with_python_console_artifacts(kwargs)
            if cleanup_model_output(result) == '':
                if 'temperature' in kwargs:
                    kwargs['temperature'] += self._increase_llm_temp_on_empty_reply
                else:
                    kwargs['temperature'] = self._increase_llm_temp_on_empty_reply
                print(f'LLM generated empty reply, increasing temperature to {kwargs["temperature"]}')
        return result

    def _split_llm_output(self, code_str_with_expected_reply):
        cleanup_code_tags = cleanup_model_output(code_str_with_expected_reply)
        lines = cleanup_code_tags.splitlines()
        if code_str_with_expected_reply != cleanup_code_tags and self._verbose:
            print('Cleaned model output.')
            print('Original:', code_str_with_expected_reply)
            print('Cleaned:', cleanup_code_tags)
        prev_demands_continuation = False
        no_dots_continuation_mode = False
        first_output_idx = len(lines)  # Default in case there is no expected output
        open_parentheses = 0
        for i, line in enumerate(lines):
            if prev_demands_continuation and line.startswith('    '):
                no_dots_continuation_mode = True
            no_dots_continuation_mode = no_dots_continuation_mode and line.startswith('    ')
            if i > 0 and not (prev_demands_continuation or line.startswith('...') or no_dots_continuation_mode):
                first_output_idx = i
                break
            open_parentheses += line.count('(') - line.count(')')
            prev_demands_continuation = line.endswith(':') or line.endswith('\\') or open_parentheses
        code_str_start = lines[0].lstrip(' .') + '\n' * (first_output_idx > 1)
        code_str_exec = code_str_start + '\n'.join(
            x[len('... '):] if x.startswith('...') else x  # Might start with spaces/indent directly
            for x in lines[1:first_output_idx]
        )
        expected_output_str = '\n'.join(lines[first_output_idx:])
        if self._verbose:
            print('command:', code_str_exec)
            print('expected output:', expected_output_str)
        return code_str_exec, expected_output_str
