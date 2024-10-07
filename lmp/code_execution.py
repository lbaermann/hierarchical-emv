import re
from dataclasses import dataclass
from types import FunctionType
from typing import Any, Dict

import numpy as np
from regex import regex

from .namespace import DynamicNamespaceDict
from .util import print_code, safe_equals, NoneType

_MAX_DYNAMIC_EXECUTION_RECURSION_DEPTH = 10


@dataclass
class _ExecutionResult:
    return_value: Any
    defined_local_vars: Dict[str, Any]


class CodeExecutionEnvironment:

    def __init__(self,
                 namespace: DynamicNamespaceDict) -> None:
        """
        Create a new code executor.
        """
        super().__init__()
        self.namespace = namespace
        self.recursion_counter = 0

    def is_defined(self, name):
        # noinspection PyBroadException
        try:
            self.namespace[name]
        except:
            return name in __builtins__  # Builtins are always available
        else:
            return True

    def del_dynamic_value(self, name: str):
        del self.namespace[name]

    def __call__(self, code, local_vars_output_dict=None, return_val_name=None, define=False):
        if local_vars_output_dict is None:
            local_vars_output_dict = {}
        result = self._exec_safe_with_recursion_check(code)
        local_vars_output_dict.update(result.defined_local_vars)
        if return_val_name:
            value = local_vars_output_dict[return_val_name]
            if define:
                self.namespace[return_val_name] = value
            return value

    def _exec_safe_with_recursion_check(self, code: str, eval_mode=False) -> _ExecutionResult:
        self.recursion_counter += 1
        if self.recursion_counter > _MAX_DYNAMIC_EXECUTION_RECURSION_DEPTH:
            raise RecursionError(code)
        try:
            return _exec_safe(code, self.namespace.build_globals_dict(), eval_mode)
        except RecursionError as e:
            raise RecursionError(code, *e.args)  # To keep the dynamic code trace
        finally:
            self.recursion_counter -= 1


def _exec_safe(code_str, global_vars=None, eval_mode=False) -> _ExecutionResult:
    if global_vars is None:
        global_vars = {}
    global_vars = _deep_copy_except_complex_types(global_vars)
    global_vars.update(exec=_empty_fn, eval=_empty_fn, compile=_empty_fn)
    # noinspection PyTypeChecker
    global_vars['__builtins__'] = dict(__builtins__)
    global_vars['__builtins__'].update(exec=_empty_fn, eval=_empty_fn, open=_empty_fn,
                                       compile=_empty_fn, input=_empty_fn, exit=_empty_fn,
                                       __import__=_empty_fn)
    global_vars['__builtins__']['__import__'] = None

    code_str = _filter_existing_imports(code_str, global_vars)
    banned_phrases = [r'(^|\W+)import(\W+|$)',  # Regex is there to allow words like "important"
                      '__']  # Remaining imports should raise an error
    for phrase in banned_phrases:
        if re.search(phrase, code_str, re.MULTILINE):
            raise ImportError(code_str)

    # The parameter "locals" for exec/eval is set to none because it has a weird semantic.
    #   see https://docs.python.org/3.10/library/functions.html#exec
    # Instead, everything is written into globals and then extracted from there.
    all_keys_before = set(global_vars.keys())
    primitive_globals_before = {k: v for k, v in global_vars.items() if _is_primitive_value(v)}
    # to properly detect in-place modifications of containers, do a deep copy before
    primitive_globals_before = _deep_copy_except_complex_types(primitive_globals_before)
    function_defs_before = {k: v for k, v in global_vars.items() if isinstance(v, FunctionType)}
    if eval_mode:
        print('\n\n', '=' * 30, '\n\n')
        print('eval', code_str)
        return_value = eval(code_str, global_vars, None)
    else:
        print('\n\n', '=' * 30, '\n\n')
        print_code(code_str)
        exec(code_str, global_vars, None)
        return_value = None

    # Keep variables that appeared newly or changed
    # New values can be anything including functions (to allow dynamic function definitions)
    # Functions are tracked so that self-defined functions can be redefined.
    primitive_globals_after = {k: v for k, v in global_vars.items()
                               if _is_primitive_value(v) and k in primitive_globals_before}
    changed_keys = {k for k in primitive_globals_before.keys()
                    if not safe_equals(primitive_globals_after.get(k), primitive_globals_before[k])
                    } | {k for k in function_defs_before.keys() if global_vars[k] != function_defs_before[k]}
    new_keys = global_vars.keys() - all_keys_before
    local_vars = {}
    for k in new_keys | changed_keys:
        local_vars[k] = global_vars[k]
    print('Updated/Defined variables after execution:', local_vars)

    return _ExecutionResult(return_value, local_vars)


def _filter_existing_imports(code_str: str, global_vars: dict):
    match = regex.search(r'(?:from\s+[\w.]+\s+)?import\s+(\w+)(?:\s*,\s*(\w+))*', code_str)
    while match:
        imported_names = match.captures(1) + match.captures(2)
        if all(name in global_vars for name in imported_names):
            code_str = code_str[:match.start()] + code_str[match.end():]
            print('Dropped already existing imports:', imported_names)
        else:
            return code_str  # This import cannot be replaced...
        match = regex.search(r'(?:from\s+[\w.]+\s+)?import\s+(\w+)(?:\s*,\s*(\w+))*', code_str)
    return code_str


def _is_primitive_value(x):
    if type(x) in [int, float, str, bool, NoneType, np.ndarray]:
        return True
    elif type(x) in [list, tuple, set]:
        return all(_is_primitive_value(y) for y in x)
    elif type(x) == dict:
        return all(_is_primitive_value(k) and _is_primitive_value(v) for k, v in x.items())
    else:
        return False


def _deep_copy_except_complex_types(x):
    if type(x) in [int, float, str, bool, NoneType]:
        return x
    elif type(x) in [list, tuple, set]:
        return type(x)(_deep_copy_except_complex_types(y) for y in x)
    elif type(x) == dict:
        return {_deep_copy_except_complex_types(k): _deep_copy_except_complex_types(v) for k, v in x.items()}
    else:
        return x


def _empty_fn(*args, **kwargs):
    pass
