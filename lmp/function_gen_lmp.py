import ast

import astunparse
from langchain.schema.language_model import BaseLanguageModel

from .code_execution import CodeExecutionEnvironment
from .lmp import LMPBase
from .util import llm_predict


class FunctionGenerationLMP(LMPBase):

    def __init__(self, cfg, llm: BaseLanguageModel, code_execution_env: CodeExecutionEnvironment):
        super().__init__(llm, code_execution_env)
        self._cfg = cfg
        self._stop_tokens = list(self._cfg['stop'])
        self._base_prompt = self._cfg['prompt_text']

    def create_f_from_sig(self, f_name, f_sig):
        print(f'Creating function: {f_sig}')

        use_query = f'{self._cfg["query_prefix"]}{f_sig}{self._cfg["query_suffix"]}'
        prompt = f'{self._base_prompt}\n{use_query}'

        f_src = llm_predict(
            self.llm,
            text=prompt,
            stop=self._stop_tokens,
            temperature=self._cfg['temperature'],
            max_tokens=self._cfg['max_tokens']
        ).strip()

        self.code_execution_env(f_src, return_val_name=f_name, define=True)

        return f_src

    def create_new_fs_from_code(self, code_str):
        fs = self._find_function_calls(code_str)

        srcs = {}
        for f_name, f_sig in fs.items():
            if not self.code_execution_env.is_defined(f_name):
                f_src = self.create_f_from_sig(f_name, f_sig)

                # recursively define child_fs in the function body if needed
                f_def_body = astunparse.unparse(ast.parse(f_src).body[0].body)
                child_f_srcs = self.create_new_fs_from_code(f_def_body)

                if len(child_f_srcs) > 0:
                    srcs.update(child_f_srcs)

                    # redefine parent f so newly created child_fs are in scope
                    self.code_execution_env.del_dynamic_value(f_name)
                    f_src = self.create_f_from_sig(f_name, f_sig)

                srcs[f_name] = f_src

        return srcs

    @staticmethod
    def _find_function_calls(code_str):
        fs, f_assigns = {}, {}
        f_parser = FunctionParser(fs, f_assigns)
        f_parser.visit(ast.parse(code_str))
        for f_name, f_assign in f_assigns.items():
            if f_name in fs:
                fs[f_name] = f_assign
        return fs


class FunctionParser(ast.NodeTransformer):

    def __init__(self, fs, f_assigns):
        super().__init__()
        self._fs = fs
        self._f_assigns = f_assigns

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name):
            f_sig = astunparse.unparse(node).strip()
            f_name = astunparse.unparse(node.func).strip()
            self._fs[f_name] = f_sig
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        if isinstance(node.value, ast.Call):
            assign_str = astunparse.unparse(node).strip()
            f_name = astunparse.unparse(node.value.func).strip()
            self._f_assigns[f_name] = assign_str
        return node
