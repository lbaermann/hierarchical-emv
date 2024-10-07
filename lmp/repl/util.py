from dataclasses import dataclass


class ExecutionHistory:
    @dataclass
    class Command:
        code: str  # without ">>>" or "..."

        def __str__(self):
            lines = self.code.splitlines()
            result = '>>> ' + lines[0]
            for line in lines[1:]:
                result += '\n... ' + line
            return result

    @dataclass
    class ExecutionResult:
        content: str

        def __str__(self):
            return self.content

    class InputPrompt:
        def __str__(self):
            return '>>>'

    def __init__(self) -> None:
        super().__init__()
        self.items = []

    def __str__(self):
        return '\n'.join(str(i) for i in self.items)
