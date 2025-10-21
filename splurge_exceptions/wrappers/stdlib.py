"""Standard library exception wrapping utilities.

Provides utilities for converting standard library exceptions to Splurge exceptions
with automatic error code resolution, context attachment, and exception chaining.
"""

from typing import Any

from splurge_exceptions import SplurgeError


def wrap_exception(
    exception: BaseException,
    target_exception_type: type[SplurgeError],
    error_code: str,
    message: str | None = None,
    context: dict[str, Any] | None = None,
    suggestions: list[str] | None = None,
    details: dict[str, Any] | None = None,
) -> SplurgeError:
    """Convert a standard library exception to a Splurge exception.

    Wraps a stdlib exception in a Splurge exception type with context attachment, and full exception chaining.

    Args:
        exception: The original exception to wrap
        target_exception_type: Target Splurge exception class (e.g., SplurgeOSError)
        error_code: Semantic error code string (required, no dots allowed)
        message: Custom error message (uses original exception message if not provided)
        context: Dictionary of context data to attach to exception
        suggestions: List of recovery suggestions
        details: Dictionary of additional details

    Returns:
        An instance of target_exception_type with wrapped exception as __cause__

    Example:
        >>> try:
        ...     raise FileNotFoundError("data.txt")
        ... except FileNotFoundError as e:
        ...     wrapped = wrap_exception(
        ...         e,
        ...         SplurgeOSError,
        ...         error_code="file-not-found",
        ...         message="Failed to read data file",
        ...         context={"path": "/data/data.txt"},
        ...         suggestions=["Check file path", "Verify permissions"]
        ...     )
        ...     raise wrapped from e
    """

    # Use original exception message if not provided
    if message is None:
        message = str(exception)

    # Create wrapped exception
    wrapped = target_exception_type(
        error_code=error_code,
        message=message,
        details=details,
    )

    # Chain the original exception
    wrapped.__cause__ = exception

    # Attach context if provided
    if context:
        if isinstance(context, dict):
            wrapped.attach_context(context_dict=context)
        else:
            # Assume it's a single key-value pair
            wrapped.attach_context(context_dict=context)

    # Add suggestions if provided
    if suggestions:
        for suggestion in suggestions:
            wrapped.add_suggestion(suggestion)

    return wrapped
