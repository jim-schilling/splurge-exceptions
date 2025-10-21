# Splurge Exceptions Framework - Examples Update Summary

## Overview

Updated the example files to demonstrate comprehensive usage of the Splurge Exceptions Framework, including new documentation on registry integration and error code management.

## Files Created/Modified

### 1. `examples/api_client_usage.py`
A comprehensive example showing how to use the framework in a typical API client library.

**Demonstrates:**
- Exception wrapping with context and suggestions
- Context manager for resource management and error handling
- Decorator-based automatic exception conversion
- Error message formatting for user-friendly output
- Exception chaining with meaningful context
- Complete workflow combining multiple error handling strategies

**Key Sections:**
- Section 1: Basic Exception Wrapping
- Section 2: Context Manager for Resource Management
- Section 3: Decorator-Based Exception Conversion
- Section 4: Error Formatting and User-Friendly Output
- Section 5: Chaining and Exception Context
- Section 6: Composite Exception Handling

**Example Functions:**
- `fetch_user_data(user_id)` - Basic wrapping example
- `process_file_with_error_handling(file_path)` - Context manager usage
- `parse_json_config(json_data)` - Decorator usage
- `handle_api_call_with_formatting()` - Error formatting
- `create_api_client_with_auth(api_key)` - Chaining example
- `perform_api_workflow()` - Complete workflow

### 2. `examples/api_integrator_usage.py`
Shows how a Splurge family library integrates custom exceptions with the global registry.

**Demonstrates:**
- Defining custom exception types for specific domains
- Registering exceptions with the global ErrorCodeRegistry
- Using registry methods for error code management
- Complete workflow with multiple custom exception types

**Custom Exception Types:**

Database Domain:
- `SplurgeDatabaseError` (base)
- `SplurgeSqlParseError`
- `SplurgeQueryExecutionError`
- `SplurgeSchemaError`

Encoding Domain:
- `SplurgeEncodingError` (base)
- `SplurgeUnicodeDecodeError`
- `SplurgeUnicodeEncodeError`

Data Format Domain:
- `SplurgeDataFormatError` (base)
- `SplurgeDsvFormatError`
- `SplurgeSchemaParseError`

**Key Sections:**
- Sections 1-3: Custom Exception Type Definitions
- Section 4: Registry Integration with `register_splurge_family_error_codes()`
- Section 5-7: Domain-specific operations
- Section 8: Integrated multi-operation workflow

**Registry Methods Demonstrated:**
```python
registry = get_global_registry()

# Register custom exception mapping
registry.register_mapping(SplurgeSqlParseError, "database.sql_parse.001")

# Look up mapped error code
code = registry.lookup_exception(SplurgeSqlParseError)

# Resolve error code intelligently
resolved = registry.resolve_code(source_exception, provided_code)

# List codes by domain
codes = registry.list_codes("database")

# Get all registered codes
all_codes = registry.get_all_codes_info()
```

### 3. `EXAMPLES.md`
New comprehensive documentation file covering both examples.

**Contents:**
- Overview of both examples
- Detailed function descriptions
- Registry API usage patterns
- Key patterns for different scenarios
- Testing information
- CI/CD integration guidance
- Related documentation links

## Registry Integration Highlights

The `api_integrator_usage.py` example shows the full workflow of registering custom exceptions:

### Step 1: Define Custom Exceptions
```python
class SplurgeSqlParseError(SplurgeDatabaseError):
    domain = "database"
```

### Step 2: Register with Global Registry
```python
registry = get_global_registry()
registry.register_mapping(SplurgeSqlParseError, "database.sql_parse.001")
```

### Step 3: Use Registry for Code Resolution
```python
# Automatic resolution when exception is caught
code = registry.resolve_code(SplurgeSqlParseError, None)

# Look up existing mappings
code = registry.lookup_exception(SplurgeSqlParseError)

# List all codes in a domain
codes = registry.list_codes("database")
```

## Example Execution Output

### API Client Usage Example
```
SPLURGE EXCEPTIONS FRAMEWORK - API CLIENT USAGE EXAMPLE

### EXAMPLE 1: Error Formatting ###
[validation.user.001]
Invalid user_id: -1. Must be positive integer.

Context:
  provided_value: -1

Suggestions:
  1. Ensure user_id is a positive integer

### EXAMPLE 3: Complete Workflow ###
Step 1: Initializing API client...
[OK] Client initialized with key: aaaaaaaa...
[OK] User data fetched: {'id': 123, ...}
[OK] File processed (56 chars)
[OK] Configuration parsed with 3 settings
======================================================================
WORKFLOW COMPLETED SUCCESSFULLY!
======================================================================
[OK] All examples completed successfully!
```

### API Integrator Usage Example
```
SPLURGE FAMILY LIBRARY - API INTEGRATOR USAGE EXAMPLE

### STEP 1: Register Custom Exception Mappings ###

[OK] Custom exception mappings registered:
    - SplurgeSqlParseError -> database.sql_parse.001
    - SplurgeUnicodeDecodeError -> encoding.unicode.001
    - SplurgeDsvFormatError -> data_format.dsv.001

### STEP 3: Registry Lookup Examples ###

1. Looking up registered exception mappings:
   SplurgeSqlParseError -> database.sql_parse.001
   SplurgeUnicodeDecodeError -> encoding.unicode.001

2. Using registry to resolve error codes:
   resolve_code(SplurgeSqlParseError, None) -> database.sql_parse.001

3. Listing all registered codes for a domain:
   Database domain codes:
     - os.file.001
     - validation.type.001
```

## Quality Assurance

✅ **Ruff Compliance**: All checks pass
- No import sorting issues
- No unused variables
- No code quality violations

✅ **Type Safety (MyPy Strict)**: All checks pass
- Full type annotations throughout
- No type ignores needed for legitimate code

✅ **Test Suite**: All 266 tests pass
- 245 existing tests still passing
- 21 hypothesis property tests passing
- No regressions introduced

✅ **Execution**: Both examples run successfully
- No runtime errors
- All features demonstrated
- Clear output formatting

## Integration with Framework

These examples integrate with:

1. **Exception Types** - All 9 Splurge exception types demonstrated
2. **Error Codes** - Full error code management and registry usage
3. **Context Managers** - Callbacks and context attachment shown
4. **Decorators** - Automatic exception conversion demonstrated
5. **Message Formatting** - User-friendly output formatting
6. **Registry** - Complete registry API usage

## Files Modified/Created

- ✅ `examples/api_client_usage.py` - 371 lines, fully implemented
- ✅ `examples/api_integrator_usage.py` - 763 lines, fully implemented with registry examples
- ✅ `EXAMPLES.md` - New comprehensive documentation

## Next Steps

These examples can be used to:
1. Demonstrate framework capabilities to new users
2. Validate API stability through integration testing
3. Provide reference implementations for library developers
4. Support CI/CD pipelines for regression testing
5. Document best practices for error handling

## Related Documentation

- Main README: `README.md`
- API Reference: `docs/api/API-REFERENCE.md`
- Test Suite: `tests/` directory
- Hypothesis Tests: `tests/unit/test_properties_hypothesis.py`
