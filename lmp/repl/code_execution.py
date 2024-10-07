from .dynamic_prompt import WAIT_FOR_USER_INPUT
from ..code_execution import CodeExecutionEnvironment


class ReplExecutionEnvironment(CodeExecutionEnvironment):
    RETURN_FN_SIGNAL = 'repl_return_fn'

    def set_result_function_name(self, result_fn_name: str):
        def result_fn(**kwargs):
            raise StopIteration((ReplExecutionEnvironment.RETURN_FN_SIGNAL, kwargs))

        self.namespace.predefined_globals[result_fn_name] = result_fn

    # noinspection PyMethodOverriding
    def __call__(self, code: str):
        local_vars = {}
        results = []

        def _eval(c: str):
            exec_result = self._exec_safe_with_recursion_check(c, eval_mode=True)
            local_vars.update(exec_result.defined_local_vars)
            results.append(exec_result.return_value)

        try:
            _eval(code)
        except SyntaxError:
            remaining = code.splitlines()
            if WAIT_FOR_USER_INPUT.fullmatch(remaining[-1]):  # full match already assures that it's not nested
                final_line = remaining.pop(-1)
            else:
                final_line = None
            for line in list(remaining):
                try:
                    if not line.strip().startswith('#'):
                        _eval(line)
                    remaining.pop(0)
                except SyntaxError:
                    break
            super().__call__('\n'.join(remaining), local_vars)
            if final_line:
                # A final wait_for_trigger() or ask(...) should always have its result returned visibly
                _eval(final_line)

        # REPL behavior: all local vars set should remain
        for k in local_vars.keys():
            self.namespace[k] = local_vars[k]

        return results
