"""Exception context manager for error handling and resource cleanup.

Provides context manager for catching, converting, and handling exceptions
with optional callback execution and exception suppression.
"""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from splurge_exceptions import SplurgeError
from splurge_exceptions.wrappers.stdlib import wrap_exception


@contextmanager
def error_context(
    exceptions: dict[type[Exception], tuple[type[SplurgeError], str]] | None = None,
    context: dict[str, Any] | None = None,
    on_success: Callable[[], Any] | None = None,
    on_error: Callable[[Exception], Any] | None = None,
    suppress: bool = False,
) -> Iterator[None]:
    """Context manager for exception handling and conversion.

    Provides a context manager for catching and converting exceptions to Splurge
    exceptions with optional callbacks, context attachment, and exception suppression.

    Args:
        exceptions: Dict mapping source exception types to (target Splurge exception type, error_code)
        context: Dictionary of context data to attach to converted exceptions
        on_success: Optional callback executed if no exception occurs
        on_error: Optional callback executed when exception is caught
        suppress: If True, suppress exceptions instead of reraising

    Yields:
        None

    Example:
        >>> def handle_success():
        ...     print("Success!")
        >>>
        >>> def handle_error(exc):
        ...     print(f"Error: {exc}")
        >>>
        >>> with error_context(
        ...     exceptions={
        ...         ValueError: (SplurgeValidationError, "validation.invalid-value"),
        ...     },
        ...     on_success=handle_success,
        ...     on_error=handle_error,
        ... ):
        ...     # Code that might raise ValueError
        ...     process_data()
    """
    try:
        yield
        # If no exception, call on_success callback
        if on_success:
            on_success()
    except BaseException as err:
        # Convert BaseException to Exception for type safety
        if not isinstance(err, Exception):
            # Re-raise non-Exception BaseExceptions
            raise

        e = err
        # Check if exception should be handled
        if exceptions and type(e) in exceptions:
            target_exc_type, error_code = exceptions[type(e)]

            # Wrap the exception
            wrapped = wrap_exception(
                e,
                target_exc_type,
                error_code=error_code,
            )

            # Attach context if provided
            if context:
                wrapped.attach_context(context_dict=context)

            # Call on_error callback with wrapped exception
            if on_error:
                try:
                    on_error(wrapped)
                except Exception:
                    # If callback fails, reraise the original wrapped exception
                    if not suppress:
                        raise wrapped from e
                    return

            # Reraise or suppress
            if not suppress:
                raise wrapped from e
        else:
            # Exception not mapped, call on_error with original
            if on_error:
                try:
                    on_error(e)
                except Exception:
                    # If callback fails, reraise the original
                    if not suppress:
                        raise
                    return

            # Reraise or suppress unmapped exception
            if not suppress:
                raise
