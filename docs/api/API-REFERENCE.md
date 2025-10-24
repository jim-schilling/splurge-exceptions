# API Reference - Splurge Exceptions

Complete API documentation for the Splurge Exceptions library (Version 2025.0.0).

## Table of Contents

1. [Core Exceptions](#core-exceptions)
2. [Error Code System](#error-code-system)
3. [Wrapping & Conversion](#wrapping--conversion)
4. [Context Managers](#context-managers)
5. [Decorators](#decorators)
6. [Message Formatting](#message-formatting)
7. [Type Definitions](#type-definitions)
8. [Import Statements](#import-statements)

## Core Exceptions

All exception classes are in `splurge_exceptions` module and inherit from `SplurgeError`.

### SplurgeError

Base class for all Splurge exceptions.

```python
class SplurgeError(Exception):
    """Base Splurge exception class with semantic error codes."""
    
    def __init__(
        self,
        error_code: str = "generic",
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
        severity: str = "error",
        recoverable: bool = False,
    ) -> None:
        """Initialize Splurge exception.
        
        Args:
            error_code: User-defined semantic error identifier
                       (e.g., "invalid-value", "timeout", "file-not-found")
                       Must match pattern: [a-z][a-z0-9-]*[a-z0-9]
                       NO dots allowed in error codes.
            message: Human-readable error message
            details: Additional error details/context dictionary
            severity: Error severity level
                     Options: "info", "warning", "error", "critical"
                     Default: "error"
            recoverable: Whether error can be recovered from
                        Default: False
        
        Raises:
            TypeError: If _domain is not defined on the class
            ValueError: If error_code or _domain don't match pattern, or severity is invalid
        
        Example:
            >>> class MyError(SplurgeError):
            ...     _domain = "custom.module"
            >>> error = MyError(
            ...     error_code="invalid-config",
            ...     message="Configuration is invalid",
            ...     details={"config_key": "database_url"},
            ... )
            >>> print(error.full_code)
            custom.module.invalid-config
        """
        ...
    
    @property
    def error_code(self) -> str:
        """Get the user-defined error code.
        
        Returns:
            Error code without domain prefix
            Example: "invalid-value"
        """
        ...
    
    @property
    def full_code(self) -> str:
        """Get the full hierarchical error code with domain.
        
        Returns:
            Full code including domain
            Example: "value.invalid-value"
        """
        ...
    
    @property
    def domain(self) -> str:
        """Get the exception domain.
        
        Returns:
            Domain string (e.g., "validation", "database.sql.query")
        """
        ...
    
    @property
    def message(self) -> str | None:
        """Get the error message."""
        ...
    
    @property
    def severity(self) -> str:
        """Get the severity level."""
        ...
    
    @property
    def is_recoverable(self) -> bool:
        """Check if error is recoverable."""
        ...
    
    def attach_context(
        self,
        key: str | None = None,
        value: Any = None,
        context_dict: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> "SplurgeError":
        """Attach context information to exception.
        
        Args:
            key: Single context key (used with value parameter)
            value: Value for key parameter
            context_dict: Dictionary of context data
            **kwargs: Alternative key-value context pairs
        
        Returns:
            Self for method chaining
        
        Example:
            >>> error.attach_context(key="field", value="email")
            >>> error.attach_context(context_dict={"field": "email", "user_id": 123})
            >>> error.attach_context(field="email", user_id=123)
        """
        ...
    
    def get_context(
        self,
        key: str | None = None,
        default: Any = None,
    ) -> Any:
        """Get attached context.
        
        Args:
            key: Specific context key to retrieve (optional)
            default: Default value if key not found
        
        Returns:
            Single value if key provided, dict of all context otherwise
        
        Example:
            >>> all_context = error.get_context()
            >>> field_value = error.get_context("field")
        """
        ...
    
    def has_context(self, key: str | None = None) -> bool:
        """Check if context exists.
        
        Args:
            key: Specific key to check (optional)
        
        Returns:
            True if context exists
        """
        ...
    
    def add_suggestion(self, suggestion: str) -> "SplurgeError":
        """Add recovery suggestion.
        
        Args:
            suggestion: Recovery suggestion text
        
        Returns:
            Self for method chaining
        
        Example:
            >>> error.add_suggestion("Check email format")
            >>> error.add_suggestion("Verify domain exists")
        """
        ...
    
    def get_suggestions(self) -> list[str]:
        """Get recovery suggestions.
        
        Returns:
            List of suggestion strings (new list, not reference)
        """
        ...
    
    def has_suggestions(self) -> bool:
        """Check if suggestions exist.
        
        Returns:
            True if suggestions available, False otherwise
        """
        ...
```

### SplurgeValueError

For input validation and data validation errors.

```python
class SplurgeValueError(SplurgeError):
    """Raised when input validation fails."""
    _domain = "value"
```

**Common Error Codes:**
- `invalid-value` - Invalid value provided
- `type-mismatch` - Type mismatch error
- `out-of-range` - Value out of range
- `invalid-format` - Invalid format
- `invalid-email` - Invalid email format
- `required-field` - Required field missing

### SplurgeOSError

For operating system and file-related errors.

```python
class SplurgeOSError(SplurgeError):
    """Raised for OS and file system errors."""
    _domain = "os"
```

**Common Error Codes:**
- `file-not-found` - File not found
- `permission-denied` - Permission denied
- `io-error` - I/O error

### SplurgeLookupError

For lookup and search failures.

```python
class SplurgeLookupError(SplurgeError):
    """Raised for lookup issues."""
    _domain = "lookup"
```

**Common Error Codes:**
- `not-found` - Item not found
- `invalid-key` - Invalid lookup key
- `index-out-of-range` - Index out of range

### SplurgeRuntimeError

For runtime execution errors.

```python
class SplurgeRuntimeError(SplurgeError):
    """Raised for runtime execution errors."""
    _domain = "runtime"
```

**Common Error Codes:**
- `operation-failed` - General runtime error
- `timeout` - Operation timeout
- `resource-exhausted` - Resource exhausted

### SplurgeTypeError

For type validation and conversion errors.

```python
class SplurgeTypeError(SplurgeError):
    """Raised for type validation failures."""
    _domain = "type"
```

**Common Error Codes:**
- `invalid-type` - Invalid type provided
- `conversion-failed` - Type conversion failed
- `type-mismatch` - Type mismatch

### SplurgeAttributeError

For missing object attributes and methods.

```python
class SplurgeAttributeError(SplurgeError):
    """Exception raised for missing object attributes/methods."""
    _domain = "attribute"
```

**Common Error Codes:**
- `missing-attribute` - Attribute does not exist on object
- `missing-method` - Method does not exist on object

### SplurgeImportError

For module import and loading failures.

```python
class SplurgeImportError(SplurgeError):
    """Exception raised for module import failures."""
    _domain = "import"
```

**Common Error Codes:**
- `module-not-found` - Module could not be imported
- `import-failed` - Import operation failed
- `circular-import` - Circular import detected

### SplurgeFrameworkError

For framework-level errors and custom domain extensions.

```python
class SplurgeFrameworkError(SplurgeError):
    """Base exception for framework-specific extensions."""
    _domain = "framework"
```

**Common Error Codes:**
- `framework-error` - Framework-level error
- `invalid-configuration` - Invalid framework configuration

This class serves as the base for exceptions defined by frameworks built on top of splurge-exceptions. Domain-specific frameworks should inherit from this class to create their own exception hierarchies.

## Error Code System

### Error Code Format

Splurge Exceptions uses a **semantic error code system** with hierarchical domains:

**Full Error Code Format:**
```
domain.semantic-error-code
```

**Examples:**
- `value.invalid-value` - Value domain, invalid-value error
- `database.sql.query.timeout` - Database > SQL > Query domain, timeout error
- `os.file-not-found` - OS domain, file-not-found error

### Domain Hierarchy

Domains form a hierarchical structure separated by dots:

```
domain                    # Single level (e.g., "validation")
domain.subdomain         # Two levels (e.g., "database.sql")
domain.level2.level3     # Three or more levels (e.g., "database.sql.query")
```

Each domain component must match: `[a-z][a-z0-9-]*[a-z0-9]`

### User-Supplied Error Codes

User-supplied error codes (the semantic part) **CANNOT contain dots**. They must match:

```
[a-z][a-z0-9-]*[a-z0-9]
```

**Valid error codes:**
- `invalid-value`
- `file-not-found`
- `timeout`
- `user-not-found`

**Invalid error codes (rejected at runtime):**
- `invalid.value` (contains dot)
- `INVALID-VALUE` (uppercase not allowed)
- `invalid_value` (underscore not allowed)
- `invalid--value` (double hyphen not allowed)

### Creating Custom Exception Classes

Define custom domains in your exception subclasses:

```python
from splurge_exceptions import SplurgeError

class CustomDatabaseError(SplurgeError):
    _domain = "database.custom.operations"

# Usage:
try:
    # database operation
    raise CustomDatabaseError(
        error_code="query-execution",  # NO dots allowed
        message="Failed to execute query"
    )
except CustomDatabaseError as e:
    print(e.full_code)  # Prints: database.custom.operations.query-execution
```

## Wrapping & Conversion

### wrap_exception

Convert any exception to a Splurge exception.

```python
def wrap_exception(
    exception: BaseException,
    target_exception_type: type[SplurgeError],
    *,
    error_code: str = "generic",
    message: str | None = None,
    context: dict[str, Any] | None = None,
    suggestions: list[str] | None = None,
    details: dict[str, Any] | None = None,
) -> SplurgeError:
    """Wrap source exception as Splurge exception.
    
    Args:
        exception: Original exception to wrap
        target_exception_type: Target Splurge exception class
        error_code: User-defined semantic error code (e.g., "invalid-value", "timeout")
                   Must match pattern: [a-z][a-z0-9-]*[a-z0-9]
                   NO dots allowed
        message: Custom message (uses original exception message if not provided)
        context: Context dictionary to attach to wrapped exception
        suggestions: Suggestions list to attach to wrapped exception
        details: Additional detail information
    
    Returns:
        Wrapped Splurge exception with __cause__ set to original
    
    Raises:
        ValueError: If error_code format is invalid
    
    Example:
        >>> try:
        ...     value = int("invalid")
        ... except ValueError as e:
        ...     wrapped = wrap_exception(
        ...         e,
        ...         SplurgeValueError,
        ...         error_code="invalid-value",
        ...         message="Could not parse input as integer",
        ...         context={"input": "invalid", "expected_type": "int"},
        ...         suggestions=["Provide a valid integer"],
        ...     )
        ...     raise wrapped
    
    Features:
        - Preserves exception chain (__cause__)
        - Preserves original traceback
        - Preserves exception context
        - Attaches context and suggestions
        - Supports custom messages
    
    Note:
        error_code is REQUIRED.
    """
    ...
```

**Features:**
- Required explicit error codes (semantic format)
- Preserves exception chain
- Attaches context and suggestions
- Custom message support

## Context Managers

### error_context

Context manager for exception handling with callbacks.

```python
@contextmanager
def error_context(
    exceptions: dict[type[Exception], tuple[type[SplurgeError], str | None]] | None = None,
    context: dict[str, Any] | None = None,
    on_success: Callable[[], Any] | None = None,
    on_error: Callable[[Exception], Any] | None = None,
    suppress: bool = False,
) -> Iterator[None]:
    """Context manager for exception handling and conversion.
    
    Args:
        exceptions: Dict mapping source to (target exception, error_code)
                   Format: {ValueError: (SplurgeValueError, "value.value.001")}
        context: Dictionary of context data to attach to exceptions
        on_success: Optional callback executed if no exception occurs
                   Signature: Callable[[], Any]
        on_error: Optional callback executed when exception caught
                 Signature: Callable[[Exception], Any]
        suppress: If True, suppress exceptions instead of reraising
    
    Yields:
        None
    
    Raises:
        Mapped exception if not suppressed
    
    Example:
        >>> def handle_success():
        ...     print("Success!")
        >>> 
        >>> def handle_error(exc):
        ...     print(f"Error: {exc}")
        >>> 
        >>> with error_context(
        ...     exceptions={
        ...         ValueError: (SplurgeValueError, "value.001"),
        ...     },
        ...     context={"field": "email"},
        ...     on_success=handle_success,
        ...     on_error=handle_error,
        ...     suppress=False,
        ... ):
        ...     validate_email(user_input)
    
    Features:
        - Exception mapping and automatic conversion
        - Context attachment
        - Callback execution
        - Exception suppression
        - Nested context support
    """
    ...
```

**Parameters:**
- `exceptions`: Mapping of source exception types to (target type, error code)
- `context`: Data to attach to wrapped exceptions
- `on_success`: Called on successful completion
- `on_error`: Called when exception caught (receives wrapped exception)
- `suppress`: If True, suppress exceptions instead of reraising

**Behavior:**
1. Execute code block
2. If no exception: call `on_success` callback (if provided)
3. If exception:
   - Check if mapped in `exceptions` dict
   - If mapped: wrap to target exception type
   - If context provided: attach to wrapped exception
   - Call `on_error` callback with wrapped exception
   - If `suppress=False`: reraise wrapped exception
   - If `suppress=True`: return normally

## Decorators

### handle_exceptions

Decorator for automatic exception conversion.

```python
def handle_exceptions(
    exceptions: dict[type[BaseException], tuple[type[SplurgeError], str | None]],
    log_level: str = "error",
    reraise: bool = True,
    include_traceback: bool = True,
) -> Callable[[F], F]:
    """Decorator for automatic exception handling and conversion.
    
    Args:
        exceptions: Dict mapping source to (target exception, error_code)
                   Format: {ValueError: (SplurgeValueError, "value.001")}
        log_level: Logging level for exceptions
                  Options: "debug", "info", "warning", "error", "critical"
                  Default: "error"
        reraise: Whether to reraise wrapped exception (default: True)
        include_traceback: Include traceback in log (default: True)
    
    Returns:
        Decorated function
    
    Example:
        >>> @handle_exceptions(
        ...     exceptions={
        ...         ValueError: (SplurgeValueError, "value.001"),
        ...         FileNotFoundError: (SplurgeOSError, "os.file.001"),
        ...     },
        ...     log_level="error",
        ...     reraise=True,
        ... )
        ... def process_file(path: str) -> str:
        ...     with open(path) as f:
        ...         return f.read()
    
    Features:
        - Automatic exception conversion
        - Logging of exceptions
        - Optional exception suppression
        - Works with methods, classmethods, staticmethods
        - Preserves function signature and metadata
    """
    ...
```

**Parameters:**
- `exceptions`: Exception type mapping
- `log_level`: Python logging level ("debug", "info", "warning", "error", "critical")
- `reraise`: If True, reraise wrapped exception; if False, return None
- `include_traceback`: Include full traceback in log message

**Behavior:**
1. Wrap function
2. On exception:
   - Check if mapped in `exceptions` dict
   - If mapped: wrap to target exception type
   - Log exception with specified level
   - If `reraise=True`: reraise wrapped exception
   - If `reraise=False`: return None

## Message Formatting

### ErrorMessageFormatter

Format exceptions into readable structured output.

```python
class ErrorMessageFormatter:
    """Formats Splurge exceptions into readable messages."""
    
    def format_error(
        self,
        error: SplurgeError,
        include_context: bool = True,
        include_suggestions: bool = True,
    ) -> str:
        """Format complete error message.
        
        Args:
            error: SplurgeError instance to format
            include_context: Include context section (default: True)
            include_suggestions: Include suggestions section (default: True)
        
        Returns:
            Formatted error message string
        
        Example:
            >>> formatter = ErrorMessageFormatter()
            >>> error = SplurgeValueError(
            ...     error_code="invalid-email",
            ...     message="Invalid email format"
            ... )
            >>> error.attach_context(key="field", value="email")
            >>> error.add_suggestion("Use valid email format")
            >>> message = formatter.format_error(error, include_context=True, include_suggestions=True)
            >>> print(message)
            # [validation.invalid-email] Invalid email format
            # Context:
            #   field: email
            # Suggestions:
            #   1. Use valid email format
        
        Output Format:
            [full_error_code] message
            Context:
              key: value
            Suggestions:
              1. suggestion 1
        """
        ...
```

## Type Definitions

Common type definitions used throughout the API.

```python
# Exception mapping (source exception -> (target exception, error code))
ExceptionMapping = dict[
    type[Exception],
    tuple[type[SplurgeError], str]
]

# Severity levels
SeverityLevel = Literal["info", "warning", "error", "critical"]

# Log levels
LogLevel = Literal["debug", "info", "warning", "error", "critical"]

# Context data
ContextData = dict[str, Any]

# Suggestions list
Suggestions = list[str]

# Callback signatures
OnSuccess = Callable[[], Any]
OnError = Callable[[Exception], Any]
```

## Import Statements

### Import all public components

```python
from splurge_exceptions import (
    # Base exception
    SplurgeError,
    # Specific exceptions
    SplurgeValueError,
    SplurgeOSError,
    SplurgeLookupError,
    SplurgeRuntimeError,
    SplurgeTypeError,
    SplurgeAttributeError,
    SplurgeImportError,
    SplurgeFrameworkError,
    # Utilities
    wrap_exception,
    handle_exceptions,
    error_context,
    ErrorMessageFormatter,
)

## Error Handling Best Practices

1. **Use Semantic Error Codes**: Use descriptive error codes without dots (e.g., "invalid-value", "timeout")
2. **Use Type-Specific Exceptions**: Use the most appropriate Splurge exception type for the domain
3. **Attach Context**: Always attach relevant context information for debugging
4. **Add Suggestions**: Provide actionable recovery suggestions to users
5. **Preserve Chains**: Let Python preserve exception chains automatically via `__cause__`
6. **Log Appropriately**: Use decorators for automatic logging
7. **Format for Users**: Use `ErrorMessageFormatter` for user-facing messages
8. **Define Custom Domains**: Create custom exception classes with domain hierarchies for specific projects

## See Also

- [README-DETAILS.md](../README-DETAILS.md) - Comprehensive feature documentation
- [CLI-REFERENCE.md](../cli/CLI-REFERENCE.md) - CLI tools reference
- [CHANGELOG.md](../../CHANGELOG.md) - Version history
