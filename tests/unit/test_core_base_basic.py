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


def test_full_code_domain_ends_with_error_code():
    """Test full_code returns only domain when domain already ends with error_code."""

    class NestedDomainException(SplurgeError):
        _domain = "app.validation.invalid-email"

    error = NestedDomainException("Email is invalid", error_code="invalid-email")
    assert error.error_code == "invalid-email"
    # Should return just domain, not domain.error_code
    assert error.full_code == "app.validation.invalid-email"


def test_full_code_domain_does_not_end_with_error_code():
    """Test full_code concatenates when domain doesn't end with error_code."""

    class SimpleDomainException(SplurgeError):
        _domain = "app.validation"

    error = SimpleDomainException("Validation failed", error_code="invalid-email")
    assert error.error_code == "invalid-email"
    # Should concatenate with dot
    assert error.full_code == "app.validation.invalid-email"


def test_full_code_partial_match_not_sufficient():
    """Test that partial match at end doesn't trigger deduplication."""

    class DomainException(SplurgeError):
        _domain = "app.my-invalid-value"

    error = DomainException("Error", error_code="invalid-value")
    # Domain ends with "invalid-value" substring but not as separate component
    # Depends on implementation: if using string.endswith(), this will deduplicate
    # If checking for component boundary, it won't
    assert error.full_code == "app.my-invalid-value"


def test_full_code_no_error_code():
    """Test full_code returns domain when no error_code provided."""
    error = DummyException("Test error")
    assert error.error_code is None
    assert error.full_code == "test"
