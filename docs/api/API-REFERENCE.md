# API Reference - Splurge Exceptions

Complete API documentation for the Splurge Exceptions library (Version 2025.1.0).

## Table of Contents

1. [Core Exceptions](#core-exceptions)
2. [Error Code System](#error-code-system)
3. [Message Formatting](#message-formatting)
4. [Type Definitions](#type-definitions)
5. [Import Statements](#import-statements)

## Core Exceptions

All exception classes are in `splurge_exceptions` module and inherit from `SplurgeError`.

### SplurgeError

Base class for all Splurge exceptions.

```python
class SplurgeError(Exception):
    """Base Splurge exception class with semantic error codes."""
    
    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize Splurge exception.
        
        Args:
            message: Human-readable error message (required)
            error_code: User-defined semantic error identifier (optional)
                       (e.g., "invalid-value", "timeout", "file-not-found")
                       If provided, must match pattern: [a-z][a-z0-9-]*[a-z0-9]
                       NO dots allowed in error codes.
                       Invalid codes are normalized automatically (no validation error).
            details: Additional error details/context dictionary
        
        Example:
            >>> class MyError(SplurgeError):
            ...     _domain = "custom.module"
            >>> error = MyError(
            ...     "Configuration is invalid",
            ...     error_code="invalid-config",
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
            Domain string (e.g., "splurge.validation", "database.sql.query")
        """
        ...
    
    @property
    def message(self) -> str | None:
        """Get the error message."""
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

### SplurgeSubclassError

Framework exception raised when a `SplurgeError` subclass is misconfigured.

```python
class SplurgeSubclassError(Exception):
    """Raised when a SplurgeError subclass is misconfigured.

    This exception indicates that a subclass of SplurgeError has:
    - A missing or invalid ``_domain`` class attribute
    - An invalid ``error_code`` value that doesn't match patterns
    - An invalid ``_domain`` value that doesn't match patterns

    This is a framework-level error and should only occur during development or
    testing if exception subclasses are defined incorrectly.

    Example:

        class BrokenError(SplurgeError):
            pass  # Missing _domain!

        try:
            BrokenError("Error message", error_code="test")
        except SplurgeSubclassError as e:
            print(f"Exception definition error: {e}")
    """

    pass
```

**When is this raised?**
- Instantiating a `SplurgeError` subclass without defining `_domain` class attribute
- Providing an invalid `error_code` that doesn't match `[a-z][a-z0-9-]*[a-z0-9]` pattern
- Providing an invalid `_domain` that contains invalid component formats
- Providing a `_domain` with empty dot-separated components (e.g., `"a..b"`)

**Catching this exception:**
```python
from splurge_exceptions import SplurgeSubclassError

try:
    # Define exception
    class MyError(SplurgeError):
        _domain = "invalid..domain"  # Invalid: empty component
    
    # Instantiate it
    MyError("Error message", error_code="test")
except SplurgeSubclassError as e:
    print(f"Subclass error: {e}")
```

### Built-In Semantic Exception Types

Splurge Exceptions provides 8 built-in semantic exception types for convenience. These are intended for different use cases:

#### For Applications

If you're **building an application**, use these built-in types directly for common error scenarios:

```python
from splurge_exceptions import SplurgeValueError, SplurgeOSError

# Application-level validation
if not email:
    raise SplurgeValueError(
        "Email is required",
        error_code="required-field"
    )

# File operations
try:
    load_config()
except FileNotFoundError as e:
    raise SplurgeOSError(
        "Configuration file not found",
        error_code="config-not-found"
    ) from e
```

#### For Libraries

If you're **building a library**, define your own exception hierarchy using `SplurgeFrameworkError` as the base. This makes error origins explicit and traceable:

```python
from splurge_exceptions import SplurgeFrameworkError

# Your library defines its own hierarchy
class MyLibraryError(SplurgeFrameworkError):
    _domain = "mylibrary"

class MyLibraryValidationError(MyLibraryError):
    _domain = "mylibrary.validation"

# Now callers see: "mylibrary.validation.invalid-config"
raise MyLibraryValidationError(
    "Configuration is invalid",
    error_code="invalid-config"
)
```

See [Library Integration Guide](../README-DETAILS.md#library-integration-guide) for detailed examples.

### SplurgeValueError

For input validation and data validation errors.

```python
class SplurgeValueError(SplurgeError):
    """Raised when input validation fails."""
    _domain = "splurge.value"
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
    _domain = "splurge.os"
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
    _domain = "splurge.lookup"
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
    _domain = "splurge.runtime"
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
    _domain = "splurge.type"
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
    _domain = "splurge.attribute"
```

**Common Error Codes:**
- `missing-attribute` - Attribute does not exist on object
- `missing-method` - Method does not exist on object

### SplurgeImportError

For module import and loading failures.

```python
class SplurgeImportError(SplurgeError):
    """Exception raised for module import failures."""
    _domain = "splurge.import"
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
    _domain = "splurge.framework"
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
        "Failed to execute query",
        error_code="query-execution",  # NO dots allowed
    )
except CustomDatabaseError as e:
    print(e.full_code)  # Prints: database.custom.operations.query-execution
```

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
            ...     "Invalid email format",
            ...     error_code="invalid-email"
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
    # Base exceptions
    SplurgeError,
    SplurgeSubclassError,
    # Semantic exceptions
    SplurgeValueError,
    SplurgeOSError,
    SplurgeLookupError,
    SplurgeRuntimeError,
    SplurgeTypeError,
    SplurgeAttributeError,
    SplurgeImportError,
    SplurgeFrameworkError,
    # Formatting utility
    ErrorMessageFormatter,
)
```

### Minimal imports (most common cases)

```python
from splurge_exceptions import (
    SplurgeError,           # Base class for custom exceptions
    SplurgeFrameworkError,  # Base for library-specific exceptions
    ErrorMessageFormatter,  # Format errors for display
)
```

## Error Handling Best Practices

1. **Use Semantic Error Codes**: Use descriptive error codes without dots (e.g., "invalid-value", "timeout")
2. **Use Type-Specific Exceptions**: Use the most appropriate Splurge exception type for the domain
3. **Attach Context**: Always attach relevant context information for debugging
4. **Add Suggestions**: Provide actionable recovery suggestions to users
5. **Preserve Chains**: Always use `raise ... from` to preserve exception chains
6. **Format for Users**: Use `ErrorMessageFormatter` for user-facing messages

## See Also

- [README-DETAILS.md](../README-DETAILS.md) - Comprehensive feature documentation
- [CLI-REFERENCE.md](../cli/CLI-REFERENCE.md) - CLI tools reference
- [CHANGELOG.md](../../CHANGELOG.md) - Version history
