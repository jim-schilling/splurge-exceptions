"""Exception handling decorator for automatic exception conversion.

Provides a decorator for automatically catching and converting exceptions
to Splurge exceptions with optional logging and context attachment.
"""

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

from splurge_exceptions import SplurgeError
from splurge_exceptions.wrappers.stdlib import wrap_exception

F = TypeVar("F", bound=Callable[..., Any])

# Get module-level logger
logger = logging.getLogger(__name__)


def handle_exceptions(
    exceptions: dict[type[BaseException], tuple[type[SplurgeError], str]],
    log_level: str = "error",
    reraise: bool = True,
    include_traceback: bool = True,
) -> Callable[[F], F]:
    """Decorator for automatic exception handling and conversion to Splurge exceptions.

    Catches specified exceptions and converts them to Splurge exceptions with optional logging.

    Args:
        exceptions: Dictionary mapping source exception types to target Splurge exception
                   type and error code. Format: {SourceException: (SplurgeExceptionType, "error.code")}
        log_level: Logging level for exceptions. Default "error".
                  Values: "debug", "info", "warning", "error", "critical"
        reraise: Whether to reraise the wrapped exception. If False, logs and returns None.
                Default True.
        include_traceback: Whether to include traceback in logged message. Default True.

    Returns:
        Decorator function that wraps the target function.

    Example:
        >>> @handle_exceptions(
        ...     exceptions={
        ...         ValueError: (SplurgeValidationError, "invalid-value"),
        ...         FileNotFoundError: (SplurgeOSError, "file-not-found"),
        ...     },
        ...     log_level="error",
        ...     reraise=True,
        ... )
        ... def process_file(path: str) -> str:
        ...     with open(path) as f:
        ...         if not f.read().strip():
        ...             raise ValueError("File is empty")
        ...         return "OK"
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                # Check if this exception should be handled
                source_exc_type = type(e)
                if source_exc_type not in exceptions:
                    # Not mapped, reraise as-is
                    raise

                # Get target exception type and error code
                target_exc_type, error_code = exceptions[source_exc_type]

                # Wrap the exception
                wrapped = wrap_exception(
                    e,
                    target_exc_type,
                    error_code=error_code,
                )

                # Get log function
                log_func = getattr(logger, log_level, logger.error)

                # Log the exception
                if include_traceback:
                    log_func(
                        f"Exception {wrapped.error_code}: {wrapped.message}",
                        exc_info=True,
                    )
                else:
                    log_func(f"Exception {wrapped.error_code}: {wrapped.message}")

                # Reraise or suppress
                if reraise:
                    raise wrapped from e
                else:
                    return None

        return wrapper  # type: ignore[return-value]

    return decorator
