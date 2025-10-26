"""Unit tests for core base exception class."""
import pytest

from splurge_exceptions import SplurgeError, SplurgeSubclassError


class DummyException(SplurgeError):
    """Test exception class."""
    _domain = "test"


def test_with_message_and_error_code():
    """Test with both message and error_code."""
    error = DummyException("Test error", error_code="test-code")
    assert error.message == "Test error"
    assert error.error_code == "test-code"
    assert error.full_code == "test.test-code"


def test_with_message_only():
    """Test with message only."""
    error = DummyException("Test error")
    assert error.message == "Test error"
    assert error.error_code is None
    assert error.full_code == "test"


def test_normalization_uppercase():
    """Test error code normalization."""
    error = DummyException("Test", error_code="Invalid-Code")
    assert error.error_code == "invalid-code"


def test_normalization_underscores():
    """Test underscore conversion."""
    error = DummyException("Test", error_code="invalid_code")
    assert error.error_code == "invalid-code"


def test_normalization_empty_becomes_none():
    """Test empty becomes None."""
    error = DummyException("Test", error_code="")
    assert error.error_code is None
    assert error.full_code == "test"


def test_missing_domain_raises():
    """Test missing domain."""
    with pytest.raises(SplurgeSubclassError):
        SplurgeError("msg")
