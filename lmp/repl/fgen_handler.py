from .util import ExecutionHistory
from ..function_gen_lmp import FunctionGenerationLMP


class ReplFunctionGenerationHandler:

    def __init__(self, fgen_lmp: FunctionGenerationLMP):
        super().__init__()
        self._fgen_lmp = fgen_lmp

    def __call__(self, execution_history: ExecutionHistory):
        last_command = execution_history.items.pop()
        assert isinstance(last_command, ExecutionHistory.Command)

        try:  # The try/finally is to allow for SyntaxError handlers to access the command
            definitions = self._fgen_lmp.create_new_fs_from_code(last_command.code)

            # Define the functions (this is not actually executed, but functions are already
            #  defined by fgen_lmp which shares the code execution environment)
            for f_def in definitions.values():
                execution_history.items.append(ExecutionHistory.Command(f_def))
        finally:
            # Re-insert the command again in order to try it again (this is to be executed)
            execution_history.items.append(last_command)
