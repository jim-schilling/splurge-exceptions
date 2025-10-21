# ErrorCodeRegistry Usage Guide

This guide shows how to use the `ErrorCodeRegistry` to register and manage custom exception codes in the Splurge Exceptions Framework.

## Overview

The `ErrorCodeRegistry` is a central component that:
- Maps custom exception types to error codes
- Provides intelligent error code resolution
- Stores and retrieves error code descriptions
- Lists codes by domain

## Registry Methods

### 1. `register_mapping(exception_class, error_code)`

Register a custom exception class with a default error code.

```python
from splurge_exceptions import get_global_registry

registry = get_global_registry()

# Map custom exception to error code
registry.register_mapping(SplurgeSqlParseError, "database.sql_parse.001")
registry.register_mapping(SplurgeUnicodeDecodeError, "encoding.unicode.001")
```

**Use Cases:**
- Initialize library's exception mappings
- Enable automatic code resolution
- Document default error codes

---

### 2. `lookup_exception(exception_class)`

Look up the registered error code for an exception class.

```python
# Get the mapped error code
code = registry.lookup_exception(SplurgeSqlParseError)
print(code)  # Output: "database.sql_parse.001"

# Returns None if not found
code = registry.lookup_exception(CustomException)
print(code)  # Output: None
```

**Use Cases:**
- Check if an exception is registered
- Get default error code for an exception
- Document exception mappings

---

### 3. `resolve_code(source_exception, provided_error_code)`

Resolve the appropriate error code using intelligent algorithm.

```python
# Use mapped code (no provided code)
code = registry.resolve_code(SplurgeSqlParseError, None)
print(code)  # Output: "database.sql_parse.001"

# Use provided fully-qualified code
code = registry.resolve_code(SplurgeSqlParseError, "database.sql_parse.002")
print(code)  # Output: "database.sql_parse.002"

# Pad partial code specification
code = registry.resolve_code(ValueError, "validation")
print(code)  # Output: "validation.generic.000"

# Fallback for unmapped exceptions
code = registry.resolve_code(CustomException, None)
print(code)  # Output: "generic.generic.000"
```

**Resolution Algorithm:**
1. If provided_code is fully qualified (e.g., "os.file.001"), use it
2. Else if exception has built-in mapping, use mapped code
3. Else if provided_code is partial, pad with `.000`
4. Else return "generic.generic.000"

---

### 4. `get_code_info(error_code)`

Get the description for an error code.

```python
# Get description for a code
description = registry.get_code_info("os.file.001")
print(description)  # Output: "File not found"

# Returns None if not found
description = registry.get_code_info("unknown.code.001")
print(description)  # Output: None
```

**Use Cases:**
- Document error codes
- User-friendly error messages
- API documentation generation

---

### 5. `list_codes(domain=None)`

List all registered error codes, optionally filtered by domain.

```python
# List all registered codes
all_codes = registry.list_codes()
print(all_codes)  # Output: ['os.file.001', 'os.file.002', ...]

# List codes for specific domain
db_codes = registry.list_codes("database")
print(db_codes)  # Output: ['database.sql_parse.001', 'database.query.001', ...]

# List codes for encoding domain
encoding_codes = registry.list_codes("encoding")
print(encoding_codes)  # Output: ['encoding.unicode.001', ...]
```

**Use Cases:**
- Document available error codes
- Generate error code references
- Domain-specific error handling

---

### 6. `get_all_codes_info()`

Get all code descriptions as a dictionary.

```python
# Get all codes and descriptions
all_info = registry.get_all_codes_info()
print(len(all_info))  # Output: 16

# Iterate over all codes
for code, description in all_info.items():
    print(f"{code}: {description}")

# Output:
# os.generic.000: Generic OS/system error (unmapped)
# os.file.001: File not found
# os.file.002: File exists
# ...
```

**Use Cases:**
- Generate comprehensive error code documentation
- Populate error code lookup tables
- API reference generation

---

## Complete Example: Registering a Custom Library

```python
from splurge_exceptions import SplurgeError, get_global_registry

# Step 1: Define custom exceptions
class SplurgeCustomError(SplurgeError):
    domain = "custom"

class SplurgeCustomParseError(SplurgeCustomError):
    domain = "custom"

class SplurgeCustomExecutionError(SplurgeCustomError):
    domain = "custom"

# Step 2: Register exceptions during library initialization
def init_custom_library():
    registry = get_global_registry()
    
    # Register exception mappings
    registry.register_mapping(
        SplurgeCustomParseError,
        "custom.parse.001"
    )
    registry.register_mapping(
        SplurgeCustomExecutionError,
        "custom.execution.001"
    )
    
    print("Custom library exceptions registered!")

# Step 3: Use registry to resolve codes automatically
def process_with_auto_code_resolution(data):
    try:
        # Code that might raise SplurgeCustomParseError
        parse_data(data)
    except SplurgeCustomParseError as e:
        # Registry automatically resolves to "custom.parse.001"
        registry = get_global_registry()
        code = registry.resolve_code(SplurgeCustomParseError, None)
        print(f"Error code: {code}")  # Output: "Error code: custom.parse.001"
        raise

# Step 4: Query registry for error information
def show_available_codes():
    registry = get_global_registry()
    
    # List all custom codes
    custom_codes = registry.list_codes("custom")
    print(f"Available custom error codes: {custom_codes}")
    
    # Get code descriptions
    for code in custom_codes:
        desc = registry.get_code_info(code)
        print(f"  {code}: {desc}")
```

## Error Code Format

All error codes follow the standard format: `domain.category.code`

**Examples:**
- `validation.value.001` - Validation domain, value category, code 001
- `database.sql_parse.001` - Database domain, sql_parse category, code 001
- `encoding.unicode.001` - Encoding domain, unicode category, code 001

**Format Rules:**
- `domain`: Short identifier (e.g., "os", "validation", "database")
- `category`: Sub-domain (e.g., "file", "type", "query")
- `code`: Numeric code 000-999

---

## Best Practices

### 1. Register During Initialization
```python
# good: Register in module __init__.py
def _init_exceptions():
    registry = get_global_registry()
    registry.register_mapping(CustomException, "custom.type.001")

_init_exceptions()
```

### 2. Use Meaningful Domains
```python
# good: Clear, domain-specific naming
registry.register_mapping(SplurgeDbError, "database.query.001")
registry.register_mapping(SplurgeDataError, "data_format.csv.001")

# avoid: Generic naming
registry.register_mapping(CustomError, "error.error.001")
```

### 3. Document Error Codes
```python
# good: Clear descriptions
code_descriptions = {
    "database.query.001": "Query execution timeout",
    "database.query.002": "Query returned no results",
}

# avoid: Vague descriptions
code_descriptions = {
    "database.query.001": "DB error",
    "database.query.002": "No data",
}
```

### 4. Resolve Codes Consistently
```python
# good: Use registry for automatic resolution
registry = get_global_registry()
code = registry.resolve_code(exception_type, None)

# acceptable: Use explicit code
error = SplurgeError(error_code="database.query.001")

# avoid: Hardcoding everywhere
code1 = "database.query.001"
code2 = "database.query.001"
code3 = "database.query.001"
```

---

## Testing Registry Integration

```python
import pytest
from splurge_exceptions import get_global_registry

def test_exception_registration():
    registry = get_global_registry()
    
    # Test mapping exists
    code = registry.lookup_exception(CustomException)
    assert code == "custom.type.001"

def test_code_resolution():
    registry = get_global_registry()
    
    # Test automatic resolution
    code = registry.resolve_code(CustomException, None)
    assert code == "custom.type.001"

def test_list_domain_codes():
    registry = get_global_registry()
    
    # Test domain filtering
    codes = registry.list_codes("custom")
    assert "custom.type.001" in codes

def test_code_info_lookup():
    registry = get_global_registry()
    
    # Test description retrieval
    info = registry.get_code_info("os.file.001")
    assert info == "File not found"
```

---

## Related Documentation

- [API Client Usage](examples/api_client_usage.py)
- [API Integrator Usage](examples/api_integrator_usage.py)
- [Main Examples Guide](EXAMPLES.md)
- [API Reference](docs/api/API-REFERENCE.md)
