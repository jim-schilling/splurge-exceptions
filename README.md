# Splurge Exceptions

[![PyPI version](https://badge.fury.io/py/splurge-exceptions.svg)](https://pypi.org/project/splurge-exceptions/)
[![Python versions](https://img.shields.io/pypi/pyversions/splurge-exceptions.svg)](https://pypi.org/project/splurge-exceptions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

[![CI](https://github.com/jim-schilling/splurge-exceptions/actions/workflows/ci-quick-test.yml/badge.svg)](https://github.com/jim-schilling/splurge-exceptions/actions/workflows/ci-quick-test.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen.svg)](https://github.com/jim-schilling/splurge-exceptions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-black)](https://mypy-lang.org/)



A comprehensive Python exception management library that provides structured error handling, semantic error codes, and intelligent error organization for Splurge projects.

## Quick Start

### Installation

```bash
pip install splurge-exceptions
```

### Basic Usage

#### 1. Create Structured Exceptions

```python
from splurge_exceptions import SplurgeValueError

# Create a semantic exception with context
error = SplurgeValueError(
    "Email address format is invalid",
    error_code="invalid-email",
    details={"provided": "user@", "expected": "user@domain.com"}
)

# Attach context and suggestions
error.attach_context("user_id", 12345)
error.add_suggestion("Use format: username@domain.com")
error.add_suggestion("Verify domain is included")

# Full error code: "splurge.value.invalid-email"
print(error.full_code)
```

#### 2. Convert Exceptions with Chaining

```python
from splurge_exceptions import SplurgeValueError

try:
    # Some operation that might fail
    int("invalid")
except ValueError as e:
    # Wrap the exception with structured error
    wrapped = SplurgeValueError(
        "Could not parse input as integer",
        error_code="invalid-integer",
        details={"input": "invalid"}
    )
    raise wrapped from e
```

#### 3. Format Errors for Users

```python
from splurge_exceptions import ErrorMessageFormatter

formatter = ErrorMessageFormatter()
formatted = formatter.format_error(
    error,
    include_context=True,
    include_suggestions=True,
)
print(formatted)
```

#### 4. Integration Support for Splurge Family Libraries
```python
from splurge_exceptions import SplurgeFrameworkError

class SplurgeSafeIoError(SplurgeFrameworkError):
    _domain = "splurge-safe-io"

class SplurgeSafeIoRuntimeError(SplurgeSafeIoError):
    _domain = "splurge-safe-io.runtime"

raise SplurgeSafeIoRuntimeError(
    "Unexpected error occurred",
    error_code="unexpected",
)
# Resulting full error code: "splurge-safe-io.runtime.unexpected"
```

## Key Features

🎯 **Semantic Error Codes** - Hierarchical error codes with domain organization  
� **Exception Chaining** - Preserve exception chains with `raise ... from`  
📋 **Context Attachment** - Add operation context and recovery suggestions  
� **Message Formatting** - Beautiful, structured error message output  
� **Type Safe** - Full type annotations with MyPy strict mode support  
🎭 **Framework Extensions** - Clean extension points for domain-specific exceptions

## Exception Types

Splurge Exceptions provides 9 exception types for different error scenarios:

- `SplurgeError` - Base exception class
- `SplurgeValueError` - Input validation errors
- `SplurgeOSError` - Operating system errors
- `SplurgeRuntimeError` - Runtime execution errors
- `SplurgeTypeError` - Type errors
- `SplurgeAttributeError` - Missing object attributes/methods
- `SplurgeImportError` - Module import failures
- `SplurgeLookupError` - Lookup errors
- `SplurgeFrameworkError` - Framework-level errors
- `SplurgeSubclassError` - Framework misconfiguration errors (used internally)

## Documentation

- **[README-DETAILS.md](docs/README-DETAILS.md)** - Comprehensive feature documentation and examples
- **[API-REFERENCE.md](docs/api/API-REFERENCE.md)** - Complete API reference
- **[CLI-REFERENCE.md](docs/cli/CLI-REFERENCE.md)** - CLI tools reference
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

## Project Structure

```
splurge-exceptions/
├── splurge_exceptions/          # Main package
│   ├── core/                    # Core exceptions and error codes
│   ├── formatting/              # Message formatting utilities
│   ├── context/                 # Context utilities
│   └── cli.py                   # CLI interface
├── tests/                       # Test suite (130+ tests)
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
└── docs/                        # Documentation
```

## Testing

The library includes comprehensive test coverage:

- **130 tests** - Unit tests (100% passing)
- **94% code coverage** - All public APIs tested
- **MyPy strict mode** - Full type safety validation
- **Ruff linting** - Code quality enforcement

Run tests:
```bash
pytest tests/
pytest tests/ --cov=splurge_exceptions --cov-report=html
```

## License

MIT License - See [LICENSE](LICENSE) file for details

## Author

Jim Schilling
