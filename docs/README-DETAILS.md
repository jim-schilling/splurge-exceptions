# Splurge Exceptions - Comprehensive Guide

A comprehensive Python exception management library that provides structured error handling, exception wrapping, and intelligent error code management for modern applications.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Core Concepts](#core-concepts)
5. [Usage Patterns](#usage-patterns)
6. [Library Integration Guide](#library-integration-guide)
7. [Best Practices](#best-practices)
8. [References](#references)

## Overview

Splurge Exceptions is a modern Python exception framework designed to provide:

- **Structured Error Handling**: Semantic error codes with hierarchical domains
- **Exception Wrapping**: Convert any exception to structured Splurge exceptions
- **Context Management**: Attach context data and recovery suggestions to exceptions
- **Type Safety**: Full type annotations with MyPy strict mode support
- **Library Integration**: Clean extension points for domain-specific exceptions

## Features

### Core Exception Classes

Splurge Exceptions provides 6 specialized exception classes, each with its own domain:

| Exception Class | Domain | Purpose |
|-----------------|--------|---------|
| `SplurgeValueError` | `value` | Input validation and data validation errors |
| `SplurgeOSError` | `os` | Operating system and file system errors |
| `SplurgeLookupError` | `lookup` | Lookup and search failures |
| `SplurgeRuntimeError` | `runtime` | Runtime execution errors |
| `SplurgeTypeError` | `type` | Type validation and conversion errors |
| `SplurgeAttributeError` | `attribute` | Attribute access and existence errors |
| `SplurgeImportError` | `import` | Module and import-related errors |
| `SplurgeFrameworkError` | `framework` | Framework-level errors and extensions |

### Exception Features

- **Semantic Error Codes**: User-defined codes like `"invalid-value"`, `"file-not-found"`
- **Hierarchical Domains**: Structured error organization (`value.invalid-email`)
- **Context Attachment**: Add operation context, user data, timestamps
- **Recovery Suggestions**: Provide actionable error resolution guidance
- **Severity Levels**: Info, warning, error, critical classifications
- **Exception Chaining**: Preserve original exception context via `__cause__`

### Exception Management Tools

#### Exception Wrapping (`wrap_exception`)
Convert any standard library or third-party exception to a structured Splurge exception:

```python
from splurge_exceptions import wrap_exception, SplurgeValueError

try:
    # Some operation that might fail
    int("invalid")
except ValueError as e:
    wrapped = wrap_exception(
        e,
        SplurgeValueError,
        error_code="invalid-integer",
        message="Could not parse input as integer",
        context={"input": "invalid", "expected_type": "int"}
    )
    raise wrapped
```

#### Context Managers (`error_context`)
Handle exceptions with automatic conversion and context attachment:

```python
from splurge_exceptions import error_context, SplurgeValueError

with error_context(
    exceptions={ValueError: (SplurgeValueError, "invalid-value")},
    context={"operation": "user_validation", "field": "email"},
    on_success=lambda: print("Validation successful"),
    on_error=lambda e: print(f"Validation failed: {e}")
):
    validate_email(user_input)
```

#### Decorators (`handle_exceptions`)
Automatically convert exceptions on function calls:

```python
from splurge_exceptions import handle_exceptions, SplurgeOSError

@handle_exceptions(
    exceptions={FileNotFoundError: (SplurgeOSError, "file-not-found")},
    log_level="error"
)
def read_config_file(path: str) -> str:
    with open(path) as f:
        return f.read()
```

#### Error Formatting (`ErrorMessageFormatter`)
Create user-friendly error messages with context and suggestions:

```python
from splurge_exceptions import ErrorMessageFormatter

formatter = ErrorMessageFormatter()
formatted_message = formatter.format_error(
    exception,
    include_context=True,
    include_suggestions=True
)
print(formatted_message)
```

### Development & Quality

- **Type Safety**: Full MyPy strict mode compliance
- **Code Quality**: Ruff linting with zero errors
- **Testing**: 229+ tests with 94% coverage
- **Property-Based Testing**: Hypothesis validation with 2,100+ scenarios
- **Zero Dependencies**: No runtime dependencies for maximum compatibility

## Quick Start

### Installation

```bash
pip install splurge-exceptions
```

### Basic Usage

#### 1. Simple Exception Handling

```python
from splurge_exceptions import SplurgeValueError

# Create a structured exception
error = SplurgeValueError(
    error_code="invalid-email",
    message="Email address format is invalid",
    details={"provided": "user@", "domain": "example.com"}
)

# Add context and suggestions
error.attach_context("user_id", 12345)
error.add_suggestion("Use format: username@domain.com")
error.add_suggestion("Check for missing domain part")

print(error.full_code)  # "value.invalid-email"
```

#### 2. Exception Wrapping

```python
from splurge_exceptions import wrap_exception, SplurgeValueError

try:
    # Some validation that might fail
    validate_user_data({"email": "invalid-email"})
except ValueError as original_error:
    # Wrap with structured exception
    structured_error = wrap_exception(
        original_error,
        SplurgeValueError,
        error_code="user-validation-failed",
        context={"operation": "user_registration"}
    )
    raise structured_error
```

#### 3. Context Manager Pattern

```python
from splurge_exceptions import error_context, SplurgeOSError

with error_context(
    exceptions={FileNotFoundError: (SplurgeOSError, "config-file-missing")},
    context={"config_path": "/etc/app/config.json"}
):
    load_configuration()
```

#### 4. Decorator Pattern

```python
from splurge_exceptions import handle_exceptions, SplurgeRuntimeError

@handle_exceptions(
    exceptions={
        ConnectionError: (SplurgeRuntimeError, "database-unavailable"),
        TimeoutError: (SplurgeRuntimeError, "database-timeout")
    }
)
def fetch_user_data(user_id: int) -> dict:
    # Database operations that might fail
    return db.query("SELECT * FROM users WHERE id = ?", [user_id])
```

#### 5. Error Formatting

```python
from splurge_exceptions import ErrorMessageFormatter

formatter = ErrorMessageFormatter()

try:
    risky_operation()
except Exception as e:
    # Format for user display
    user_message = formatter.format_error(e, include_context=True)
    print(user_message)
```

## Core Concepts

### Error Code System

Splurge Exceptions uses a semantic error code system with hierarchical domains:

```
domain.semantic-error-code
```

**Examples:**
- `value.invalid-email` - Value domain, invalid email error
- `os.file-not-found` - OS domain, file not found error
- `database.connection.timeout` - Database > Connection domain, timeout error

**Domain Hierarchy Rules:**
- Domains can be single level (`value`) or hierarchical (`database.sql.query`)
- Each domain component must match: `[a-z][a-z0-9-]*[a-z0-9]`
- User error codes cannot contain dots

### Exception Context

All Splurge exceptions support rich context attachment:

```python
error = SplurgeValueError(error_code="validation-failed")

# Attach different types of context
error.attach_context("user_id", 12345)
error.attach_context("timestamp", "2025-01-01T10:00:00Z")
error.attach_context("operation", "user_registration")
error.attach_context(context_dict={"field": "email", "value": "user@"})

# Retrieve context
user_id = error.get_context("user_id")
all_context = error.get_all_context()

**Context merge semantics:**

- Attaching context is shallow-copy-like: when you pass a dict to
    `attach_context(context_dict=...)` the current keys are copied but nested
    mutable values are not deep-copied (i.e., attach is shallow).
- When multiple contexts are composed (for example with nested
    `error_context()` managers), key conflicts are resolved by replacement:
    the inner/most-recent context value replaces the outer one. If both the
    outer and inner values for the same key are dictionaries, the inner
    dictionary completely replaces the outer dictionary (no deep merge).

This behavior is deliberate: it produces predictable, easy-to-understand
conflict resolution (inner wins) and avoids surprising deep-merge rules.
```

### Recovery Suggestions

Provide actionable guidance for error resolution:

```python
error = SplurgeOSError(error_code="file-not-found")

error.add_suggestion("Verify the file path exists")
error.add_suggestion("Check file permissions")
error.add_suggestion("Ensure the directory is accessible")

suggestions = error.get_suggestions()
# Returns: ["Verify the file path exists", "Check file permissions", ...]
```

### Exception Hierarchy

```
Exception
└── SplurgeError (base class)
    ├── SplurgeValueError (domain: "value")
    ├── SplurgeOSError (domain: "os")
    ├── SplurgeLookupError (domain: "lookup")
    ├── SplurgeRuntimeError (domain: "runtime")
    ├── SplurgeTypeError (domain: "type")
    ├── SplurgeAttributeError (domain: "attribute")
    ├── SplurgeImportError (domain: "import")
    └── SplurgeFrameworkError (domain: "framework")
        └── CustomDomainError (your extensions)
```

## Usage Patterns

### Application-Level Usage

For end-user applications consuming libraries:

```python
# Import what you need
from splurge_exceptions import (
    SplurgeValueError,
    SplurgeOSError,
    error_context,
    ErrorMessageFormatter
)

# Handle errors from libraries
try:
    user_service.create_user(user_data)
except SplurgeValueError as e:
    formatter = ErrorMessageFormatter()
    print("Validation Error:")
    print(formatter.format_error(e, include_suggestions=True))
except SplurgeOSError as e:
    print(f"System Error: {e.error_code}")
```

### Library-Level Usage

For libraries providing services to applications:

```python
from splurge_exceptions import SplurgeValueError, wrap_exception

class UserService:
    def validate_email(self, email: str) -> bool:
        if "@" not in email:
            raise SplurgeValueError(
                error_code="invalid-email-format",
                message="Email must contain @ symbol",
                details={"provided": email}
            )
        return True

    def create_user(self, user_data: dict) -> int:
        # Wrap third-party library errors
        try:
            external_validator.validate(user_data)
        except ValueError as e:
            raise wrap_exception(
                e,
                SplurgeValueError,
                error_code="external-validation-failed",
                context={"validator": "external_lib"}
            ) from e

        # Your business logic here
        return save_to_database(user_data)
```

## Library Integration Guide

### Creating Domain-Specific Exceptions

As a library integrator, you can extend Splurge Exceptions to provide domain-specific error handling:

#### Step 1: Create Domain-Specific Exception Classes

```python
from splurge_exceptions import SplurgeFrameworkError

# Base class for your library's errors
class MyLibraryError(SplurgeFrameworkError):
    """Base exception for MyLibrary errors."""
    _domain = "mylibrary"

# Specific error types for different concerns
class MyLibraryValidationError(MyLibraryError):
    """Validation errors in MyLibrary."""
    _domain = "mylibrary.validation"

class MyLibraryConnectionError(MyLibraryError):
    """Connection and network errors."""
    _domain = "mylibrary.connection"

class MyLibraryConfigError(MyLibraryError):
    """Configuration-related errors."""
    _domain = "mylibrary.config"
```

#### Step 2: Use Semantic Error Codes

```python
class DatabaseClient:
    def connect(self, connection_string: str):
        if not connection_string:
            raise MyLibraryValidationError(
                error_code="empty-connection-string",
                message="Connection string cannot be empty"
            )

        if "invalid" in connection_string:
            raise MyLibraryConnectionError(
                error_code="invalid-connection-format",
                message="Connection string format is invalid",
                details={"provided": connection_string}
            )

        # Success case
        self.connection = create_connection(connection_string)

    def query(self, sql: str, params=None):
        if not self.connection:
            raise MyLibraryConnectionError(
                error_code="not-connected",
                message="No active database connection"
            )

        try:
            return self.connection.execute(sql, params)
        except TimeoutError as e:
            raise wrap_exception(
                e,
                MyLibraryConnectionError,
                error_code="query-timeout",
                context={"sql": sql, "timeout": "30s"}
            ) from e
```

#### Step 3: Provide Rich Context and Suggestions

```python
class APIService:
    def authenticate_user(self, token: str):
        try:
            user = self._validate_token(token)
            return user
        except ValueError as e:
            auth_error = wrap_exception(
                e,
                MyLibraryValidationError,
                error_code="invalid-auth-token",
                context={"token_prefix": token[:10] + "..."}
            )

            # Add recovery suggestions
            auth_error.add_suggestion("Verify token format and expiration")
            auth_error.add_suggestion("Check token was copied correctly")
            auth_error.add_suggestion("Regenerate token if expired")

            raise auth_error from e
```

#### Step 4: Document Error Codes

Create documentation for your library's error codes:

```python
# mylibrary/errors.py
"""
MyLibrary Error Codes Reference:

Validation Errors (mylibrary.validation.*):
- empty-connection-string: Connection string is required
- invalid-connection-format: Connection string format invalid
- invalid-auth-token: Authentication token invalid or expired

Connection Errors (mylibrary.connection.*):
- not-connected: No active database connection
- connection-refused: Database refused connection
- query-timeout: Query execution exceeded timeout

Configuration Errors (mylibrary.config.*):
- missing-config: Required configuration missing
- invalid-config-value: Configuration value invalid
"""

# Export all error classes
__all__ = [
    "MyLibraryError",
    "MyLibraryValidationError",
    "MyLibraryConnectionError",
    "MyLibraryConfigError",
]
```

### Integration Best Practices

#### 1. Consistent Error Codes
- Use lowercase, hyphen-separated names: `connection-timeout`, not `connectionTimeout`
- Keep codes descriptive but concise: `invalid-auth-token`, not `token-validation-failed`

#### 2. Rich Context Information
- Include relevant operation context (user IDs, file paths, operation names)
- Add timestamps for debugging
- Include parameter values (safely truncated)

#### 3. Helpful Suggestions
- Provide 1-3 actionable recovery suggestions
- Focus on the most common resolution paths
- Include links to documentation when relevant

#### 4. Exception Chaining
- Always use `raise ... from e` to preserve exception chains
- Use `wrap_exception()` for clean chain preservation

#### 5. Domain Hierarchy
- Use hierarchical domains: `mylibrary.api.auth`, not just `auth`
- Group related errors under common sub-domains

#### 6. Type Safety
- Use proper type annotations in your error classes
- Document parameter and return types

## Best Practices

### Error Code Design

- **Descriptive**: Use clear, descriptive names (`file-not-found` vs `fnf`)
- **Consistent**: Follow the same patterns across your library
- **Hierarchical**: Use domain hierarchy for organization
- **Stable**: Don't change error codes once published

### Context Management

- **Relevant**: Only attach context relevant to the error
- **Safe**: Don't include sensitive information in error context
- **Structured**: Use consistent key naming conventions
- **Useful**: Include information that helps debugging

### Exception Handling

- **Specific**: Catch specific exception types, not broad `Exception`
- **Chaining**: Preserve exception chains with `from` clause
- **Context**: Add relevant context before re-raising
- **Logging**: Use decorators for consistent logging

### User Experience

- **Clear Messages**: Write error messages for humans, not machines
- **Actionable**: Include suggestions users can actually follow
- **Progressive**: Show basic info first, detailed info on demand
- **Consistent**: Use consistent formatting and terminology

### Performance Considerations

- **Lazy Evaluation**: Don't compute expensive context unless needed
- **Memory Efficient**: Be mindful of context data size
- **Exception Overhead**: Exceptions are for exceptional cases, not control flow
- **Stack Traces**: Keep stack traces manageable in production

## References

- **[API Reference](API-REFERENCE.md)** - Complete API documentation with all classes, methods, and examples
- **[CLI Reference](CLI-REFERENCE.md)** - Command-line interface documentation and usage examples
- **[CHANGELOG](CHANGELOG.md)** - Version history and change details
- **[Examples](../examples/)** - Working code examples for different use cases

---

**Splurge Exceptions** provides a robust foundation for structured error handling in Python applications and libraries. Whether you're building end-user applications or creating reusable libraries, Splurge Exceptions offers the tools you need for professional-grade error management.
