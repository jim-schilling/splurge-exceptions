"""Unit tests for core exception types."""

from splurge_exceptions import (
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValueError,
)


def test_splurge_value_error():
    """Test SplurgeValueError."""
    error = SplurgeValueError("Invalid value", error_code="invalid")
    assert error.message == "Invalid value"
    assert error.error_code == "invalid"
    assert error.domain == "splurge.value"


def test_splurge_os_error():
    """Test SplurgeOSError."""
    error = SplurgeOSError("File error", error_code="file-not-found")
    assert error.message == "File error"
    assert error.error_code == "file-not-found"
    assert error.domain == "splurge.os"


def test_splurge_runtime_error():
    """Test SplurgeRuntimeError."""
    error = SplurgeRuntimeError("Runtime error", error_code="execution-failed")
    assert error.message == "Runtime error"
    assert error.error_code == "execution-failed"
    assert error.domain == "splurge.runtime"
