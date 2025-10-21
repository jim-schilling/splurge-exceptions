"""API Integrator Usage Example - Splurge Family Library Integration.

This example demonstrates how a library in the Splurge family
(e.g., splurge-db, splurge-encoding, splurge-data) would leverage the
splurge-exceptions framework to define domain-specific exceptions and
integrate with the exception management system.

This library defines custom exceptions for:
- Database operations (SQL parsing, query execution)
- Data encoding/decoding (Unicode errors, format parsing)
- Data format handling (DSV, JSON, CSV parsing)

The library provides semantic error codes for consistent error management
across the Splurge ecosystem. Each exception includes a domain and semantic
error code that clearly identifies the error condition.
"""

from typing import Any

from splurge_exceptions import (
    SplurgeError,
    error_context,
    handle_exceptions,
    wrap_exception,
)
from splurge_exceptions.formatting.message import ErrorMessageFormatter

# ============================================================================
# Section 1: Custom Exception Types for Splurge-DB Library
# ============================================================================


class SplurgeDatabaseError(SplurgeError):
    """Base exception for database-related errors.

    Used by splurge-db library for all database operation failures.
    This is a custom exception that extends SplurgeError to participate
    in the splurge-exceptions framework.
    """

    _domain = "database"


class SplurgeSqlParseError(SplurgeDatabaseError):
    """Exception for SQL parsing failures.

    Raised when SQL query parsing, validation, or syntax analysis fails.

    Example:
        >>> raise SplurgeSqlParseError(
        ...     error_code="sql-parse-error",
        ...     message="Invalid SQL syntax in WHERE clause"
        ... )
    """

    _domain = "database"


class SplurgeQueryExecutionError(SplurgeDatabaseError):
    """Exception for query execution failures.

    Raised when SQL query execution fails, including database-level errors.

    Example:
        >>> raise SplurgeQueryExecutionError(
        ...     error_code="query-timeout",
        ...     message="Query timeout after 30 seconds"
        ... )
    """

    _domain = "database"


class SplurgeSchemaError(SplurgeDatabaseError):
    """Exception for database schema-related errors.

    Raised when schema validation, migration, or structure errors occur.
    """

    _domain = "database"


# ============================================================================
# Section 2: Custom Exception Types for Splurge-Encoding Library
# ============================================================================


class SplurgeEncodingError(SplurgeError):
    """Base exception for encoding/decoding errors.

    Used by splurge-encoding library for all character encoding operations.
    """

    _domain = "encoding"


class SplurgeUnicodeDecodeError(SplurgeEncodingError):
    """Exception for Unicode decoding failures.

    Raised when decoding bytes to string fails due to encoding issues.

    Example:
        >>> raise SplurgeUnicodeDecodeError(
        ...     error_code="unicode-decode-error",
        ...     message="Invalid UTF-8 sequence at position 42"
        ... )
    """

    _domain = "encoding"


class SplurgeUnicodeEncodeError(SplurgeEncodingError):
    """Exception for Unicode encoding failures.

    Raised when encoding string to bytes fails due to encoding constraints.
    """

    _domain = "encoding"


# ============================================================================
# Section 3: Custom Exception Types for Splurge-Data Library
# ============================================================================


class SplurgeDataFormatError(SplurgeError):
    """Base exception for data format errors.

    Used by splurge-data library for all data format parsing and validation.
    """

    _domain = "data_format"


class SplurgeDsvFormatError(SplurgeDataFormatError):
    """Exception for DSV (Delimited Separated Values) format errors.

    Raised when parsing or validating DSV files fails.

    Example:
        >>> raise SplurgeDsvFormatError(
        ...     error_code="dsv-format-error",
        ...     message="Inconsistent field count in row 5"
        ... )
    """

    _domain = "data_format"


class SplurgeSchemaParseError(SplurgeDataFormatError):
    """Exception for data schema parsing failures.

    Raised when schema definition parsing or validation fails.
    """

    _domain = "data_format"


# ============================================================================
# Section 4: Database Operations with Custom Exceptions
# ============================================================================


@handle_exceptions(
    exceptions={
        SyntaxError: (SplurgeSqlParseError, "sql-syntax-error"),
        ValueError: (SplurgeSqlParseError, "invalid-sql"),
    },
    log_level="error",
)
def parse_sql_query(sql: str) -> dict[str, Any]:
    """Parse SQL query with validation.

    Args:
        sql: SQL query string to parse

    Returns:
        Parsed query structure

    Raises:
        SplurgeSqlParseError: If SQL parsing fails
    """
    if not sql.strip():
        raise ValueError("SQL query cannot be empty")

    if "DROP" in sql.upper() and "PRODUCTION" in sql.upper():
        raise SyntaxError("Dangerous operation not allowed")

    # Simulate parsing
    return {
        "type": "SELECT",
        "tables": ["users"],
        "fields": ["*"],
        "raw": sql,
    }


def execute_database_query(query: str, timeout_seconds: float = 30.0) -> list[dict[str, Any]]:
    """Execute database query with timeout handling.

    Args:
        query: SQL query to execute
        timeout_seconds: Query timeout in seconds

    Returns:
        Query results

    Raises:
        SplurgeQueryExecutionError: If query execution fails
    """
    context_data = {
        "query": query[:50] + "..." if len(query) > 50 else query,
        "timeout_seconds": timeout_seconds,
    }

    def on_error(exc: Exception) -> None:
        """Handle query execution errors."""
        print(f"Query execution error: {exc}")

    with error_context(
        exceptions={
            TimeoutError: (SplurgeQueryExecutionError, "query-timeout"),
            RuntimeError: (SplurgeQueryExecutionError, "query-error"),
        },
        context=context_data,
        on_error=on_error,
        suppress=False,
    ):
        # Simulate query execution
        if "timeout" in query.lower():
            raise TimeoutError(f"Query exceeded {timeout_seconds}s timeout")

        if "no_results" in query.lower():
            raise RuntimeError("Query produced no results")

        # Return mock results
        return [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ]


def validate_database_schema(schema_def: dict[str, Any]) -> bool:
    """Validate database schema definition.

    Args:
        schema_def: Schema definition dictionary

    Returns:
        True if schema is valid

    Raises:
        SplurgeSchemaError: If schema validation fails
    """
    required_keys = ["name", "fields", "primary_key"]

    try:
        for key in required_keys:
            if key not in schema_def:
                raise KeyError(f"Missing required key: {key}")

        if not isinstance(schema_def["fields"], dict):
            raise TypeError("'fields' must be a dictionary")

        if not schema_def["fields"]:
            raise ValueError("Schema must have at least one field")

        return True

    except (KeyError, TypeError, ValueError) as e:
        error = wrap_exception(
            e,
            SplurgeSchemaError,
            error_code="schema-validation-error",
        )
        error.attach_context(key="schema_name", value=schema_def.get("name", "unknown"))
        error.add_suggestion("Verify schema definition includes required keys")
        error.add_suggestion("Check field definitions are properly formatted")
        raise error from e


# ============================================================================
# Section 6: Encoding Operations with Custom Exceptions
# ============================================================================


@handle_exceptions(
    exceptions={
        UnicodeDecodeError: (SplurgeUnicodeDecodeError, "unicode-decode-error"),
        LookupError: (SplurgeUnicodeDecodeError, "encoding-not-supported"),
    },
    log_level="error",
)
def decode_bytes_to_string(data: bytes, encoding: str = "utf-8") -> str:
    """Decode bytes to string with error handling.

    Args:
        data: Bytes to decode
        encoding: Character encoding to use

    Returns:
        Decoded string

    Raises:
        SplurgeUnicodeDecodeError: If decoding fails
    """
    try:
        return data.decode(encoding)
    except LookupError as e:
        raise LookupError(f"Unknown encoding: {encoding}") from e


def encode_string_to_bytes(data: str, encoding: str = "utf-8") -> bytes:
    """Encode string to bytes with error handling.

    Args:
        data: String to encode
        encoding: Character encoding to use

    Returns:
        Encoded bytes

    Raises:
        SplurgeUnicodeEncodeError: If encoding fails
    """
    try:
        return data.encode(encoding)
    except UnicodeEncodeError as e:
        error = wrap_exception(
            e,
            SplurgeUnicodeEncodeError,
            error_code="unicode-encode-error",
        )
        error.attach_context(key="encoding", value=encoding)
        error.attach_context(key="problem_position", value=e.start)
        error.add_suggestion(f"Character cannot be represented in {encoding}")
        error.add_suggestion("Try using utf-8 encoding instead")
        raise error from e


# ============================================================================
# Section 7: Data Format Operations with Custom Exceptions
# ============================================================================


def parse_dsv_content(content: str, delimiter: str = ",") -> list[list[str]]:
    """Parse DSV (Delimited Separated Values) content.

    Args:
        content: DSV content string
        delimiter: Field delimiter character

    Returns:
        List of rows, each row is a list of fields

    Raises:
        SplurgeDsvFormatError: If parsing fails
    """
    lines = content.strip().split("\n")
    if not lines:
        raise ValueError("Empty DSV content")

    # Parse first row to determine field count
    first_row = lines[0].split(delimiter)
    expected_fields = len(first_row)
    rows: list[list[str]] = [first_row]

    try:
        for row_num, line in enumerate(lines[1:], start=2):
            fields = line.split(delimiter)

            if len(fields) != expected_fields:
                raise ValueError(f"Row {row_num}: expected {expected_fields} fields, got {len(fields)}")

            rows.append(fields)

        return rows

    except ValueError as e:
        error = wrap_exception(
            e,
            SplurgeDsvFormatError,
            error_code="dsv-format-error",
        )
        error.attach_context(key="delimiter", value=repr(delimiter))
        error.attach_context(key="expected_fields", value=expected_fields)
        error.add_suggestion("Verify the delimiter is correct")
        error.add_suggestion("Check for proper quoting of fields with delimiters")
        raise error from e


def parse_data_schema(schema_definition: str) -> dict[str, Any]:
    """Parse data schema from definition string.

    Args:
        schema_definition: Schema definition string (JSON format)

    Returns:
        Parsed schema dictionary

    Raises:
        SplurgeSchemaParseError: If schema parsing fails
    """
    import json

    try:
        schema = json.loads(schema_definition)

        # Validate schema structure
        if "fields" not in schema:
            raise KeyError("Schema missing 'fields' definition")

        # Validate field definitions
        for field_name, field_def in schema["fields"].items():
            if "type" not in field_def:
                raise ValueError(f"Field '{field_name}' missing 'type' definition")

        return schema  # type: ignore[no-any-return]

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        error = wrap_exception(
            e,
            SplurgeSchemaParseError,
            error_code="schema-parse-error",
        )
        error.add_suggestion("Ensure schema is valid JSON")
        error.add_suggestion("Check all fields have required properties")
        raise error from e


# ============================================================================
# Section 8: Integrated Workflow Example
# ============================================================================


def process_data_pipeline(
    raw_data: bytes,
    schema_json: str,
    database_query: str,
) -> dict[str, Any]:
    """Process a complete data pipeline with multiple operations.

    This demonstrates using custom Splurge exceptions across database,
    encoding, and data format operations.

    Args:
        raw_data: Raw bytes data to process
        schema_json: Schema definition as JSON string
        database_query: Database query to validate

    Returns:
        Processing results

    Raises:
        Various SplurgeError subclasses for different operations
    """
    formatter = ErrorMessageFormatter()
    results = {}

    try:
        # Step 1: Decode incoming data
        print("Step 1: Decoding data...")
        decoded_data = decode_bytes_to_string(raw_data, encoding="utf-8")
        results["decoded_rows"] = len(decoded_data.split("\n"))
        print(f"[OK] Decoded {results['decoded_rows']} lines of data")

        # Step 2: Parse DSV format
        print("Step 2: Parsing DSV format...")
        rows = parse_dsv_content(decoded_data, delimiter=",")
        results["parsed_rows"] = len(rows)
        print(f"[OK] Parsed {results['parsed_rows']} rows")

        # Step 3: Validate schema
        print("Step 3: Validating schema...")
        schema = parse_data_schema(schema_json)
        results["schema_fields"] = len(schema["fields"])
        print(f"[OK] Schema validated with {results['schema_fields']} fields")

        # Step 4: Validate SQL query
        print("Step 4: Validating SQL query...")
        parsed_query = parse_sql_query(database_query)
        results["query_type"] = parsed_query["type"]
        print("[OK] SQL query validated")

        # Step 5: Execute query
        print("Step 5: Executing query...")
        query_results = execute_database_query(database_query)
        results["query_results"] = len(query_results)
        print(f"[OK] Query returned {results['query_results']} rows")

        # Step 6: Validate database schema
        print("Step 6: Validating database schema...")
        schema_def = {
            "name": "users",
            "fields": {field_name: {"type": "string"} for field_name in schema.get("fields", {})},
            "primary_key": "id",
        }
        is_valid = validate_database_schema(schema_def)
        results["schema_valid"] = is_valid
        print("[OK] Database schema is valid")

        return results

    except SplurgeError as e:
        print("\n" + "=" * 70)
        print("PIPELINE ERROR OCCURRED!")
        print("=" * 70)
        formatted = formatter.format_error(e)
        print(formatted)
        raise


# ============================================================================
# Main Example Execution
# ============================================================================


if __name__ == "__main__":
    print("=" * 70)
    print("SPLURGE FAMILY LIBRARY - API INTEGRATOR USAGE EXAMPLE")
    print("=" * 70)

    formatter = ErrorMessageFormatter()

    # Example 1: SQL Parsing
    print("\n### EXAMPLE 1: SQL Query Parsing ###\n")
    try:
        query = parse_sql_query("SELECT id, name FROM users WHERE status = 'active'")
        print("[OK] Query parsed successfully")
        print(f"  Type: {query['type']}")
    except SplurgeError as e:
        print(formatter.format_error(e))

    # Example 2: Unicode Decoding
    print("\n### EXAMPLE 2: Unicode Decoding ###\n")
    try:
        test_bytes = b"Hello, World!"
        decoded = decode_bytes_to_string(test_bytes)
        print(f"[OK] Decoded successfully: {decoded}")
    except SplurgeError as e:
        print(formatter.format_error(e))

    # Example 3: DSV Parsing
    print("\n### EXAMPLE 3: DSV Format Parsing ###\n")
    try:
        dsv_content = "name,email,age\nAlice,alice@example.com,30\nBob,bob@example.com,25"
        rows = parse_dsv_content(dsv_content)
        print(f"[OK] Parsed {len(rows)} rows successfully")
        for i, row in enumerate(rows):
            print(f"  Row {i}: {row}")
    except SplurgeError as e:
        print(formatter.format_error(e))

    # Example 4: Schema Parsing
    print("\n### EXAMPLE 4: Data Schema Parsing ###\n")
    try:
        schema_json = '{"fields": {"id": {"type": "int"}, "name": {"type": "str"}}}'
        schema = parse_data_schema(schema_json)
        print(f"[OK] Schema parsed with {len(schema['fields'])} fields")
    except SplurgeError as e:
        print(formatter.format_error(e))

    # Example 5: Database Schema Validation
    print("\n### EXAMPLE 5: Database Schema Validation ###\n")
    try:
        schema_def = {
            "name": "products",
            "fields": {"id": {"type": "int"}, "name": {"type": "str"}},
            "primary_key": "id",
        }
        is_valid = validate_database_schema(schema_def)
        print("[OK] Database schema is valid")
    except SplurgeError as e:
        print(formatter.format_error(e))

    # Example 6: Complete Pipeline
    print("\n### EXAMPLE 6: Complete Data Pipeline ###\n")
    try:
        raw_data = b"name,email,age\nAlice,alice@example.com,30\nBob,bob@example.com,25"
        schema_json = '{"fields": {"name": {"type": "str"}, "email": {"type": "str"}, "age": {"type": "int"}}}'
        database_query = "SELECT * FROM users WHERE age > 25"

        results = process_data_pipeline(
            raw_data=raw_data,
            schema_json=schema_json,
            database_query=database_query,
        )

        print("\n" + "=" * 70)
        print("PIPELINE RESULTS:")
        print("=" * 70)
        for key, value in results.items():
            print(f"  {key}: {value}")
        print("=" * 70)

    except SplurgeError as e:
        print(f"Pipeline failed: {e}")

    print("\n[OK] All examples completed!")
