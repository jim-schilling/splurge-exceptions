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

Splurge Exceptions provides 8 semantic exception classes plus a framework misconfiguration class:

| Exception Class | Domain | Purpose |
|-----------------|--------|---------|
| `SplurgeValueError` | `splurge.value` | Input validation and data validation errors |
| `SplurgeOSError` | `splurge.os` | Operating system and file system errors |
| `SplurgeLookupError` | `splurge.lookup` | Lookup and search failures |
| `SplurgeRuntimeError` | `splurge.runtime` | Runtime execution errors |
| `SplurgeTypeError` | `splurge.type` | Type validation and conversion errors |
| `SplurgeAttributeError` | `splurge.attribute` | Attribute access and existence errors |
| `SplurgeImportError` | `splurge.import` | Module and import-related errors |
| `SplurgeFrameworkError` | `splurge.framework` | Framework-level errors and extensions |
| `SplurgeSubclassError` | (framework) | Raised when a SplurgeError subclass is misconfigured |

### Exception Features

- **Semantic Error Codes**: User-defined codes like `"invalid-value"`, `"file-not-found"`
- **Hierarchical Domains**: Structured error organization (`splurge.value.invalid-email`)
- **Context Attachment**: Add operation context, user data, timestamps
- **Recovery Suggestions**: Provide actionable error resolution guidance
- **Exception Chaining**: Preserve original exception context via `raise ... from`

### Exception Management with Explicit Patterns

#### Manual Exception Conversion
Convert any standard library or third-party exception to a structured Splurge exception:

```python
from splurge_exceptions import SplurgeValueError

try:
    # Some operation that might fail
    int("invalid")
except ValueError as e:
    # Wrap the exception with explicit try/except
    wrapped = SplurgeValueError(
        "Could not parse input as integer",
        error_code="invalid-integer",
        details={"input": "invalid", "expected_type": "int"}
    )
    wrapped.attach_context({
        "operation": "parse_integer",
        "input_value": "invalid"
    })
    raise wrapped from e
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
    "Email address format is invalid",
    error_code="invalid-email",
    details={"provided": "user@", "domain": "example.com"}
)

# Add context and suggestions
error.attach_context("user_id", 12345)
error.add_suggestion("Use format: username@domain.com")
error.add_suggestion("Check for missing domain part")

print(error.full_code)  # "splurge.value.invalid-email"
```

#### 2. Exception Conversion with Chaining

```python
from splurge_exceptions import SplurgeValueError

try:
    # Some validation that might fail
    validate_user_data({"email": "invalid-email"})
except ValueError as original_error:
    # Create structured exception and chain original
    structured_error = SplurgeValueError(
        "User validation failed",
        error_code="user-validation-failed"
    )
    structured_error.attach_context({
        "operation": "user_registration"
    })
    raise structured_error from original_error
```

#### 3. Error Formatting

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

#### 4. Error Formatting with Context and Suggestions

## Core Concepts

### Error Code System

Splurge Exceptions uses a semantic error code system with hierarchical domains:

```
domain.semantic-error-code
```

**Examples:**
- `splurge.value.invalid-email` - Splurge > Value domain, invalid email error
- `splurge.os.file-not-found` - Splurge > OS domain, file not found error
- `database.connection.timeout` - Database > Connection domain, timeout error

**Domain Hierarchy Rules:**
- Built-in Splurge exceptions use `splurge.*` prefix (e.g., `splurge.value`, `splurge.os`)
- User-defined domains should use library/namespace prefix (e.g., `database.sql.query`, `mylib.validation`)
- Each domain component must match: `[a-z][a-z0-9-]*[a-z0-9]`
- User error codes cannot contain dots

### Exception Context

All Splurge exceptions support rich context attachment:

```python
error = SplurgeValueError("Validation failed", error_code="validation-failed")

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
error = SplurgeOSError("File not found", error_code="file-not-found")

error.add_suggestion("Verify the file path exists")
error.add_suggestion("Check file permissions")
error.add_suggestion("Ensure the directory is accessible")

suggestions = error.get_suggestions()
# Returns: ["Verify the file path exists", "Check file permissions", ...]
```

### Exception Hierarchy

```
Exception
└── SplurgeSubclassError (internal framework misconfiguration)
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

**For end-user applications** consuming libraries, use the built-in semantic exception types for convenience:

```python
# Import what you need
from splurge_exceptions import (
    SplurgeValueError,        # Input/data validation errors
    SplurgeOSError,           # File/OS errors  
    SplurgeRuntimeError,      # Runtime execution errors
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

# Raise built-in types for simple cases
if not user_email:
    raise SplurgeValueError(
        "Email is required",
        error_code="required-field",
        details={"field": "email"}
    )
```

**Key Points for Applications:**
- Use the built-in `Splurge*Error` types for quick, semantic error handling
- Stack traces clearly show error types (e.g., `SplurgeValueError`)
- Type checking with `except SplurgeValueError` works naturally
- Full code includes `splurge.*` prefix for easy filtering in logs

### Library-Level Usage (RECOMMENDED)

**For libraries providing services**, define your own exception hierarchy to make error origins explicit:

```python
from splurge_exceptions import SplurgeFrameworkError

# Step 1: Define your library's base exception
class SplurgeSafeIoError(SplurgeFrameworkError):
    """Base exception for SplurgeSafeIo library."""
    _domain = "splurge-safe-io"

# Step 2: Define domain-specific error types
class SplurgeSafeIoValidationError(SplurgeSafeIoError):
    """Validation errors in SplurgeSafeIo."""
    _domain = "splurge-safe-io.validation"

class SplurgeSafeIoConnectionError(SplurgeSafeIoError):
    """Connection errors in SplurgeSafeIo."""
    _domain = "splurge-safe-io.connection"

class SplurgeSafeIoRuntimeError(SplurgeSafeIoError):
    """Runtime/unexpected errors in SplurgeSafeIo."""
    _domain = "splurge-safe-io.runtime"

# Step 3: Use your library's exceptions
class FileService:
    def read_config(self, path: str) -> dict:
        try:
            with open(path) as f:
                return json.load(f)
        except FileNotFoundError as e:
            error = SplurgeSafeIoRuntimeError(
                f"Configuration file not found: {path}",
                error_code="config-not-found"
            )
            error.__cause__ = e
            error.attach_context({"path": path})
            raise error
        except json.JSONDecodeError as e:
            error = SplurgeSafeIoValidationError(
                "Configuration file contains invalid JSON",
                error_code="invalid-json"
            )
            error.__cause__ = e
            error.attach_context({"path": path})
            raise error
```

**Results with library-specific exceptions:**
- Full error code: `splurge-safe-io.validation.invalid-json` (origin is clear!)
- Type checking: `except SplurgeSafeIoValidationError` (specific and type-safe)
- Log filtering: Easy to find all `splurge-safe-io.*` errors
- Caller clarity: Knows exactly which library threw the error

**Key Points for Libraries:**
- ✅ **DO** define your own exception hierarchy inheriting from `SplurgeFrameworkError`
- ✅ **DO** use your library name/prefix in domains (e.g., `splurge-safe-io`)
- ✅ **DO** create semantic sub-types for different error categories
- ❌ **DON'T** use the built-in `Splurge*Error` types (they're for apps, not libraries)
- ❌ **DON'T** use bare `SplurgeError` or `SplurgeRuntimeError` from your library

### When to Use Which Approach

| Use Case | Exception Type | Example |
|----------|---|---------|
| Simple app-level error | `SplurgeValueError` | Missing required field |
| App file/OS error | `SplurgeOSError` | File not found in user code |
| Library validation | `YourLibError.ValidationError` | Invalid config in your library |
| Library runtime error | `YourLibError.RuntimeError` | Unexpected failure in your library |
| Framework extension | `SplurgeFrameworkError` | Base for custom hierarchies |

## Library Integration Guide

### Creating Domain-Specific Exceptions

As a library integrator, extend Splurge Exceptions to provide domain-specific error handling:

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
                "Connection string cannot be empty",
                error_code="empty-connection-string"
            )

        if "invalid" in connection_string:
            raise MyLibraryConnectionError(
                "Connection string format is invalid",
                error_code="invalid-connection-format",
                details={"provided": connection_string}
            )

        # Success case
        self.connection = create_connection(connection_string)

    def query(self, sql: str, params=None):
        if not self.connection:
            raise MyLibraryConnectionError(
                "No active database connection",
                error_code="not-connected"
            )

        try:
            return self.connection.execute(sql, params)
        except TimeoutError as e:
            raise wrap_exception(
                e,
                MyLibraryConnectionError,
                "Query execution timed out",
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
                "Authentication token invalid or expired",
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
- Set `__cause__` on wrapped exceptions for clean chain preservation

#### 5. Domain Hierarchy
- Use hierarchical domains: `mylibrary.api.auth`, not just `auth`
- Group related errors under common sub-domains

#### 6. Type Safety
- Use proper type annotations in your error classes
- Document parameter and return types

## Best Practices

### Exception Selection

#### For Applications
- ✅ **DO** use the built-in `Splurge*Error` types for common cases
- ✅ **DO** handle specific exception types with targeted `except` clauses
- ✅ **DO** format errors for end users using `ErrorMessageFormatter`
- ❌ **DON'T** use bare `SplurgeError` - prefer the semantic types

#### For Libraries
- ✅ **DO** define your own exception hierarchy inheriting from `SplurgeFrameworkError`
- ✅ **DO** use your library name in the domain prefix (e.g., `splurge-safe-io`)
- ✅ **DO** create semantic sub-types for different error categories
- ✅ **DO** chain original exceptions with `__cause__`
- ❌ **DON'T** use the built-in `Splurge*Error` types in library code
- ❌ **DON'T** use bare `SplurgeError` or `SplurgeRuntimeError` in libraries

### Error Code Design

- **Descriptive**: Use clear, descriptive names (`file-not-found` vs `fnf`)
- **Consistent**: Follow the same patterns across your library
- **Hierarchical**: Use domain hierarchy for organization (via inheritance)
- **Stable**: Don't change error codes once published (backward compatibility)
- **Lowercase**: Always use lowercase with hyphens (e.g., `invalid-value`, not `InvalidValue`)

### Domain Naming for Libraries

When creating a library like `splurge-safe-io`:

```python
# Good - clear library origin
class SplurgeSafeIoError(SplurgeFrameworkError):
    _domain = "splurge-safe-io"

class SplurgeSafeIoValidationError(SplurgeSafeIoError):
    _domain = "splurge-safe-io.validation"

# Result: Full codes like "splurge-safe-io.validation.invalid-path"

# Bad - generic or ambiguous
class MyError(SplurgeFrameworkError):
    _domain = "error"  # ❌ Not descriptive

class IoError(SplurgeFrameworkError):
    _domain = "io"  # ❌ Conflicts with built-in names
```

### Context Management

- **Relevant**: Only attach context relevant to debugging the error
- **Safe**: Don't include sensitive information (passwords, tokens) in error context
- **Structured**: Use consistent key naming conventions
- **Useful**: Include information that helps developers understand what went wrong
- **Concise**: Keep context data reasonably sized

### Exception Handling

- **Specific**: Catch specific exception types, not broad `Exception`
- **Chaining**: Always preserve exception chains with `from` clause
- **Context**: Add relevant context before re-raising
- **Logging**: Use decorators for consistent logging across your codebase
- **Recovery**: Provide actionable recovery suggestions when possible

### User Experience

- **Clear Messages**: Write error messages for humans, not machines
- **Actionable**: Include suggestions users can actually follow
- **Progressive**: Show basic info first, detailed info on demand
- **Consistent**: Use consistent formatting and terminology
- **Localization**: Consider translation needs for user-facing messages

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
