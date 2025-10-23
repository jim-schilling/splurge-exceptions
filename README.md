# Splurge Exceptions

[![PyPI version](https://badge.fury.io/py/splurge-exceptions.svg)](https://pypi.org/project/splurge-exceptions/)
[![Python versions](https://img.shields.io/pypi/pyversions/splurge-exceptions.svg)](https://pypi.org/project/splurge-exceptions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

[![CI](https://github.com/jim-schilling/splurge-exceptions/actions/workflows/ci-quick-test.yml/badge.svg)](https://github.com/jim-schilling/splurge-exceptions/actions/workflows/ci-quick-test.yml)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](https://github.com/jim-schilling/splurge-exceptions)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-black)](https://mypy-lang.org/)



A comprehensive Python exception management library that provides structured error handling, exception wrapping, and intelligent error code management for modern applications.

## Quick Start

### Installation

```bash
pip install splurge-exceptions
```

### Basic Usage

#### 1. Wrap Exceptions

```python
from splurge_exceptions import wrap_exception, SplurgeValueError

try:
    age = int("not a number")
except ValueError as e:
    error = wrap_exception(
        e,
        SplurgeValueError,
        error_code="invalid-value",
        message="Could not parse age as integer",
    )
    raise error
```

#### 2. Use Context Manager

```python
from splurge_exceptions import error_context, SplurgeValueError

with error_context(
    exceptions={
        ValueError: (SplurgeValueError, "invalid-value"),
    },
    context={"field": "email"},
    suppress=False,
):
    # Your code here
    validate_email(user_input)
```

#### 3. Use Decorator

```python
from splurge_exceptions import handle_exceptions, SplurgeOSError

@handle_exceptions(
    exceptions={
        FileNotFoundError: (SplurgeOSError, "file-not-found"),
    },
    log_level="error",
)
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()
```

#### 4. Format Errors

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

## Key Features

✨ **Exception Wrapping** - Convert any exception to structured Splurge exceptions
🎯 **Error Codes** - Intelligent error code management with domain-based organization
🔄 **Context Managers** - Handle exceptions with optional callbacks and context
🏷️ **Decorators** - Automatic exception conversion on decorated functions
📋 **Message Formatting** - Beautiful, structured error message output
🖥️ **CLI Tools** - Browse error codes and generate documentation
📊 **Type Safe** - Full type annotations with MyPy strict mode support

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
│   ├── wrappers/                # Exception wrapping utilities
│   ├── decorators/              # Decorator utilities
│   ├── managers/                # Context managers
│   ├── formatting/              # Message formatting
│   └── cli.py                   # CLI interface
├── tests/                       # Test suite (245+ tests)
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
└── docs/                        # Documentation
```

## Testing

The library includes comprehensive test coverage:

- **168 tests** - Unit tests (100% passing)
- **100% code coverage** - All public APIs tested
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
