"""Core exception types for Splurge Exceptions Framework.

DOMAINS: ["exceptions", "core"]
"""

from splurge_exceptions.core.base import SplurgeError

__all__ = [
    "SplurgeValueError",
    "SplurgeOSError",
    "SplurgeLookupError",
    "SplurgeRuntimeError",
    "SplurgeTypeError",
    "SplurgeAttributeError",
    "SplurgeImportError",
    "SplurgeFrameworkError",
]


class SplurgeValueError(SplurgeError):
    """Exception raised for value validation failures.

    Used when input data, configuration, or state validation fails.

    Example:
        >>> raise SplurgeValueError(
        ...     error_code="invalid-value",
        ...     message="Invalid value provided"
        ...     details={"value": "123", "expected": "int"}
        ... )
    """

    _domain = "value"


class SplurgeOSError(SplurgeError):
    """Exception raised for OS, system, and I/O failures.

    Used for file system operations, system calls, and I/O-related errors.

    Example:
        >>> raise SplurgeOSError(
        ...     error_code="file-not-found",
        ...     message="File not found"
        ...     details={"operation": "file_read", "path": "/data/data.txt"}
        ... )
    """

    _domain = "os"


class SplurgeLookupError(SplurgeError):
    """Exception raised for lookup issues.

    Used when lookup, retrieval, or search fails.

    Example:
        >>> raise SplurgeLookupError(
        ...     error_code="invalid-format",
        ...     message="Invalid lookup"
        ...     details={"query": "SELECT * FROM users WHERE id = 1"}
        ... )
    """

    _domain = "lookup"


class SplurgeRuntimeError(SplurgeError):
    """Exception raised for runtime operation failures.

    Used for runtime errors that occur during program execution.

    Example:
        >>> raise SplurgeRuntimeError(
        ...     error_code="operation-failed",
        ...     message="Operation failed"
        ...     details={"operation": "file_read", "path": "/data/data.txt"}
        ... )
    """

    _domain = "runtime"


class SplurgeTypeError(SplurgeError):
    """Exception raised for type validation failures.

    Used when type validation, conversion, or casting fails.

    Example:
        >>> raise SplurgeTypeError(
        ...     error_code="invalid-type",
        ...     message="Invalid type"
        ...     details={"expected": "int", "received": "str"}
        ... )
    """

    _domain = "type"


class SplurgeAttributeError(SplurgeError):
    """Exception raised for missing object attributes/methods.

    Used when accessing attributes or methods that don't exist on an object.

    Example:
        >>> raise SplurgeAttributeError(
        ...     error_code="missing-attribute",
        ...     message="Attribute does not exist"
        ...     details={"object": "MyClass", "attribute": "missing_method"}
        ... )
    """

    _domain = "attribute"


class SplurgeImportError(SplurgeError):
    """Exception raised for module import failures.

    Used when module loading, importing, or plugin loading fails.

    Example:
        >>> raise SplurgeImportError(
        ...     error_code="module-not-found",
        ...     message="Module could not be imported"
        ...     details={"module": "mymodule", "path": "/path/to/module"}
        ... )
    """

    _domain = "import"


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
        ...     details={"operation": "file_read", "path": "/data/data.txt"}
        ... )
    """

    _domain = "framework"
