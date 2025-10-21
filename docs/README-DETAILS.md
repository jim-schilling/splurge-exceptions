# Splurge Exceptions - Comprehensive Documentation

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Installation](#installation)
4. [Exception Types](#exception-types)
5. [Features](#features)
6. [Usage Guide](#usage-guide)
7. [Advanced Usage](#advanced-usage)
8. [Error Codes](#error-codes)
9. [Testing](#testing)
10. [References](#references)

## Overview

Splurge Exceptions is a comprehensive Python exception management library designed for modern applications requiring structured error handling, semantic error codes, and consistent exception management across layers.

### Why Splurge Exceptions?

- **Structured Error Handling**: Replace ad-hoc exception handling with standardized, hierarchical exception types
- **Semantic Error Codes**: User-defined, domain-organized error codes without registry overhead
- **Context & Suggestions**: Attach contextual information and recovery suggestions to exceptions
- **Multiple Integration Patterns**: Decorators, context managers, and explicit wrapping
- **Type Safe**: Full type annotations with MyPy strict mode support
- **Production Ready**: 100% test coverage with 168 comprehensive unit tests

## Core Concepts

### Error Codes (v2025.0.0+)

Error codes in Splurge Exceptions use a **hierarchical domain system with semantic codes**:

**Format:**
```
domain[.subdomain[.subsubdomain]].semantic-error-code
```

**Examples:**
- `validation.invalid-value` - Validation domain, invalid-value error
- `database.sql.query.timeout` - Database > SQL > Query domain, timeout error
- `os.file-not-found` - OS domain, file-not-found error
- `authentication.user-not-found` - Authentication domain, user-not-found error

**Key Rules:**
- **Domains**: Can contain multiple dot-separated levels (e.g., `database.sql.query`)
- **Error Codes**: User-supplied semantic identifiers, NO dots allowed (e.g., `invalid-value`, `timeout`)
- **Validation**: Both domains and error codes must match: `[a-z][a-z0-9-]*[a-z0-9]`

### Exception Hierarchy

```
BaseException
└── Exception
    └── SplurgeError (custom base)
        ├── SplurgeValidationError (domain: "validation")
        ├── SplurgeOSError (domain: "os")
        ├── SplurgeConfigurationError (domain: "config")
        ├── SplurgeRuntimeError (domain: "runtime")
        ├── SplurgeAuthenticationError (domain: "authentication")
        ├── SplurgeAuthorizationError (domain: "authorization")
        ├── SplurgeNotImplementedError (domain: "runtime")
        └── SplurgeFrameworkError (domain: "framework")
```

### Key Attributes

Every Splurge exception includes:
- `error_code` - User-defined semantic error code (e.g., "invalid-value")
- `full_code` - Complete hierarchical code including domain (e.g., "validation.invalid-value")
- `domain` - Exception domain hierarchy (e.g., "validation")
- `message` - Human-readable error message
- `details` - Additional detail dictionary
- `severity` - Error severity level ("info", "warning", "error", "critical")
- `recoverable` - Whether the error can be recovered from
- Context - Attached contextual data
- Suggestions - Recovery suggestions

## Installation

### From PyPI

```bash
pip install splurge-exceptions
```

### From Source

```bash
git clone https://github.com/jim-schilling/splurge-exceptions
cd splurge-exceptions
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/jim-schilling/splurge-exceptions
cd splurge-exceptions
pip install -e ".[dev]"
pytest tests/
```

## Exception Types

### SplurgeError

Base exception class for all Splurge exceptions.

```python
from splurge_exceptions import SplurgeError

# Cannot be instantiated directly - must use a subclass
# Subclasses must define _domain class attribute

try:
    # Some operation
    pass
except SplurgeError as e:
    print(f"Error Code: {e.error_code}")  # "invalid-value"
    print(f"Full Code: {e.full_code}")    # "validation.invalid-value"
    print(f"Domain: {e.domain}")          # "validation"
    print(f"Message: {e.message}")
    print(f"Context: {e.get_context()}")
    print(f"Suggestions: {e.get_suggestions()}")
```

### SplurgeValidationError

Used for input validation errors.

```python
from splurge_exceptions import wrap_exception, SplurgeValidationError

try:
    age = int(user_input)
    if age < 0:
        raise ValueError("Age cannot be negative")
except ValueError as e:
    error = wrap_exception(
        e,
        SplurgeValidationError,
        error_code="invalid-value",  # NO dots in error code
        message="Age must be positive",
    )
    error.attach_context(key="provided_value", value=user_input)
    error.add_suggestion("Provide a positive integer")
    raise error
```

**Domain:** `validation`

**Common Error Codes:**
- `invalid-value` - Invalid value
- `type-mismatch` - Type mismatch
- `out-of-range` - Value out of range
- `invalid-format` - Invalid format
- `invalid-email` - Invalid email
- `required-field` - Required field missing

### SplurgeOSError

Used for operating system and file-related errors.

```python
from splurge_exceptions import handle_exceptions, SplurgeOSError

@handle_exceptions(
    exceptions={
        FileNotFoundError: (SplurgeOSError, "file-not-found"),
        PermissionError: (SplurgeOSError, "permission-denied"),
    }
)
def read_configuration(path: str) -> str:
    with open(path) as f:
        return f.read()
```

**Domain:** `os`

**Common Error Codes:**
- `file-not-found` - File not found
- `permission-denied` - Permission denied
- `io-error` - I/O error

### SplurgeConfigurationError

Used for configuration and setup issues.

```python
from splurge_exceptions import SplurgeConfigurationError

if not config.get("database_url"):
    error = SplurgeConfigurationError(
        error_code="config.database.001",
        message="Database URL not configured",
    )
    error.add_suggestion("Set DATABASE_URL environment variable")
    raise error
```

### SplurgeRuntimeError

Used for runtime execution errors.

```python
from splurge_exceptions import SplurgeRuntimeError

if result is None:
    error = SplurgeRuntimeError(
        error_code="runtime.processing.001",
        message="Processing returned null result",
    )
    raise error
```

### SplurgeAuthenticationError

Used for authentication failures.

```python
from splurge_exceptions import SplurgeAuthenticationError

if not token.is_valid():
    error = SplurgeAuthenticationError(
        error_code="auth.token.001",
        message="Invalid authentication token",
    )
    raise error
```

### SplurgeAuthorizationError

Used for authorization/permission failures.

```python
from splurge_exceptions import SplurgeAuthorizationError

if not user.has_permission("admin"):
    error = SplurgeAuthorizationError(
        error_code="auth.permission.001",
        message="User lacks required permissions",
    )
    raise error
```

### SplurgeNotImplementedError

Used for unimplemented features.

```python
from splurge_exceptions import SplurgeNotImplementedError

if feature_flag.is_disabled():
    error = SplurgeNotImplementedError(
        error_code="feature.export.001",
        message="CSV export is not yet implemented",
    )
    error.add_suggestion("Feature will be available in v2.0")
    raise error
```

### SplurgeFrameworkError

Used for framework-level errors.

```python
from splurge_exceptions import SplurgeFrameworkError

if not isinstance(middleware, BaseMiddleware):
    error = SplurgeFrameworkError(
        error_code="framework.middleware.001",
        message="Invalid middleware type",
    )
    raise error
```

## Features

### 1. Exception Wrapping

Convert any exception to a structured Splurge exception.

```python
from splurge_exceptions import wrap_exception, SplurgeValidationError

try:
    value = int("invalid")
except ValueError as original:
    # Wrap the original exception
    wrapped = wrap_exception(
        original,
        SplurgeValidationError,
        error_code="validation.integer.001",
        message="Please provide a valid integer",
    )
    
    # Add context
    wrapped.attach_context(context_dict={
        "field": "age",
        "input": "invalid",
        "expected_type": "integer",
    })
    
    # Add suggestions
    wrapped.add_suggestion("Check that the input contains only digits")
    wrapped.add_suggestion("Use the age validation endpoint for assistance")
    
    raise wrapped
```

**Features:**
- Preserves exception chain (`__cause__`)
- Automatic error code resolution
- Context and suggestion attachment
- Message customization

### 2. Context Manager

Handle exceptions with optional callbacks and context.

```python
from splurge_exceptions import error_context, SplurgeValidationError

success_count = 0
error_count = 0

def on_success() -> None:
    global success_count
    success_count += 1

def on_error(exc: Exception) -> None:
    global error_count
    error_count += 1
    print(f"Error occurred: {exc}")

with error_context(
    exceptions={
        ValueError: (SplurgeValidationError, "validation.value.001"),
    },
    context={
        "operation": "user_registration",
        "timestamp": datetime.now().isoformat(),
    },
    on_success=on_success,
    on_error=on_error,
    suppress=False,
):
    # Your code here - if ValueError is raised, it will be:
    # 1. Wrapped to SplurgeValidationError
    # 2. Have context attached
    # 3. Trigger on_error callback
    validate_user_input(data)
```

**Features:**
- Exception mapping and automatic conversion
- Context attachment
- Callback execution (on_success, on_error)
- Exception suppression option
- Support for nested contexts

### 3. Decorator

Automatically convert exceptions on decorated functions.

```python
from splurge_exceptions import handle_exceptions, SplurgeOSError, SplurgeValidationError

@handle_exceptions(
    exceptions={
        FileNotFoundError: (SplurgeOSError, "os.file.001"),
        ValueError: (SplurgeValidationError, "validation.value.001"),
    },
    log_level="error",
    reraise=True,
    include_traceback=True,
)
def process_file(path: str) -> str:
    if not isinstance(path, str):
        raise TypeError("Path must be string")
    
    with open(path) as f:
        content = f.read()
        if not content.strip():
            raise ValueError("File is empty")
    
    return content
```

**Features:**
- Automatic exception conversion
- Configurable logging
- Optional re-raising
- Traceback inclusion
- Works with methods, classmethods, staticmethods

### 4. Message Formatting

Format exceptions into readable, structured output.

```python
from splurge_exceptions import ErrorMessageFormatter

formatter = ErrorMessageFormatter()

error = wrap_exception(
    ValueError("Invalid email"),
    SplurgeValidationError,
    error_code="validation.email.001",
)
error.attach_context(context_dict={
    "field": "email",
    "input": "invalid@",
    "endpoint": "/api/users",
})
error.add_suggestion("Use valid email format: user@example.com")
error.add_suggestion("Check RFC 5322 specification")

# Format complete message
message = formatter.format_error(
    error,
    include_context=True,
    include_suggestions=True,
)

print(message)
# Output:
# [validation.email.001] Invalid email
# Context:
#   field: email
#   input: invalid@
#   endpoint: /api/users
# Suggestions:
#   1. Use valid email format: user@example.com
#   2. Check RFC 5322 specification
```

**Methods:**
- `format_error(error, include_context, include_suggestions)` - Format complete error
- `format_context(context_dict)` - Format context only
- `format_suggestions(suggestions)` - Format suggestions only

### 5. CLI Tools

Browse error codes and generate documentation.

```bash
# Show specific error code
python -m splurge_exceptions show-code validation.value.001

# List all error codes
python -m splurge_exceptions list-codes

# List codes in domain
python -m splurge_exceptions list-codes --domain auth

# Generate documentation
python -m splurge_exceptions generate-docs --format markdown
```

See [CLI-REFERENCE.md](cli/CLI-REFERENCE.md) for complete CLI documentation.

## Usage Guide

### Scenario 1: User Registration

```python
from splurge_exceptions import error_context, SplurgeValidationError, SplurgeConfigurationError

def register_user(email: str, password: str) -> None:
    """Register a new user with validation."""
    
    with error_context(
        exceptions={
            ValueError: (SplurgeValidationError, "validation.user.001"),
            KeyError: (SplurgeConfigurationError, "config.database.001"),
        },
        context={
            "operation": "register_user",
            "email": email,
        },
    ):
        # Validate email
        if "@" not in email:
            raise ValueError("Invalid email format")
        
        # Validate password
        if len(password) < 8:
            raise ValueError("Password too short")
        
        # Save to database
        db.users.insert({"email": email, "password": hash_password(password)})
```

### Scenario 2: File Processing

```python
from splurge_exceptions import handle_exceptions, SplurgeOSError

@handle_exceptions(
    exceptions={
        FileNotFoundError: (SplurgeOSError, "os.file.001"),
        PermissionError: (SplurgeOSError, "os.permission.001"),
        IOError: (SplurgeOSError, "os.io.001"),
    },
    log_level="error",
)
def read_and_process_file(path: str) -> list[str]:
    """Read and process a file."""
    with open(path) as f:
        lines = f.readlines()
    
    return [line.strip() for line in lines]
```

### Scenario 3: Configuration Loading

```python
from splurge_exceptions import SplurgeConfigurationError, ErrorMessageFormatter

def load_configuration(config_path: str) -> dict:
    """Load and validate configuration."""
    import json
    
    try:
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError as e:
        error = wrap_exception(
            e,
            SplurgeConfigurationError,
            error_code="config.file.001",
        )
        error.add_suggestion(f"Create {config_path} with required settings")
        raise error
    except json.JSONDecodeError as e:
        error = wrap_exception(
            e,
            SplurgeConfigurationError,
            error_code="config.invalid.001",
        )
        error.add_suggestion("Fix JSON syntax in configuration file")
        raise error
    
    # Validate required keys
    required_keys = ["database_url", "api_key"]
    for key in required_keys:
        if key not in config:
            error = SplurgeConfigurationError(
                error_code="config.missing.001",
                message=f"Missing required configuration: {key}",
            )
            formatter = ErrorMessageFormatter()
            print(formatter.format_error(error, include_suggestions=True))
            raise error
    
    return config
```

## Advanced Usage

### Creating Custom Exception Domains

Define custom exception classes with specific domain hierarchies:

```python
from splurge_exceptions import SplurgeError

# Create custom exception with hierarchical domain
class BillingError(SplurgeError):
    """Exception for billing-related errors."""
    _domain = "billing.payments"

class CreditCardValidationError(SplurgeError):
    """Exception for credit card validation."""
    _domain = "billing.payments.card-validation"

# Use custom exceptions with semantic error codes
try:
    validate_credit_card(card_number)
except ValueError as e:
    error = wrap_exception(
        e,
        CreditCardValidationError,
        error_code="invalid-card-number",  # NO dots allowed!
        message="Credit card validation failed",
    )
    error.attach_context(
        key="card_last_four",
        value=card_number[-4:],
    )
    error.add_suggestion("Verify card number, expiry date, and CVV")
    raise error

# Full code will be: "billing.payments.card-validation.invalid-card-number"
```

### Exception Mapping Dictionary

Create reusable exception mappings with semantic error codes:

```python
from splurge_exceptions import (
    error_context,
    SplurgeValidationError,
    SplurgeOSError,
    SplurgeConfigurationError,
)

# Define mapping once
FILE_PROCESSING_EXCEPTIONS = {
    FileNotFoundError: (SplurgeOSError, "file-not-found"),
    PermissionError: (SplurgeOSError, "permission-denied"),
    IOError: (SplurgeOSError, "io-error"),
    ValueError: (SplurgeValidationError, "invalid-content"),
}

# Reuse in multiple places
with error_context(exceptions=FILE_PROCESSING_EXCEPTIONS):
    process_file(path)
```

### Chaining Exceptions

Exceptions automatically preserve chains:

```python
from splurge_exceptions import wrap_exception, SplurgeValidationError, SplurgeRuntimeError

try:
    try:
        raise ValueError("Invalid input")
    except ValueError as e:
        wrapped1 = wrap_exception(e, SplurgeValidationError, "validation.001")
        raise wrapped1
except SplurgeValidationError as e:
    wrapped2 = wrap_exception(e, SplurgeRuntimeError, "runtime.001")
    raise wrapped2

# Access full chain:
# wrapped2.__cause__ == wrapped1
# wrapped1.__cause__ == original ValueError
```

### Async Support

Use in async functions:

```python
from splurge_exceptions import error_context, SplurgeValidationError

async def validate_async_data(data: dict) -> None:
    """Validate data asynchronously."""
    
    with error_context(
        exceptions={
            ValueError: (SplurgeValidationError, "validation.async.001"),
        },
    ):
        # Async validation
        result = await validator.validate(data)
        if not result.is_valid:
            raise ValueError(result.errors)
```

## Error Codes

Splurge Exceptions uses **semantic error codes** organized by domain hierarchy:

### Error Code Format

```
domain[.subdomain].semantic-code
```

Examples:
- `validation.invalid-value`
- `database.sql.query.timeout`
- `os.file-not-found`

**Rules:**
- **Domains**: Can have multiple levels separated by dots
- **Error Codes**: Must NOT contain dots, are user-supplied
- **Pattern**: Both must match `[a-z][a-z0-9-]*[a-z0-9]`

### Validation Domain
- `invalid-value` - Invalid value
- `type-mismatch` - Invalid type
- `out-of-range` - Value out of range
- `invalid-format` - Invalid format
- `invalid-email` - Invalid email
- `required-field` - Required field missing

### OS Domain
- `file-not-found` - File not found
- `permission-denied` - Permission denied
- `io-error` - I/O error

### Configuration Domain
- `missing-key` - Configuration missing
- `invalid-value` - Invalid configuration
- `parse-error` - Configuration parsing error

### Authentication Domain
- `user-not-found` - User not found
- `invalid-token` - Invalid token
- `token-expired` - Token expired

### Runtime Domain
- `operation-failed` - General runtime error
- `not-implemented` - Feature not implemented
- `timeout` - Operation timeout

See [API-REFERENCE.md](api/API-REFERENCE.md) for complete reference.

## Testing

The library includes comprehensive test coverage:

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest tests/ --cov=splurge_exceptions --cov-report=html
```

### Run Specific Test Suite

```bash
# Unit tests only
pytest tests/unit/

# Specific test file
pytest tests/unit/test_wrappers_stdlib_basic.py

# Specific test class
pytest tests/unit/test_core_base_basic.py::TestSplurgeErrorInstantiation
```

### Code Quality

```bash
# Linting
ruff check splurge_exceptions/

# Type checking
mypy splurge_exceptions/ --strict
```

### Test Metrics

- **168 unit tests** - Comprehensive coverage
- **100% code coverage** - All public APIs tested
- **0 linting errors** - Clean codebase
- **0 type errors** - Strict type safety

## References

- **[API-REFERENCE.md](api/API-REFERENCE.md)** - Complete API documentation
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history
- **[GitHub Repository](https://github.com/jim-schilling/splurge-exceptions)** - Source code

## Support & Contributing

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/jim-schilling/splurge-exceptions).

## License

MIT License - See [LICENSE](../LICENSE) file for details

## Author

Jim Schilling
