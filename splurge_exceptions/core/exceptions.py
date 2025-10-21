"""Core exception types for Splurge Exceptions Framework.

DOMAINS: ["exceptions", "core"]
"""

from splurge_exceptions.core.base import SplurgeError

__all__ = [
    "SplurgeValidationError",
    "SplurgeOSError",
    "SplurgeConfigurationError",
    "SplurgeRuntimeError",
    "SplurgeAuthenticationError",
    "SplurgeAuthorizationError",
    "SplurgeNotImplementedError",
    "SplurgeFrameworkError",
]


class SplurgeValidationError(SplurgeError):
    """Exception raised for data validation failures.

    Used when input data, configuration, or state validation fails.

    Example:
        >>> raise SplurgeValidationError(
        ...     error_code="invalid-value",
        ...     message="Invalid value provided"
        ... )
    """

    _domain = "validation"


class SplurgeOSError(SplurgeError):
    """Exception raised for OS, system, and I/O failures.

    Used for file system operations, system calls, and I/O-related errors.

    Example:
        >>> raise SplurgeOSError(
        ...     error_code="file-not-found",
        ...     message="File not found"
        ... )
    """

    _domain = "os"


class SplurgeConfigurationError(SplurgeError):
    """Exception raised for configuration issues.

    Used when configuration parsing, validation, or loading fails.

    Example:
        >>> raise SplurgeConfigurationError(
        ...     error_code="invalid-format",
        ...     message="Invalid configuration format"
        ... )
    """

    _domain = "config"


class SplurgeRuntimeError(SplurgeError):
    """Exception raised for runtime operation failures.

    Used for runtime errors that occur during program execution.

    Example:
        >>> raise SplurgeRuntimeError(
        ...     error_code="operation-failed",
        ...     message="Operation failed"
        ... )
    """

    _domain = "runtime"


class SplurgeAuthenticationError(SplurgeError):
    """Exception raised for authentication failures.

    Used when authentication credentials are invalid or missing.

    Example:
        >>> raise SplurgeAuthenticationError(
        ...     error_code="invalid-credentials",
        ...     message="Invalid credentials"
        ... )
    """

    _domain = "authentication"


class SplurgeAuthorizationError(SplurgeError):
    """Exception raised for authorization failures.

    Used when a user lacks required permissions or privileges.

    Example:
        >>> raise SplurgeAuthorizationError(
        ...     error_code="access-denied",
        ...     message="Access denied"
        ... )
    """

    _domain = "authorization"


class SplurgeNotImplementedError(SplurgeError):
    """Exception raised for unimplemented features.

    Used when a feature or functionality is not yet implemented.

    Example:
        >>> raise SplurgeNotImplementedError(
        ...     error_code="feature-not-implemented",
        ...     message="Feature not yet implemented"
        ... )
    """

    _domain = "runtime"


class SplurgeFrameworkError(SplurgeError):
    """Base exception for framework-specific extensions.

    This class serves as the base for exceptions defined by frameworks
    built on top of splurge-exceptions. Domain-specific frameworks should
    inherit from this class to create their own exception hierarchies.

    Example:
        >>> from splurge_exceptions import SplurgeFrameworkError
        >>> class SplurgeDsvError(SplurgeFrameworkError):
        ...     _domain = "dsv"
        >>> raise SplurgeDsvError(
        ...     error_code="parse-failed",
        ...     message="Failed to parse DSV file"
        ... )
    """

    _domain = "framework"
