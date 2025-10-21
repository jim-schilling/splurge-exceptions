# Splurge Exceptions Framework - Usage Examples

This directory contains comprehensive examples demonstrating how to use the Splurge Exceptions Framework in different scenarios.

## Examples

### 1. API Client Usage (`examples/api_client_usage.py`)

Demonstrates how to use the framework in a typical API client library with:

- **Exception Wrapping** - Converting stdlib exceptions to Splurge exceptions
- **Context Managers** - Resource management with error handling and callbacks
- **Decorators** - Automatic exception conversion on function calls
- **Error Formatting** - User-friendly error message output with context and suggestions
- **Chaining** - Building meaningful exception chains with context
- **Composite Workflows** - Combining multiple error handling strategies

**Key Functions:**
- `fetch_user_data()` - Exception wrapping example
- `process_file_with_error_handling()` - Context manager usage
- `parse_json_config()` - Decorator-based conversion
- `handle_api_call_with_formatting()` - Error formatting
- `perform_api_workflow()` - Complete workflow demonstration

**Run:** `python examples/api_client_usage.py`

### 2. API Integrator Usage (`examples/api_integrator_usage.py`)

Demonstrates how a Splurge family library would extend the framework with custom exceptions and register them in the global error code registry. This example shows integration from the perspective of a library like splurge-db, splurge-encoding, or splurge-data.

**Custom Exception Domains:**

- **Database** - SQL parsing, query execution, schema validation
  - `SplurgeDatabaseError` (base)
  - `SplurgeSqlParseError`
  - `SplurgeQueryExecutionError`
  - `SplurgeSchemaError`

- **Encoding** - Unicode handling and character encoding
  - `SplurgeEncodingError` (base)
  - `SplurgeUnicodeDecodeError`
  - `SplurgeUnicodeEncodeError`

- **Data Format** - DSV, JSON, CSV, and schema parsing
  - `SplurgeDataFormatError` (base)
  - `SplurgeDsvFormatError`
  - `SplurgeSchemaParseError`

**Registry Integration:**

The example demonstrates the `ErrorCodeRegistry` API:

```python
from splurge_exceptions import get_global_registry

registry = get_global_registry()

# Register custom exception mappings
registry.register_mapping(CustomException, "domain.category.001")

# Look up mapped error code
code = registry.lookup_exception(CustomException)

# Resolve error code with intelligent algorithm
resolved = registry.resolve_code(source_exception, provided_code)

# List codes by domain
codes = registry.list_codes("database")

# Get all registered codes
all_codes = registry.get_all_codes_info()
```

**Key Functions:**
- `register_splurge_family_error_codes()` - Registry registration
- Database operations - SQL parsing and query execution
- Encoding operations - Unicode encoding/decoding
- Data format operations - DSV and schema parsing
- `process_data_pipeline()` - Complete multi-operation workflow

**Run:** `python examples/api_integrator_usage.py`

## Key Patterns

### Pattern 1: Exception Wrapping

```python
from splurge_exceptions import wrap_exception, SplurgeValidationError

try:
    value = int(user_input)
except ValueError as e:
    error = wrap_exception(
        e,
        SplurgeValidationError,
        error_code="validation.value.001",
    )
    error.attach_context(key="input", value=user_input)
    error.add_suggestion("Provide a valid integer")
    raise error from e
```

### Pattern 2: Context Manager

```python
from splurge_exceptions import error_context, SplurgeOSError, SplurgeValidationError

with error_context(
    exceptions={
        FileNotFoundError: (SplurgeOSError, "os.file.001"),
        ValueError: (SplurgeValidationError, "validation.content.001"),
    },
    context={"file_path": path},
    on_error=lambda e: print(f"Error: {e}"),
    suppress=False,
):
    # Code that might raise exceptions
    process_file(path)
```

### Pattern 3: Decorator

```python
from splurge_exceptions import handle_exceptions, SplurgeValidationError

@handle_exceptions(
    exceptions={
        ValueError: (SplurgeValidationError, "validation.json.001"),
        KeyError: (SplurgeValidationError, "validation.json.002"),
    },
    log_level="warning",
)
def parse_config(json_str: str) -> dict:
    # ValueError and KeyError are automatically converted
    return json.loads(json_str)
```

### Pattern 4: Error Formatting

```python
from splurge_exceptions.formatting.message import ErrorMessageFormatter

formatter = ErrorMessageFormatter()
try:
    # Code that raises SplurgeError
    process_data()
except SplurgeError as e:
    message = formatter.format_error(
        e,
        include_context=True,
        include_suggestions=True,
    )
    print(message)
```

### Pattern 5: Registry Integration

```python
from splurge_exceptions import get_global_registry

registry = get_global_registry()

# Register custom exception mapping
registry.register_mapping(CustomException, "domain.category.001")

# Resolve code using registry
code = registry.resolve_code(CustomException, None)

# List codes by domain
codes = registry.list_codes("domain")
```

## Testing

Both examples are fully tested:

- **Type Safety:** Strict mypy compliance with full type annotations
- **Code Quality:** All ruff linting checks pass
- **Execution:** Both examples run successfully without errors

Run tests:
```bash
python -m ruff check examples/
python -m mypy examples/ --strict
python examples/api_client_usage.py
python examples/api_integrator_usage.py
```

## Integration with CI/CD

These examples can be used in CI/CD pipelines to:
- Validate framework API stability
- Ensure backward compatibility
- Demonstrate framework capabilities
- Serve as regression tests for integration scenarios

## Related Documentation

- [README.md](README.md) - Framework overview
- [API Reference](docs/api/API-REFERENCE.md) - Complete API documentation
- [Test Suite](tests/) - Unit and integration tests

## Contributing

When adding new examples:
1. Keep examples focused and self-contained
2. Include comprehensive docstrings
3. Maintain type safety (mypy strict)
4. Follow code quality guidelines (ruff)
5. Add documentation for new patterns
