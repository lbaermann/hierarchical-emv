import traceback
from typing import List

from .semantic_hint_errror import SemanticHintError


class ErrorHandler:

    def can_handle(self, e: BaseException):
        raise NotImplementedError

    def handle(self, e: BaseException) -> str:
        """
        Handle the given exception, either by raising it again (abort) or returning a string to be inserted into the
        execution history of the simulated Python console.
        """
        raise NotImplementedError

    def reset(self):
        """This is called to signalize there was a successfully executed statement,
        and any state/counters can be reset"""
        pass


class SimpleCountingErrorHandler(ErrorHandler):

    def __init__(self, exception_types: List, max_error_before_abort: int) -> None:
        super().__init__()
        self.exception_types = exception_types
        self.max_error_before_abort = max_error_before_abort
        self.counter = 0

    def can_handle(self, e: BaseException):
        return any(isinstance(e, t) for t in self.exception_types)

    def handle(self, e: BaseException) -> str:
        """
        Handle the given exception, either by raising it again (abort) or returning a string to be inserted into the
        execution history of the simulated Python console.
        """
        self.counter += 1
        if self.counter > self.max_error_before_abort:
            raise
        else:
            return self.format_exception_for_llm(e)

    def format_exception_for_llm(self, e: BaseException):
        raise NotImplementedError

    def reset(self):
        self.counter = 0


class UndefinedNameHandler(SimpleCountingErrorHandler):
    """ Give the LLM a chance to react to its usage of undefined APIs/params """

    def __init__(self, max_error_before_abort: int = 3) -> None:
        super().__init__([NameError, TypeError], max_error_before_abort)

    def handle(self, e: BaseException):
        traceback.print_exc()  # Print the exception, in case the TypeError occurred in the API implementation itself.
        return super().handle(e)

    def format_exception_for_llm(self, e: BaseException):
        return f'{e.__class__.__name__}: {e}.' + (
            ' Solve the task with the imported definitions only.' if isinstance(e, NameError) else '')


class UndefinedAttributeHandler(SimpleCountingErrorHandler):
    """ Give the LLM a chance to react to its usage of undefined attributes of objects """

    def __init__(self, max_error_before_abort: int = 3) -> None:
        super().__init__([AttributeError], max_error_before_abort)

    def handle(self, e: BaseException):
        traceback.print_exc()  # Print the exception, in case the Error occurred in the API implementation itself.
        return super().handle(e)

    def format_exception_for_llm(self, e: AttributeError):
        attrs = [s for s in dir(e.obj) if '_' != s[0]]
        return (f'{e.__class__.__name__}: {e}. Try to solve the task differently, '
                f'and make sure to use only the defined attributes: {attrs}')


class SemanticErrorHandler(SimpleCountingErrorHandler):
    """ SemanticHintError is used in API implementation to throw semantic error messages """

    def __init__(self, max_error_before_abort: int = 4) -> None:
        super().__init__([SemanticHintError], max_error_before_abort)

    def handle(self, e: SemanticHintError) -> str:
        if e.critical:
            return super().handle(e)
        else:
            return self.format_exception_for_llm(e)

    def format_exception_for_llm(self, e: BaseException):
        assert isinstance(e, SemanticHintError)
        return e.message


class ImportHandler(SimpleCountingErrorHandler):
    """ If the LLM tries to import something, give it a hint that this is not allowed"""

    def __init__(self, max_error_before_abort: int = 3) -> None:
        super().__init__([ImportError], max_error_before_abort)

    def format_exception_for_llm(self, e: BaseException):
        return ('ImportError: No imports possible. Try solving the task with only the provided '
                'functions, and if this is not possible, tell the user that you cannot solve it.')


class CollectionAccessErrorHandler(SimpleCountingErrorHandler):
    """ If the LLM makes an IndexError or KeyError """

    def __init__(self, max_error_before_abort: int = 3) -> None:
        super().__init__([IndexError, KeyError], max_error_before_abort)

    def format_exception_for_llm(self, e: BaseException):
        return f'{str(e)}. Revise the code carefully to avoid this error.'


class SyntaxErrorHandler(SimpleCountingErrorHandler):

    def __init__(self, max_error_before_abort: int = 2) -> None:
        super().__init__([SyntaxError], max_error_before_abort)

    def format_exception_for_llm(self, e: BaseException):
        s = str(e).replace('<unknown>, ', '').replace('<string>, ', '')  # Useless "unknown" file name
        return f'SyntaxError: {s}. Revise the code carefully to avoid this error.'


def default_error_handler_config():
    return [
        dict(type='UndefinedNameHandler'),
        dict(type='UndefinedAttributeHandler'),
        dict(type='SemanticErrorHandler'),
        dict(type='ImportHandler'),
        dict(type='CollectionAccessErrorHandler'),
        dict(type='SyntaxErrorHandler'),
    ]
