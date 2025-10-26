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

import json
import re
from typing import Any

from splurge_exceptions import (
    ErrorMessageFormatter,
    SplurgeError,
    SplurgeFrameworkError,
    SplurgeOSError,
)

# ============================================================================
# Custom Domain Exceptions for Database Library
# ============================================================================


class SplurgeDatabaseError(SplurgeFrameworkError):
    """Base exception for database-related errors.

    Used by splurge-db library for all database operation failures.
    This is a custom exception that extends SplurgeError to participate
    in the splurge-exceptions framework.
    """

    _domain = "database"


class SplurgeSqlError(SplurgeDatabaseError):
    """Exception for SQL-related errors.

    Raised when SQL query parsing, validation, or syntax analysis fails.
    """

    _domain = "database.sql"


class SplurgeQueryError(SplurgeSqlError):
    """Exception for query execution errors.

    Raised when query execution fails due to database constraints,
    timeouts, or runtime conditions.
    """

    _domain = "database.sql.query"


class SplurgeConnectionError(SplurgeDatabaseError):
    """Exception for database connection errors.

    Raised when database connection establishment, authentication,
    or configuration fails.
    """

    _domain = "database.connection"


class SplurgeTransactionError(SplurgeDatabaseError):
    """Exception for transaction-related errors.

    Raised when transaction management, rollback, or commit operations fail.
    """

    _domain = "database.transaction"


class SplurgeMigrationError(SplurgeDatabaseError):
    """Exception for database migration errors.

    Raised when database schema migrations, version conflicts,
    or migration execution fails.
    """

    _domain = "database.migration"


# ============================================================================
# Custom Domain Exceptions for Data Processing Library
# ============================================================================


class SplurgeDataError(SplurgeFrameworkError):
    """Base exception for data processing errors.

    Used by splurge-data library for all data manipulation failures.
    """

    _domain = "data"


class SplurgeEncodingError(SplurgeDataError):
    """Exception for data encoding/decoding errors.

    Raised when data encoding, decoding, or format conversion fails.
    """

    _domain = "data.encoding"


class SplurgeValidationError(SplurgeDataError):
    """Exception for data validation errors.

    Raised when data validation rules, constraints, or format checks fail.
    """

    _domain = "data.validation"


class SplurgeFormatError(SplurgeDataError):
    """Exception for data format parsing errors.

    Raised when parsing structured data formats (JSON, CSV, XML) fails.
    """

    _domain = "data.format"


# ============================================================================
# Database Client Library Implementation
# ============================================================================


class DatabaseClient:
    """A database client library that uses splurge-exceptions for comprehensive error handling."""

    def __init__(self, connection_string: str):
        """Initialize database client.

        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        self.connection = None
        self.formatter = ErrorMessageFormatter()

    def connect(self) -> None:
        """Establish database connection with comprehensive error handling."""
        try:
            # Simulate connection logic
            if "invalid" in self.connection_string.lower():
                raise ValueError("Invalid connection string format")

            if "timeout" in self.connection_string.lower():
                raise TimeoutError("Connection timeout")

            if "refused" in self.connection_string.lower():
                raise ConnectionError("Connection refused")

            # Simulate successful connection
            self.connection = {"status": "connected"}
            print("Database connected successfully")
        except (ConnectionError, TimeoutError, ValueError) as e:
            error: SplurgeError
            if isinstance(e, ConnectionError):
                error = SplurgeConnectionError(
                    str(e),
                    error_code="connection-refused",
                )
            elif isinstance(e, TimeoutError):
                error = SplurgeConnectionError(
                    str(e),
                    error_code="connection-timeout",
                )
            else:  # ValueError
                error = SplurgeSqlError(
                    str(e),
                    error_code="invalid-connection-string",
                )
            raise error from e

    def execute_query(self, query: str, parameters: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute SQL query with error handling and context.

        Args:
            query: SQL query string
            parameters: Query parameters

        Returns:
            Query results
        """
        try:
            if not self.connection:
                raise SplurgeConnectionError("No active database connection", error_code="not-connected")

            # SQL validation - raise domain-specific exceptions directly
            if not query.strip():
                raise SplurgeSqlError("Query cannot be empty", error_code="empty-query")

            # Check for dangerous operations
            dangerous_patterns = [
                r"\bDROP\s+TABLE\b",
                r"\bDELETE\s+FROM\s+\w+\s*$",
                r"\bTRUNCATE\b",
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    raise SplurgeSqlError(
                        "Dangerous SQL operation detected",
                        error_code="dangerous-operation",
                        details={"pattern": pattern, "query": query},
                    )

            # Simulate query execution
            if "INVALID" in query.upper():
                raise ValueError("Invalid SQL syntax")

            if "TIMEOUT" in query.upper():
                raise RuntimeError("Query execution timeout")

            # Return mock results
            return [{"id": 1, "name": "Sample", "value": 42}]
        except (ValueError, RuntimeError) as e:
            error: SplurgeError
            if isinstance(e, ValueError):
                error = SplurgeSqlError(
                    str(e),
                    error_code="execution-syntax-error",
                )
            else:  # RuntimeError
                error = SplurgeQueryError(
                    str(e),
                    error_code="execution-failed",
                )
            raise error from e

    def batch_execute(self, queries: list[str]) -> list[list[dict[str, Any]]]:
        """Execute multiple queries in a transaction.

        Args:
            queries: List of SQL queries

        Returns:
            List of query results
        """
        if not self.connection:
            raise SplurgeConnectionError("No active database connection", error_code="not-connected")

        results = []

        def handle_query_success():
            print("  + Query executed successfully")

        def handle_query_error(exc):
            print(f"  - Query failed: {self.formatter.format_error(exc, include_context=True)}")

        for i, query in enumerate(queries):
            try:
                result = self.execute_query(query)
                results.append(result)
                handle_query_success()
            except (ValueError, RuntimeError) as e:
                error: SplurgeError
                if isinstance(e, ValueError):
                    error = SplurgeSqlError(
                        str(e),
                        error_code="invalid-syntax",
                    )
                else:  # RuntimeError
                    error = SplurgeQueryError(
                        str(e),
                        error_code="execution-failed",
                    )
                error.attach_context(
                    batch_index=i,
                    query=query[:50],
                )
                handle_query_error(error)
                raise error from e

        return results

    def disconnect(self) -> None:
        """Disconnect from database."""
        if self.connection:
            self.connection = None
            print("Database disconnected")


# ============================================================================
# Data Processing Library Implementation
# ============================================================================


class DataProcessor:
    """A data processing library that uses splurge-exceptions for comprehensive error handling."""

    def __init__(self, encoding: str = "utf-8"):
        """Initialize data processor.

        Args:
            encoding: Default text encoding
        """
        self.encoding = encoding
        self.formatter = ErrorMessageFormatter()

    def validate_json_schema(self, data: dict[str, Any], schema: dict[str, Any]) -> bool:
        """Validate JSON data against a schema.

        Args:
            data: JSON data to validate
            schema: Validation schema

        Returns:
            True if valid, raises exception if invalid
        """
        # Check required fields
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in data:
                raise SplurgeValidationError(
                    f"Required field '{field}' is missing",
                    error_code="missing-required-field",
                    details={"field": field, "schema": schema},
                )

        # Check field types
        properties = schema.get("properties", {})
        for field, value in data.items():
            if field in properties:
                expected_type = properties[field].get("type")
                if expected_type and not isinstance(value, self._get_type_class(expected_type)):
                    raise SplurgeValidationError(
                        f"Field '{field}' should be of type '{expected_type}'",
                        error_code="type-mismatch",
                        details={"field": field, "expected": expected_type, "actual": type(value).__name__},
                    )

        return True

    def _get_type_class(self, type_name: str):
        """Get Python type class from type name."""
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        return type_map.get(type_name, object)

    def load_json_file(self, file_path: str) -> dict[str, Any]:
        """Load and validate JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            Parsed JSON data
        """
        try:
            with open(file_path, encoding=self.encoding) as f:
                content = f.read()

                # Parse JSON
                try:
                    data = json.loads(content)
                except json.JSONDecodeError as e:
                    error = SplurgeFormatError(
                        str(e),
                        error_code="json-parse-error",
                    )
                    raise error from e
                except UnicodeDecodeError as e:
                    error = SplurgeEncodingError(
                        str(e),
                        error_code="encoding-error",
                    )
                    raise error from e
                except ValueError as e:
                    error = SplurgeValidationError(
                        str(e),
                        error_code="validation-error",
                    )
                    raise error from e

                # Validate structure
                if not isinstance(data, dict):
                    raise SplurgeValidationError(
                        "JSON root must be an object",
                        error_code="invalid-json-structure",
                        details={"actual_type": type(data).__name__},
                    )

                return data

        except FileNotFoundError as e:
            error = SplurgeOSError(f"File not found: {file_path}", error_code="file-not-found")
            error.attach_context({"file_path": file_path})
            raise error from e

    def process_csv_data(self, csv_content: str, delimiter: str = ",") -> list[dict[str, Any]]:
        """Process CSV data with comprehensive error handling.

        Args:
            csv_content: CSV content as string
            delimiter: CSV field delimiter

        Returns:
            Processed data as list of dictionaries
        """
        lines = csv_content.strip().split("\n")
        if not lines:
            raise SplurgeFormatError("CSV content cannot be empty", error_code="empty-csv")

        # Parse header
        try:
            header = [field.strip() for field in lines[0].split(delimiter)]
        except Exception as e:
            error = SplurgeFormatError(
                f"Failed to parse CSV header with delimiter '{delimiter}'",
                error_code="invalid-csv-header"
            )
            error.attach_context({"delimiter": delimiter})
            raise error from e

        results = []

        def handle_row_error(exc):
            print(f"  ✗ Row parsing failed: {self.formatter.format_error(exc)}")

        for i, line in enumerate(lines[1:], 1):
            if not line.strip():
                continue  # Skip empty lines

            try:
                values = [field.strip() for field in line.split(delimiter)]

                if len(values) != len(header):
                    raise SplurgeFormatError(
                        f"Row has {len(values)} fields, expected {len(header)}",
                        error_code="field-count-mismatch",
                        details={"row": i, "expected": len(header), "actual": len(values)},
                    )

                row_data = dict(zip(header, values, strict=False))
                results.append(row_data)

            except (ValueError, IndexError) as e:
                error: SplurgeError
                if isinstance(e, ValueError):
                    error = SplurgeFormatError(
                        str(e),
                        error_code="invalid-csv-row",
                    )
                else:  # IndexError
                    error = SplurgeFormatError(
                        str(e),
                        error_code="csv-field-mismatch",
                    )
                error.attach_context(row_number=i, line=line[:50])
                handle_row_error(error)
                # Continue processing other rows (skip this one)
                continue

        return results


# ============================================================================
# Library Integration Examples
# ============================================================================


def demonstrate_database_library_integration():
    """Demonstrate how the database library integrates with splurge-exceptions."""
    print("=== Database Library Integration ===")

    client = DatabaseClient("postgresql://user:pass@localhost/mydb")

    # Demonstrate various error scenarios
    error_scenarios = [
        ("Invalid connection", "invalid://connection", SplurgeSqlError),
        ("Connection timeout", "timeout://connection", SplurgeConnectionError),
        ("Connection refused", "refused://connection", SplurgeConnectionError),
    ]

    for description, connection_string, expected_error in error_scenarios:
        print(f"\n{description}:")

        try:
            # Test connection with manual error handling
            if "invalid" in connection_string.lower():
                raise ValueError("Invalid connection string format")
            elif "timeout" in connection_string.lower():
                raise TimeoutError("Connection timeout")
            elif "refused" in connection_string.lower():
                raise ConnectionError("Connection refused")
            else:
                client.connection = {"status": "connected"}
                print("  + Connected successfully")

        except expected_error as e:
            if hasattr(e, "error_code"):
                formatted = client.formatter.format_error(e, include_context=True, include_suggestions=True)
                print(f"  + Caught expected error:\n{formatted}")
            else:
                print(f"  + Caught expected error: {e}")
        except Exception as e:
            print(f"  - Unexpected error: {e}")
        finally:
            client.disconnect()

    # Test query scenarios separately
    print("\nQuery execution scenarios:")
    client.connection = {"status": "connected"}

    query_scenarios = [
        ("Empty query", "", SplurgeSqlError),
        ("Invalid syntax", "SELECT INVALID FROM users", SplurgeSqlError),
        ("Query timeout", "SELECT TIMEOUT FROM users", SplurgeQueryError),
        ("Dangerous operation", "DROP TABLE users", SplurgeSqlError),
    ]

    for description, query, expected_error in query_scenarios:
        print(f"\n{description}:")

        try:
            result = client.execute_query(query)
            print(f"  + Query executed successfully: {len(result)} rows")
        except expected_error as e:
            formatted = client.formatter.format_error(e, include_context=True, include_suggestions=True)
            print(f"  + Caught expected error:\n{formatted}")
        except Exception as e:
            print(f"  - Unexpected error: {e}")

    client.disconnect()


def demonstrate_data_processing_integration():
    """Demonstrate how the data processing library integrates with splurge-exceptions."""
    print("\n=== Data Processing Library Integration ===")

    processor = DataProcessor()

    # Test JSON validation
    print("\nJSON Schema Validation:")

    schema = {
        "type": "object",
        "required": ["name", "email"],
        "properties": {"name": {"type": "string"}, "email": {"type": "string"}, "age": {"type": "integer"}},
    }

    test_data = [
        {"name": "John", "email": "john@example.com"},  # Valid
        {"name": "Jane"},  # Missing email
        {"name": "Bob", "email": "bob@example.com", "age": "not-a-number"},  # Wrong type
    ]

    for i, data in enumerate(test_data):
        print(f"\nTest case {i + 1}: {data}")
        try:
            processor.validate_json_schema(data, schema)
            print("  + Validation passed")
        except SplurgeValidationError as e:
            formatted = processor.formatter.format_error(e, include_context=True)
            print(f"  - Validation failed:\n{formatted}")

    # Test CSV processing
    print("\nCSV Processing:")

    csv_data = """name,email,age
John Doe,john@example.com,25
Jane Smith,jane@example.com,thirty
Bob Johnson,bob@example.com,35
Missing Fields,missing@example.com"""

    try:
        results = processor.process_csv_data(csv_data)
        print(f"  + Successfully processed {len(results)} valid rows")
        for row in results:
            print(f"    - {row}")
    except Exception as e:
        print(f"  - CSV processing failed: {e}")


def demonstrate_batch_operations():
    """Demonstrate batch operations with error aggregation."""
    print("\n=== Batch Operations with Error Aggregation ===")

    client = DatabaseClient("postgresql://user:pass@localhost/mydb")
    client.connect()

    # Mix of valid and invalid queries
    queries = [
        "SELECT * FROM users LIMIT 10",  # Valid
        "SELECT INVALID FROM users",  # Invalid syntax
        "SELECT * FROM products LIMIT 5",  # Valid
        "SELECT TIMEOUT FROM orders",  # Timeout
        "SELECT * FROM categories",  # Valid
    ]

    print("Executing batch queries:")
    try:
        results = client.batch_execute(queries)
        print(f"  + Batch completed with {len(results)} results")
    except Exception as e:
        print(f"  - Batch failed: {e}")
    finally:
        client.disconnect()


def demonstrate_error_context_and_suggestions():
    """Demonstrate error context and recovery suggestions."""
    print("\n=== Error Context and Recovery Suggestions ===")

    client = DatabaseClient("postgresql://user:pass@localhost/mydb")

    # Manually create an error to demonstrate context and suggestions
    try:
        raise (
            SplurgeSqlError(
                message="Dangerous SQL operation detected",
                error_code="dangerous-operation",
                details={"operation": "DROP TABLE", "table": "users"},
            )
            .attach_context("user_id", "admin")
            .attach_context("timestamp", "2025-01-01 12:00:00")
            .add_suggestion("Use SELECT queries for data retrieval instead of DROP")
            .add_suggestion("Consider using TRUNCATE for removing all rows")
            .add_suggestion("Check permissions before attempting destructive operations")
        )

    except SplurgeSqlError as e:
        formatted = client.formatter.format_error(e, include_context=True, include_suggestions=True)
        print("Enhanced error with context and suggestions:")
        print(formatted)


if __name__ == "__main__":
    """Run all library integration demonstrations."""
    print("Splurge Exceptions - Library Integration Examples")
    print("=" * 60)

    demonstrate_database_library_integration()
    demonstrate_data_processing_integration()
    demonstrate_batch_operations()
    demonstrate_error_context_and_suggestions()

    print("\n" + "=" * 60)
    print("All library integration examples completed!")
    print("\nKey takeaways for library integrators:")
    print("- Extend SplurgeFrameworkError for domain-specific exceptions")
    print("- Use semantic error codes with hierarchical domains")
    print("- Leverage context managers and decorators for clean error handling")
    print("- Provide recovery suggestions for better user experience")
    print("- Maintain consistent error patterns across your library ecosystem")
