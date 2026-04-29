import logging
import threading
import traceback
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, List, Optional, Generator

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.tracers.context import register_configure_hook

logger = logging.getLogger(__name__)


class TokenTrackingCallbackHandler(BaseCallbackHandler):
    """Callback Handler that tracks OpenAI and Google Cloud info."""

    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    successful_requests: int = 0

    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()
        self._do_not_track = set()

    def __repr__(self) -> str:
        return (
            f"Tokens Used: {self.total_tokens}\n"
            f"\tPrompt Tokens: {self.prompt_tokens}\n"
            f"\tCompletion Tokens: {self.completion_tokens}\n"
            f"Successful Requests: {self.successful_requests}\n"
        )

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        if (kwargs.get('invocation_params', {}).get('do_not_track', False)
                or kwargs.get('metadata', {}).get('do_not_track', False)):
            self._do_not_track.add(kwargs['run_id'])

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Print out the token."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Collect token usage."""
        if kwargs['run_id'] in self._do_not_track:
            return
        try:
            generation = response.generations[0][0]
            message = generation.message
            usage_metadata = message.usage_metadata or message.response_metadata['token_usage']
            completion_tokens = usage_metadata.get("output_tokens", usage_metadata.get('completion_tokens'))
            prompt_tokens = usage_metadata.get("input_tokens", usage_metadata.get('prompt_tokens'))
            with self._lock:
                self.total_tokens += usage_metadata.get('total_tokens', 0)
                self.prompt_tokens += prompt_tokens
                self.completion_tokens += completion_tokens
                self.successful_requests += 1
        except (IndexError, AttributeError):
            traceback.print_exc()
            pass

    def __copy__(self) -> "TokenTrackingCallbackHandler":
        """Return a copy of the callback handler."""
        return self

    def __deepcopy__(self, memo: Any) -> "TokenTrackingCallbackHandler":
        """Return a deep copy of the callback handler."""
        return self


token_tracking_callback_var: ContextVar[Optional[TokenTrackingCallbackHandler]] = ContextVar(
    "token_tracking_callback", default=None
)

register_configure_hook(token_tracking_callback_var, True)


@contextmanager
def get_token_tracking_callback() -> Generator[TokenTrackingCallbackHandler, None, None]:
    """Get the callback handler in a context manager.
    which conveniently exposes token and cost information.

    Returns:
        TokenTrackingCallbackHandler: The callback handler.

    Example:
        >>> with get_token_tracking_callback() as cb:
        ...     # Use the callback handler
    """
    cb = TokenTrackingCallbackHandler()
    token_tracking_callback_var.set(cb)
    yield cb
    token_tracking_callback_var.set(None)
