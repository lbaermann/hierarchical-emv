import inspect


def comment(c: str):
    """
    Use this as a decorator on a function of an API object to include the given comment as part of the import statement.

    E.g.
    @comment('always call this to wait for next command or end the interaction')
    def wait_for_trigger(self) -> Dict[str, str]:
        ...

    Will yield the import definition:
    def wait_for_trigger() -> Dict[str, str] # always call this to wait for next command or end the interaction
    """

    def _apply(f):
        f.__prompt_comment__ = c
        return f

    return _apply


class DynamicNamespaceDict(dict):

    def __init__(self, api) -> None:
        super().__init__()
        self.api = api
        self.permanent_definitions = {}  # Dynamically defined (e.g. functions, nested LMPs). part of import_statement
        self.predefined_globals = {}  # Something like numpy. Not part of import_statement but available in namespace

    def __missing__(self, key):
        if key in self.predefined_globals:
            return self.predefined_globals[key]
        if key in self.permanent_definitions:
            return self.permanent_definitions[key]
        return getattr(self.api, key)

    def build_import_statement(self, use_defs=False, line_separator='\n', exclude=()):
        names_to_import = (self.permanent_definitions.keys() | set(k for k in dir(self.api)
                                                                   if not ('__' in k or k.startswith('_')))
                           ) - {'exec', 'eval'} - set(exclude)
        names_to_import = sorted(names_to_import)  # For deterministic prompts
        if names_to_import:
            if use_defs:
                imports = []
                function_defs = []
                for n in names_to_import:
                    v = self[n]
                    if callable(v):
                        s: inspect.Signature = inspect.signature(v)
                        if hasattr(v, '__prompt_comment__'):
                            comment = ' # ' + v.__prompt_comment__
                        else:
                            comment = ''
                        function_defs.append(n + str(s).replace('numpy', 'np') + comment)
                    else:
                        imports.append(n)
                import_str = (f'from utils import {", ".join(imports)}' + line_separator) if imports else ''
                return import_str + line_separator + line_separator.join(function_defs) + '\n'
            else:
                return f'from utils import {", ".join(names_to_import)}'
        else:
            return ''

    def build_globals_dict(self):
        names = (self.keys()
                 | set(k for k in dir(self.api) if not ('__' in k or k.startswith('_')))
                 | self.permanent_definitions.keys()
                 | self.predefined_globals.keys()) - {'exec', 'eval', '__builtins__'}
        return {
            n: self[n]
            for n in names
        }
