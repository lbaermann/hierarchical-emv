import inspect

from langchain.schema.language_model import BaseLanguageModel

from .code_execution import CodeExecutionEnvironment
from .namespace import comment
from .util import llm_predict


class LMPBase:

    def __init__(self, llm: BaseLanguageModel, code_execution_env: CodeExecutionEnvironment) -> None:
        super().__init__()
        self.llm = llm
        self.code_execution_env = code_execution_env


class LMP(LMPBase):

    def __init__(self, cfg, lmp_fgen, llm: BaseLanguageModel, code_execution_env: CodeExecutionEnvironment):
        super().__init__(llm, code_execution_env)
        self._cfg = cfg
        self._base_prompt = self._cfg['prompt_text']
        ctxt = self._cfg['context_vars']
        if ctxt:
            context_functions = [
                (n, self.code_execution_env.namespace[fn_name])
                for n, fn_name in ctxt.items()
            ]
            self._context_provider = lambda: '\n'.join(f'{n} = {fn()}'
                                                       for n, fn in context_functions)
        else:
            self._context_provider = lambda: ''
        self._stop_tokens = list(self._cfg['stop'])
        self._lmp_fgen = lmp_fgen
        self.exec_hist = ''

        if 'signature' in self._cfg:
            sign_cfg = self._cfg['signature']
            # Signature & Comment are applied to self instead of self.__call__
            #   as the LMP acts as the Callable object itself.
            self.__signature__ = inspect.Signature([
                inspect.Parameter(p['name'], kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=p['type'])
                for p in sign_cfg['parameters']
            ], return_annotation=sign_cfg.get('return', None))
            if 'comment' in sign_cfg:
                comment(sign_cfg['comment'])(self)

    def clear_exec_hist(self):
        self.exec_hist = ''

    def build_prompt(self, query, context=''):
        variable_vars_imports_str = self.code_execution_env.namespace.build_import_statement()
        prompt = self._base_prompt.replace('{variable_vars_imports}', variable_vars_imports_str)

        if self._cfg['maintain_session'] and self.exec_hist.strip():
            prompt += f'\n{self.exec_hist}'

        if context != '':
            prompt += f'\n{context}'

        use_query = f'{self._cfg["query_prefix"]}{query}{self._cfg["query_suffix"]}'
        prompt += f'\n{use_query}'

        return prompt, use_query

    def __call__(self, query, context=None):
        if context is None:
            context = self._context_provider()
        prompt, use_query = self.build_prompt(query, context=context)

        print('', '=' * 20, prompt, '=' * 20, '', sep='\n\n')
        code_str = llm_predict(
            self.llm,
            text=prompt,
            stop=self._stop_tokens,
            temperature=self._cfg['temperature'],
            max_tokens=self._cfg['max_tokens']
        ).strip()

        if self._cfg['include_context'] and context != '':
            to_exec = f'{context}\n{code_str}'
        else:
            to_exec = code_str

        print('output:', code_str)
        self._lmp_fgen.create_new_fs_from_code(code_str)

        return_val_name = self._cfg.get('return_val_name')
        return_val = self.code_execution_env(to_exec, return_val_name=return_val_name)

        self.exec_hist += f'\n{to_exec}'

        if return_val_name:
            return return_val
