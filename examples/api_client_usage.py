"""API Client Usage Example for Splurge Exceptions Framework.

This example demonstrates how to use the splurge-exceptions framework
in a typical API client library for error handling, exception conversion,
and user-friendly error reporting.

Key Concepts:
- Using libraries that internally use splurge-exceptions
- Handling various error scenarios in client applications
- Proper error propagation and context attachment
- Using explicit try/except patterns for clean error handling
"""

from typing import Any

# Simulate a database client library that uses splurge-exceptions internally
from splurge_exceptions import (
    ErrorMessageFormatter,
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValueError,
)

# ============================================================================
# Simulated Database Client Library (uses splurge-exceptions internally)
# ============================================================================


class DatabaseConnection:
    """Simulated database client that uses splurge-exceptions internally."""

    def __init__(self, host: str, port: int, database: str):
        """Initialize database connection.

        Args:
            host: Database host
            port: Database port
            database: Database name
        """
        self.host = host
        self.port = port
        self.database = database
        self.connected = False

    def connect(self) -> None:
        """Connect to database."""
        # Simulate connection logic
        if not self.host:
            raise SplurgeValueError(error_code="invalid-host", message="Database host cannot be empty")

        if self.port < 1 or self.port > 65535:
            raise SplurgeValueError(error_code="invalid-port", message=f"Invalid port number: {self.port}")

        # Simulate connection failure
        if self.host == "invalid.example.com":
            raise SplurgeOSError(
                error_code="connection-failed",
                message="Failed to connect to database",
                details={"host": self.host, "port": self.port},
            )

        self.connected = True

    def execute_query(self, query: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a database query.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Query results as list of dictionaries
        """
        if not self.connected:
            raise SplurgeRuntimeError(error_code="not-connected", message="Database connection not established")

        if not query.strip():
            raise SplurgeValueError(error_code="empty-query", message="Query cannot be empty")

        # Simulate query execution with potential failures
        if "INVALID" in query.upper():
            raise SplurgeValueError(error_code="invalid-syntax", message="Invalid SQL syntax", details={"query": query})

        if "TIMEOUT" in query.upper():
            raise SplurgeRuntimeError(
                error_code="query-timeout",
                message="Query execution timed out",
                details={"timeout": "30s", "query": query},
            )

        # Simulate successful query execution
        return [{"id": 1, "name": "Sample Data", "value": 42}]

    def disconnect(self) -> None:
        """Disconnect from database."""
        self.connected = False


# ============================================================================
# Application Code (Client Usage)
# ============================================================================


class UserService:
    """Application service that uses the database client."""

    def __init__(self, db_host: str = "localhost", db_port: int = 5432):
        """Initialize user service.

        Args:
            db_host: Database host
            db_port: Database port
        """
        self.db = DatabaseConnection(db_host, db_port, "users")
        self.formatter = ErrorMessageFormatter()

    def get_user_by_id(self, user_id: int) -> dict[str, Any] | None:
        """Get user by ID with comprehensive error handling.

        Args:
            user_id: User ID to lookup

        Returns:
            User data or None if not found

        Raises:
            SplurgeRuntimeError: If database operations fail
            SplurgeValueError: If validation fails
        """
        try:
            # Connect to database
            self.db.connect()

            try:
                # Execute query
                query = "SELECT * FROM users WHERE id = %s"
                results = self.db.execute_query(query, [user_id])

                if not results:
                    return None

                return results[0]

            finally:
                # Always disconnect
                self.db.disconnect()

        except SplurgeOSError as e:
            # Convert connection errors
            error = SplurgeRuntimeError(
                error_code="database-connection-error",
                message=str(e.message or e.error_code),
            )
            raise error from e
        except SplurgeRuntimeError as e:
            # Re-raise runtime errors with context
            e.attach_context("operation", "get_user_by_id")
            e.attach_context("user_id", user_id)
            raise
        except SplurgeValueError as e:
            # Validation errors pass through
            e.attach_context("operation", "get_user_by_id")
            raise

    def batch_get_users(self, user_ids: list[int]) -> list[dict[str, Any]]:
        """Get multiple users by IDs with error handling.

        Args:
            user_ids: List of user IDs

        Returns:
            List of user data
        """
        results = []

        for user_id in user_ids:
            try:
                user_data = self.get_user_by_id(user_id)
                if user_data:
                    results.append(user_data)
                    print(f"  + Retrieved user {user_id}")
            except (SplurgeOSError, SplurgeRuntimeError, SplurgeValueError) as e:
                error_msg = self.formatter.format_error(e, include_context=True)
                print(f"  - Error retrieving user {user_id}:\n{error_msg}")
                # Continue with next user instead of failing
                continue

        print(f"Successfully retrieved {len(results)} users")
        return results

    def create_user_with_validation(self, user_data: dict[str, Any]) -> int:
        """Create user with comprehensive validation and error handling.

        Args:
            user_data: User data to create

        Returns:
            Created user ID

        Raises:
            SplurgeValueError: If validation fails
            SplurgeRuntimeError: If database operations fail
        """
        try:
            # Validate input
            if not isinstance(user_data, dict):
                raise SplurgeValueError(
                    error_code="invalid-input-type",
                    message="User data must be a dictionary",
                )

            required_fields = ["name", "email"]
            for field in required_fields:
                if field not in user_data:
                    raise SplurgeValueError(
                        error_code="missing-required-field",
                        message=f"Required field '{field}' is missing",
                        details={"field": field, "provided_fields": list(user_data.keys())},
                    )

            # Validate email format
            email = user_data["email"]
            if "@" not in email:
                raise SplurgeValueError(
                    error_code="invalid-email-format",
                    message="Invalid email format",
                    details={"email": email},
                )

            # Simulate database operations
            self.db.connect()

            try:
                # Simulate user creation
                query = "INSERT INTO users (name, email) VALUES (%s, %s)"
                self.db.execute_query(query, [user_data["name"], email])

                # Return simulated user ID
                return 12345

            finally:
                self.db.disconnect()

        except (SplurgeOSError, SplurgeRuntimeError, SplurgeValueError) as e:
            # Attach context and re-raise
            e.attach_context("operation", "create_user")
            e.attach_context("user_email", user_data.get("email"))
            raise


# ============================================================================
# Example Usage Demonstrations
# ============================================================================


def demonstrate_basic_usage():
    """Demonstrate basic API client usage."""
    print("=== Basic API Client Usage ===")

    service = UserService()

    try:
        # Valid user lookup
        user = service.get_user_by_id(1)
        print(f"Found user: {user}")

    except SplurgeValueError as e:
        print(f"Validation error: {e}")
    except SplurgeRuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def demonstrate_batch_operations():
    """Demonstrate batch operations with error handling."""
    print("\n=== Batch Operations ===")

    service = UserService()

    # Mix of valid and invalid user IDs
    user_ids = [1, 2, 999, 3]

    try:
        users = service.batch_get_users(user_ids)
        print(f"Retrieved {len(users)} users successfully")
        for user in users:
            print(f"  - {user}")
    except Exception as e:
        print(f"Batch operation failed: {e}")


def demonstrate_validation_and_error_formatting():
    """Demonstrate validation and error formatting."""
    print("\n=== Validation and Error Formatting ===")

    service = UserService()
    formatter = ErrorMessageFormatter()

    # Test various validation scenarios
    test_cases = [
        {"name": "John", "email": "john@example.com"},  # Valid
        {"name": "Jane"},  # Missing email
        {"email": "invalid-email"},  # Invalid email format
        "not a dict",  # Invalid input type
    ]

    for i, user_data in enumerate(test_cases):
        print(f"\nTest case {i + 1}: {user_data}")

        try:
            user_id = service.create_user_with_validation(user_data)
            print(f"  + Created user with ID: {user_id}")
        except Exception as e:
            formatted_error = formatter.format_error(e, include_context=True, include_suggestions=True)
            print(f"  - Error:\n{formatted_error}")


def demonstrate_error_context_and_callbacks():
    """Demonstrate error handling with context attachment."""
    print("\n=== Error Handling with Context ===")

    service = UserService()

    try:
        user = service.get_user_by_id(1)
        if user:
            print(f"  ✓ Retrieved user: {user['name']}")
        else:
            print("  ✓ User operation completed successfully")
    except (SplurgeValueError, SplurgeRuntimeError, SplurgeOSError) as e:
        print(f"  ✗ User operation failed: {e.error_code}")
        formatted_error = service.formatter.format_error(e, include_context=True)
        print(f"\n{formatted_error}")


if __name__ == "__main__":
    """Run all demonstrations."""
    print("Splurge Exceptions - API Client Usage Examples")
    print("=" * 50)

    demonstrate_basic_usage()
    demonstrate_batch_operations()
    demonstrate_validation_and_error_formatting()
    demonstrate_error_context_and_callbacks()

    print("\n" + "=" * 50)
    print("All examples completed!")
