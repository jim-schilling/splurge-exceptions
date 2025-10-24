"""Base exception class for Splurge Exceptions Framework.

DOMAINS: ["exceptions", "core"]
"""

import re
from typing import Any

__all__ = ["SplurgeError"]

# Pattern for valid domain and error code components
# Must start with lowercase letter, contain only lowercase letters, digits, and hyphens,
# and end with lowercase letter or digit. Minimum 2 characters.
# Used for individual components like "invalid-value", "database", "sql"
VALID_COMPONENT_PATTERN = re.compile(r"^[a-z][a-z0-9\-]*[a-z0-9]$")

# Pattern for hierarchical domain identifiers: allows dots between components
# (e.g., "database.sql.query") but user-supplied error codes cannot contain dots
VALID_HIERARCHICAL_PATTERN = re.compile(r"^[a-z][a-z0-9\-\.]*[a-z0-9]$")


class SplurgeError(Exception):
    """Base exception for all Splurge errors.

    This is the root exception class for the Splurge exception framework. All
    framework-specific exceptions inherit from this class and must define a
    _domain class attribute.

    The _domain attribute forms the hierarchical prefix for error codes.
    For example, a class with _domain="database.sql.query" combined with
    error_code="invalid-column" produces the full code:
    "database.sql.query.invalid-column"

    Attributes:
        _domain: Hierarchical domain identifier (e.g., "database.sql.query")
        error_code: User-defined semantic error identifier (e.g., "invalid-column")
        message: Human-readable error message
        details: Additional error details/context
        severity: Error severity level (info, warning, error, critical)
        recoverable: Whether error is recoverable

    Example:
        >>> class SplurgeSqlQueryError(SplurgeError):
        ...     _domain = "database.sql.query"
        >>> error = SplurgeSqlQueryError(
        ...     error_code="column-not-found",
        ...     message="Column 'user_id' does not exist"
        ... )
        >>> print(error.full_code)
        database.sql.query.column-not-found
    """

    # Severity levels
    SEVERITY_INFO = "info"
    SEVERITY_WARNING = "warning"
    SEVERITY_ERROR = "error"
    SEVERITY_CRITICAL = "critical"

    VALID_SEVERITIES = {SEVERITY_INFO, SEVERITY_WARNING, SEVERITY_ERROR, SEVERITY_CRITICAL}

    # Must be overridden by subclasses
    _domain: str

    def __init__(
        self,
        error_code: str = "generic",
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
        severity: str = "error",
        recoverable: bool = False,
    ) -> None:
        """Initialize SplurgeError.

        Args:
            error_code: User-defined semantic error identifier (e.g., "invalid-column")
            message: Human-readable error message
            details: Additional error details/context
            severity: Error severity level (info, warning, error, critical)
            recoverable: Whether error is recoverable

        Raises:
            TypeError: If _domain is not defined on the class
            ValueError: If error_code or _domain don't match pattern, or severity is invalid
        """
        # Verify _domain is defined
        if not hasattr(self.__class__, "_domain"):
            raise TypeError(f"{self.__class__.__name__} must define _domain class attribute")

        # Validate error_code
        self._validate_error_code(error_code)

        # Validate _domain
        self._validate_domain(self._domain)

        # Validate severity
        if severity not in self.VALID_SEVERITIES:
            raise ValueError(f"Invalid severity: {severity}. Must be one of {self.VALID_SEVERITIES}")

        self._error_code = error_code
        self._message = message
        self._details = details or {}
        self._severity = severity
        self._recoverable = recoverable
        self._context: dict[str, Any] = {}
        self._suggestions: list[str] = []

        # Construct the exception message
        error_message = self._format_message()
        super().__init__(error_message)

    @staticmethod
    def _validate_error_code(error_code: str) -> None:
        """Validate error code format.

        User-provided error codes cannot contain dots. Dots are only allowed
        in domain hierarchies (e.g., "database.sql.query").

        Args:
            error_code: Error code to validate (e.g., "invalid-column", "timeout")

        Raises:
            ValueError: If error_code doesn't match pattern
        """
        if not error_code:
            raise ValueError("error_code cannot be empty")

        if not VALID_COMPONENT_PATTERN.match(error_code):
            raise ValueError(
                f"Invalid error_code '{error_code}'. Must match pattern "
                "[a-z][a-z0-9-]*[a-z0-9] (e.g., 'invalid-column', 'timeout')"
            )

    @staticmethod
    def _validate_domain(domain: str) -> None:
        """Validate domain format.

        Args:
            domain: Domain to validate

        Raises:
            ValueError: If domain doesn't match pattern
        """
        if not domain:
            raise ValueError("_domain cannot be empty")

        # Split on dots and validate each component
        components = domain.split(".")
        for component in components:
            if not component:
                raise ValueError("_domain cannot have empty components (e.g., 'a..b')")
            if not VALID_COMPONENT_PATTERN.match(component):
                raise ValueError(
                    f"Invalid _domain '{domain}'. Each component must match pattern "
                    "[a-z][a-z0-9-]*[a-z0-9] (e.g., 'database.sql.query')"
                )

    def _format_message(self) -> str:
        """Format the exception message.

        Returns:
            Formatted error message including full code and message.
        """
        parts = []

        if self.full_code:
            parts.append(f"[{self.full_code}]")

        if self._message:
            parts.append(self._message)

        return " ".join(parts) if parts else "An error occurred"

    @property
    def full_code(self) -> str:
        """Get the full error code.

        Combines domain and error_code with dots.

        Returns:
            The full error code (e.g., "database.sql.query.invalid-column")
        """
        return f"{self._domain}.{self._error_code}"

    @property
    def error_code(self) -> str:
        """Get the user-defined error code.

        Returns:
            The error code (e.g., "invalid-column")
        """
        return self._error_code

    @property
    def domain(self) -> str:
        """Get the domain.

        Returns:
            The domain (e.g., "database.sql.query")
        """
        return self._domain

    @property
    def message(self) -> str | None:
        """Get the error message.

        Returns:
            The human-readable error message or None.
        """
        return self._message

    @property
    def details(self) -> dict[str, Any]:
        """Get the error details.

        Returns:
            Dictionary of additional error details.
        """
        return self._details.copy()

    @property
    def severity(self) -> str:
        """Get the error severity level.

        Returns:
            One of: info, warning, error, critical.
        """
        return self._severity

    @property
    def recoverable(self) -> bool:
        """Check if error is recoverable.

        Returns:
            True if error is recoverable, False otherwise.
        """
        return self._recoverable

    def is_recoverable(self) -> bool:
        """Check if error is recoverable.

        Returns:
            True if error is recoverable, False otherwise.
        """
        return self._recoverable

    def get_full_message(self) -> str:
        """Get full message including code, message, and details.

        Returns:
            Full formatted error message.
        """
        parts = []

        if self.full_code:
            parts.append(f"[{self.full_code}]")

        if self._message:
            parts.append(self._message)

        if self._details:
            details_str = ", ".join(f"{k}={v!r}" for k, v in self._details.items())
            parts.append(f"({details_str})")

        return " ".join(parts) if parts else "An error occurred"

    # Context management methods
    def attach_context(
        self,
        key: str | None = None,
        value: Any = None,
        context_dict: dict[str, Any] | None = None,
    ) -> "SplurgeError":
        """Attach context data to the exception.

        Can be called with either (key, value) pair or a dictionary.

        Args:
            key: Context key (ignored if context_dict is provided)
            value: Context value (ignored if context_dict is provided)
            context_dict: Dictionary of context items to attach

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If neither key nor context_dict is provided.

        Example:
            >>> error = SplurgeError("error.001", "Something failed")
            >>> error.attach_context(key="operation", value="file_read")
            >>> error.attach_context({"retry_count": 3, "timeout": 30})
        """
        if context_dict:
            self._context.update(context_dict)
        elif key is not None:
            self._context[key] = value
        else:
            raise ValueError("Either 'key' or 'context_dict' must be provided")

        return self

    def get_context(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve context value by key.

        Args:
            key: Context key to retrieve
            default: Default value if key not found

        Returns:
            Context value or default if not found.
        """
        return self._context.get(key, default)

    def get_all_context(self) -> dict[str, Any]:
        """Retrieve all context data.

        Returns:
            Dictionary copy of all context data.
        """
        return self._context.copy()

    def has_context(self, key: str) -> bool:
        """Check if context key exists.

        Args:
            key: Context key to check

        Returns:
            True if key exists, False otherwise.
        """
        return key in self._context

    def clear_context(self) -> "SplurgeError":
        """Clear all context data.

        Returns:
            Self for method chaining.
        """
        self._context.clear()
        return self

    # Suggestion management methods
    def add_suggestion(self, suggestion: str) -> "SplurgeError":
        """Add a recovery suggestion.

        Args:
            suggestion: Recovery suggestion text

        Returns:
            Self for method chaining.

        Example:
            >>> error = SplurgeError("error.001", "File not found")
            >>> error.add_suggestion("Check if the file path is correct")
            >>> error.add_suggestion("Verify file permissions")
        """
        self._suggestions.append(suggestion)
        return self

    def get_suggestions(self) -> list[str]:
        """Retrieve all recovery suggestions.

        Returns:
            List of recovery suggestions.
        """
        return self._suggestions.copy()

    def has_suggestions(self) -> bool:
        """Check if there are any suggestions.

        Returns:
            True if suggestions exist, False otherwise.
        """
        return len(self._suggestions) > 0

    def __repr__(self) -> str:
        """Return detailed representation of exception.

        Returns:
            Detailed string representation.
        """
        args = []

        if self._error_code:
            args.append(f"error_code={self._error_code!r}")

        if self._message:
            args.append(f"message={self._message!r}")

        if self._details:
            args.append(f"details={self._details!r}")

        args.append(f"severity={self._severity!r}")

        if self._recoverable:
            args.append(f"recoverable={self._recoverable}")

        return f"{self.__class__.__name__}({', '.join(args)})"

    def __str__(self) -> str:
        """Return string representation of exception.

        Returns:
            Formatted error message.
        """
        return self.get_full_message()

    def __reduce__(self):
        """Support pickling by providing constructor args and state.

        The default Exception pickling uses the instance args (which are the
        formatted message). SplurgeError requires structured constructor
        arguments (error_code, message, details, severity, recoverable), so
        implement __reduce__ to ensure correct round-trip and preserve
        context/suggestions.

        Returns a tuple of (callable, args, state) where:
        - callable: The class constructor
        - args: A tuple with only error_code as positional argument
        - state: A dict with remaining kwargs and instance state to be restored
        """
        state = {
            "message": self._message,
            "details": self._details,
            "severity": self._severity,
            "recoverable": self._recoverable,
            "_context": self._context,
            "_suggestions": self._suggestions,
        }
        return (
            self.__class__,
            (self._error_code,),
            state,
        )

    def __setstate__(self, state: dict | None) -> None:
        """Restore pickled state (keyword arguments and instance state)."""
        if not state:
            return

        # Restore keyword arguments from the state
        message = state.get("message")
        details = state.get("details", {})
        severity = state.get("severity", "error")
        recoverable = state.get("recoverable", False)

        # Update instance with these values
        self._message = message
        self._details = details if isinstance(details, dict) else {}
        self._severity = severity
        self._recoverable = recoverable

        # Restore context and suggestions
        ctx = state.get("_context")
        if isinstance(ctx, dict):
            self._context = ctx.copy()
        sugg = state.get("_suggestions")
        if isinstance(sugg, list):
            self._suggestions = list(sugg)
