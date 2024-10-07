class SemanticHintError(Exception):
    def __init__(self, message, critical=True):
        super().__init__()
        self.message = message
        # Non-critical errors are an implementation hack to print something to the simulated console.
        #  They do not increase the error counter and thus cannot cause the LMP to abort
        self.critical = critical

    def __str__(self) -> str:
        return self.message


