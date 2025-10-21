"""API Client Usage Example for Splurge Exceptions Framework.

This example demonstrates how to use the splurge-exceptions framework
in a typical API client library for error handling, exception conversion,
and user-friendly error reporting.

Key Concepts:
- Wrapping stdlib exceptions to structured Splurge exceptions
- Using context managers for resource cleanup with error handling
- Using decorators for automatic exception conversion
- Formatting errors for user-friendly output
- Managing error codes and registries
"""

from typing import Any

from splurge_exceptions import (
    SplurgeAuthenticationError,
    SplurgeConfigurationError,
    SplurgeError,
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValidationError,
    error_context,
    handle_exceptions,
    wrap_exception,
)
from splurge_exceptions.formatting.message import ErrorMessageFormatter

# ============================================================================
# Section 1: Basic Exception Wrapping
# ============================================================================


def fetch_user_data(user_id: int) -> dict[str, Any]:
    """Fetch user data from API - demonstrates exception wrapping.

    This function shows how to catch stdlib exceptions and wrap them
    with meaningful Splurge exceptions.

    Args:
        user_id: The user ID to fetch

    Returns:
        User data dictionary

    Raises:
        SplurgeValidationError: If user_id is invalid
        SplurgeRuntimeError: If API call fails
    """
    if not isinstance(user_id, int) or user_id <= 0:
        try:
            raise ValueError(f"Invalid user_id: {user_id}. Must be positive integer.")
        except ValueError as e:
            # Wrap stdlib exception with context
            error = wrap_exception(
                e,
                SplurgeValidationError,
                error_code="invalid-value",
            )
            error.attach_context(key="provided_value", value=user_id)
            error.add_suggestion("Ensure user_id is a positive integer")
            raise error from e

    try:
        # Simulate API call
        response = {"id": user_id, "name": "John Doe", "email": "john@example.com"}
        if user_id == 999:  # Simulate error condition
            raise ConnectionError("Failed to connect to API")
        return response
    except ConnectionError as e:
        # Wrap connection errors with meaningful error code
        error = wrap_exception(
            e,
            SplurgeRuntimeError,
            error_code="connection-failed",
        )
        error.attach_context(key="endpoint", value="/api/users")
        error.attach_context(key="retry_count", value=3)
        error.add_suggestion("Check your network connection")
        error.add_suggestion("Verify the API endpoint is accessible")
        raise error from e


# ============================================================================
# Section 2: Context Manager for Resource Management
# ============================================================================


def process_file_with_error_handling(file_path: str) -> str:
    """Process a file with error handling using context manager.

    Demonstrates using error_context to handle multiple exception types
    with automatic conversion and context tracking.

    Args:
        file_path: Path to the file to process

    Returns:
        Processed content

    Raises:
        SplurgeOSError: If file operations fail
        SplurgeValidationError: If file validation fails
    """
    context_data = {"file_path": file_path, "operation": "read_and_process"}

    def on_success() -> None:
        """Called if no exception occurs."""
        print(f"Successfully processed {file_path}")

    def on_error(exc: Exception) -> None:
        """Called when an exception is caught."""
        print(f"Error during processing: {exc}")

    with error_context(
        exceptions={
            FileNotFoundError: (SplurgeOSError, "file-not-found"),
            PermissionError: (SplurgeOSError, "permission-denied"),
            ValueError: (SplurgeValidationError, "invalid-content"),
        },
        context=context_data,
        on_success=on_success,
        on_error=on_error,
        suppress=False,
    ):
        # File operations
        with open(file_path) as f:
            content = f.read()

        # Validation
        if not content.strip():
            raise ValueError("File content is empty")

        # Processing
        processed = content.upper()
        return processed


# ============================================================================
# Section 3: Decorator-Based Exception Conversion
# ============================================================================


@handle_exceptions(
    exceptions={
        ValueError: (SplurgeValidationError, "invalid-value"),
        KeyError: (SplurgeValidationError, "validation.json.002"),
        TypeError: (SplurgeRuntimeError, "runtime.type.001"),
    },
    log_level="warning",
)
def parse_json_config(json_data: str) -> dict[str, Any]:
    """Parse JSON configuration with automatic exception conversion.

    The decorator automatically converts any ValueError, KeyError, or TypeError
    to the corresponding Splurge exception with the specified error code.

    Args:
        json_data: JSON string to parse

    Returns:
        Parsed configuration dictionary

    Raises:
        SplurgeValidationError: If JSON parsing fails
        SplurgeRuntimeError: If type conversion fails
    """
    import json

    data: dict[str, Any] = json.loads(json_data)  # May raise ValueError

    # Type conversion (may raise TypeError)
    if "port" in data:
        data["port"] = int(data["port"])
    if "timeout" in data:
        data["timeout"] = float(data["timeout"])

    return data


# ============================================================================
# Section 4: Error Formatting and User-Friendly Output
# ============================================================================


def handle_api_call_with_formatting() -> None:
    """Demonstrate error formatting for user-friendly output."""
    formatter = ErrorMessageFormatter()

    try:
        _ = fetch_user_data(user_id=-1)
    except SplurgeValidationError as e:
        # Format error with context and suggestions
        formatted_message = formatter.format_error(
            e,
            include_context=True,
            include_suggestions=True,
        )
        print("=" * 70)
        print("USER-FRIENDLY ERROR MESSAGE:")
        print("=" * 70)
        print(formatted_message)
        print("=" * 70)


# ============================================================================
# Section 5: Chaining and Exception Context
# ============================================================================


def create_api_client_with_auth(api_key: str | None = None) -> dict[str, Any]:
    """Initialize API client with authentication.

    Demonstrates how to validate configuration and chain exceptions
    with meaningful context.

    Args:
        api_key: API key for authentication

    Returns:
        Client configuration

    Raises:
        SplurgeConfigurationError: If configuration is invalid
        SplurgeAuthenticationError: If API key is missing
    """
    if api_key is None:
        try:
            raise ValueError("API key is required")
        except ValueError as e:
            error = wrap_exception(
                e,
                SplurgeAuthenticationError,
                error_code="auth.api_key.001",
            )
            error.attach_context(key="config_source", value="environment")
            error.add_suggestion("Set SPLURGE_API_KEY environment variable")
            error.add_suggestion("Or pass api_key parameter to create_api_client_with_auth()")
            raise error from e

    if len(api_key) < 32:
        try:
            raise ValueError(f"API key too short: {len(api_key)} chars")
        except ValueError as e:
            error = wrap_exception(
                e,
                SplurgeConfigurationError,
                error_code="config.api_key.001",
            )
            error.attach_context(key="expected_length", value=32)
            error.attach_context(key="actual_length", value=len(api_key))
            raise error from e

    return {"api_key": api_key, "base_url": "https://api.example.com"}


# ============================================================================
# Section 6: Composite Exception Handling
# ============================================================================


def perform_api_workflow(user_id: int, file_path: str, api_key: str) -> None:
    """Perform a complete API workflow with comprehensive error handling.

    This demonstrates using multiple exception handling strategies together:
    - Decorator-based conversion (parse_json_config)
    - Context manager (process_file_with_error_handling)
    - Direct exception wrapping (create_api_client_with_auth, fetch_user_data)

    Args:
        user_id: User ID for the API call
        file_path: Path to configuration file
        api_key: API key for authentication
    """
    formatter = ErrorMessageFormatter()

    try:
        # Step 1: Initialize client
        print("Step 1: Initializing API client...")
        client = create_api_client_with_auth(api_key)
        print(f"[OK] Client initialized with key: {client['api_key'][:8]}...")

        # Step 2: Fetch user data
        print("\nStep 2: Fetching user data...")
        user_data = fetch_user_data(user_id)
        print(f"[OK] User data fetched: {user_data}")

        # Step 3: Process configuration file
        print("\nStep 3: Processing configuration file...")
        file_content = process_file_with_error_handling(file_path)
        print(f"[OK] File processed ({len(file_content)} chars)")

        # Step 4: Parse JSON configuration
        print("\nStep 4: Parsing JSON configuration...")
        config = parse_json_config(file_content)
        print(f"[OK] Configuration parsed with {len(config)} settings")

        print("\n" + "=" * 70)
        print("WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 70)

    except Exception as e:
        # Catch any Splurge exception and format it
        print("\n" + "=" * 70)
        print("WORKFLOW FAILED!")
        print("=" * 70)
        if isinstance(e, SplurgeError):
            formatted = formatter.format_error(e)
            print(formatted)
        else:
            print(f"Unexpected error: {e}")
        raise


# ============================================================================
# Main Example Execution
# ============================================================================


if __name__ == "__main__":
    print("=" * 70)
    print("SPLURGE EXCEPTIONS FRAMEWORK - API CLIENT USAGE EXAMPLE")
    print("=" * 70)

    # Example 1: Basic error formatting
    print("\n\n### EXAMPLE 1: Error Formatting ###\n")
    try:
        handle_api_call_with_formatting()
    except Exception as e:
        print(f"Exception caught: {e}")

    # Example 2: Configuration error
    print("\n\n### EXAMPLE 2: Configuration Error ###\n")
    try:
        client = create_api_client_with_auth(api_key=None)
    except SplurgeAuthenticationError as e:
        formatter = ErrorMessageFormatter()
        print(formatter.format_error(e))

    # Example 3: Complete workflow (with valid inputs for demo)
    print("\n\n### EXAMPLE 3: Complete Workflow ###\n")
    try:
        # Create a temporary config file for the example
        import os
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            tmp.write('{"host": "localhost", "port": "8080", "timeout": "30.0"}')
            tmp_path = tmp.name

        try:
            perform_api_workflow(
                user_id=123,
                file_path=tmp_path,
                api_key="a" * 32,
            )
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        print(f"Workflow error: {e}")

    print("\n[OK] All examples completed successfully!")
