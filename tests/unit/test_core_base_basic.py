"""Unit tests for core base exception class.

DOMAINS: ["core", "base"]
"""

import pytest

from splurge_exceptions import SplurgeError


# Test exception for base class testing
class DummyException(SplurgeError):
    """Test exception class with _domain defined."""

    _domain = "test"


class TestSplurgeErrorInstantiation:
    """Test SplurgeError instantiation and properties."""

    def test_instantiation_with_error_code_and_message(self) -> None:
        """Test basic instantiation with error code and message."""
        error = DummyException(error_code="test-error", message="Test error")

        assert error.error_code == "test-error"
        assert error.message == "Test error"

    def test_instantiation_with_all_parameters(self) -> None:
        """Test instantiation with all parameters."""
        details = {"key": "value"}
        error = DummyException(
            error_code="test-error",
            message="Test error",
            details=details,
            severity="error",
        )

        assert error.error_code == "test-error"
        assert error.message == "Test error"
        assert error.details == details
        assert error.severity == "error"

    def test_instantiation_with_default_values(self) -> None:
        """Test instantiation with default values."""
        error = DummyException(error_code="test-error")

        assert error.error_code == "test-error"
        assert error.message is None
        assert error.details == {}
        assert error.severity == "error"

    def test_invalid_severity_raises_error(self) -> None:
        """Test that invalid severity raises ValueError."""
        with pytest.raises(ValueError, match="Invalid severity"):
            DummyException(error_code="test-error", severity="invalid")

    def test_severity_levels(self) -> None:
        """Test all valid severity levels."""
        for severity in ["info", "warning", "error", "critical"]:
            error = DummyException(error_code="test-error", severity=severity)
            assert error.severity == severity

    def test_missing_domain_raises_error(self) -> None:
        """Test that using SplurgeError without _domain raises TypeError."""
        with pytest.raises(TypeError, match="must define _domain"):
            SplurgeError(error_code="test-error")

    def test_invalid_error_code_format_raises_error(self) -> None:
        """Test that invalid error code format raises ValueError."""
        # Error codes must start with lowercase letter
        with pytest.raises(ValueError, match="Invalid error_code"):
            DummyException(error_code="Invalid-code")

    def test_error_code_with_hyphens(self) -> None:
        """Test that error codes can contain hyphens."""
        error = DummyException(error_code="invalid-value")
        assert error.error_code == "invalid-value"

    def test_error_code_with_numbers(self) -> None:
        """Test that error codes can contain numbers."""
        error = DummyException(error_code="error-42")
        assert error.error_code == "error-42"


class TestSplurgeErrorStringRepresentation:
    """Test string representations of SplurgeError."""

    def test_str_with_error_code_and_message(self) -> None:
        """Test __str__ with error code and message."""
        error = DummyException(error_code="test-error", message="Test error")
        assert str(error) == "[test.test-error] Test error"

    def test_str_with_only_message(self) -> None:
        """Test __str__ with only message."""
        error = DummyException(error_code="test-error", message="Test error")
        # With new system, error code is required
        assert "Test error" in str(error)

    def test_str_with_full_code(self) -> None:
        """Test __str__ includes full code."""
        error = DummyException(error_code="test-error")
        assert "test.test-error" in str(error)

    def test_get_full_message_without_details(self) -> None:
        """Test get_full_message without details."""
        error = DummyException(error_code="test-error", message="Test error")
        message = error.get_full_message()
        assert "test.test-error" in message
        assert "Test error" in message

    def test_get_full_message_with_details(self) -> None:
        """Test get_full_message with details."""
        error = DummyException(
            error_code="test-error",
            message="Test error",
            details={"key": "value"},
        )
        message = error.get_full_message()
        assert "test.test-error" in message
        assert "Test error" in message
        assert "key='value'" in message

    def test_repr(self) -> None:
        """Test __repr__ method."""
        error = DummyException(
            error_code="test-error",
            message="Test error",
            severity="error",
        )
        repr_str = repr(error)

        assert "DummyException" in repr_str
        assert "error_code='test-error'" in repr_str
        assert "message='Test error'" in repr_str

    def test_full_code_property(self) -> None:
        """Test full_code property."""
        error = DummyException(error_code="not-found")
        assert error.full_code == "test.not-found"

    def test_domain_property(self) -> None:
        """Test domain property."""
        error = DummyException(error_code="test-error")
        assert error.domain == "test"


class TestContextManagement:
    """Test context management methods."""

    def test_attach_context_with_key_value(self) -> None:
        """Test attaching context with key-value pair."""
        error = DummyException(error_code="test-error")
        result = error.attach_context(key="operation", value="file_read")

        assert result is error  # Method chaining
        assert error.get_context("operation") == "file_read"

    def test_attach_context_with_dict(self) -> None:
        """Test attaching context with dictionary."""
        error = DummyException(error_code="test-error")
        context_data = {"op": "read", "file": "data.txt"}
        error.attach_context(context_dict=context_data)

        assert error.get_context("op") == "read"
        assert error.get_context("file") == "data.txt"

    def test_attach_context_multiple_times(self) -> None:
        """Test attaching context multiple times."""
        error = DummyException(error_code="test-error")
        error.attach_context(key="key1", value="value1")
        error.attach_context(key="key2", value="value2")

        assert error.get_context("key1") == "value1"
        assert error.get_context("key2") == "value2"

    def test_get_context_nonexistent_key(self) -> None:
        """Test getting context for nonexistent key."""
        error = DummyException(error_code="test-error")
        assert error.get_context("nonexistent") is None

    def test_get_context_with_default(self) -> None:
        """Test getting context with default value."""
        error = DummyException(error_code="test-error")
        result = error.get_context("nonexistent", default="default_value")
        assert result == "default_value"

    def test_get_all_context(self) -> None:
        """Test getting all context as dict."""
        error = DummyException(error_code="test-error")
        error.attach_context(key="key1", value="value1")
        error.attach_context(key="key2", value="value2")

        all_context = error.get_all_context()
        assert all_context == {"key1": "value1", "key2": "value2"}

    def test_has_context(self) -> None:
        """Test checking if context key exists."""
        error = DummyException(error_code="test-error")
        error.attach_context(key="key1", value="value1")

        assert error.has_context("key1") is True
        assert error.has_context("nonexistent") is False

    def test_clear_context(self) -> None:
        """Test clearing all context."""
        error = DummyException(error_code="test-error")
        error.attach_context(key="key1", value="value1")
        error.attach_context(key="key2", value="value2")

        result = error.clear_context()
        assert result is error  # Method chaining
        assert error.get_all_context() == {}

    def test_context_isolation_between_instances(self) -> None:
        """Test that context is isolated between different exception instances."""
        error1 = DummyException(error_code="test-error")
        error2 = DummyException(error_code="test-error")

        error1.attach_context(key="key1", value="value1")

        assert error1.get_context("key1") == "value1"
        assert error2.get_context("key1") is None

    def test_attach_context_requires_key_or_dict(self) -> None:
        """Test that attach_context requires either key or dict."""
        error = DummyException(error_code="test-error")

        with pytest.raises(ValueError, match="Either 'key' or 'context_dict' must be provided"):
            error.attach_context()


class TestSuggestionManagement:
    """Test suggestion management methods."""

    def test_add_single_suggestion(self) -> None:
        """Test adding a single suggestion."""
        error = DummyException(error_code="test-error")
        result = error.add_suggestion("Check file permissions")

        assert result is error  # Method chaining
        assert error.get_suggestions() == ["Check file permissions"]

    def test_add_multiple_suggestions(self) -> None:
        """Test adding multiple suggestions."""
        error = DummyException(error_code="test-error")
        error.add_suggestion("Check file path")
        error.add_suggestion("Verify file exists")

        suggestions = error.get_suggestions()
        assert len(suggestions) == 2
        assert "Check file path" in suggestions
        assert "Verify file exists" in suggestions

    def test_get_suggestions_returns_copy(self) -> None:
        """Test that get_suggestions returns a copy."""
        error = DummyException(error_code="test-error")
        error.add_suggestion("Suggestion 1")

        suggestions = error.get_suggestions()
        suggestions.append("Suggestion 2")

        # Original should only have one suggestion
        assert len(error.get_suggestions()) == 1

    def test_has_suggestions(self) -> None:
        """Test has_suggestions method."""
        error = DummyException(error_code="test-error")
        assert error.has_suggestions() is False

        error.add_suggestion("Suggestion")
        assert error.has_suggestions() is True

    def test_suggestions_maintain_order(self) -> None:
        """Test that suggestions maintain insertion order."""
        error = DummyException(error_code="test-error")
        error.add_suggestion("First")
        error.add_suggestion("Second")
        error.add_suggestion("Third")

        assert error.get_suggestions() == ["First", "Second", "Third"]


class DummyExceptionChaining:
    """Test exception chaining functionality."""

    def test_exception_chaining_with_from(self) -> None:
        """Test exception chaining with 'from'."""
        original = FileNotFoundError("File not found")

        try:
            raise DummyException(error_code="test-error") from original
        except DummyException as e:
            assert e.__cause__ is original

    def test_is_subclass_of_exception(self) -> None:
        """Test that SplurgeError is a subclass of Exception."""
        assert issubclass(SplurgeError, Exception)

    def test_can_be_caught_as_exception(self) -> None:
        """Test that SplurgeError can be caught as Exception."""
        try:
            raise DummyException(error_code="test-error", message="Test")
        except Exception as e:
            assert isinstance(e, DummyException)


class TestMethodChaining:
    """Test method chaining capabilities."""

    def test_context_and_suggestion_chaining(self) -> None:
        """Test chaining context and suggestion methods."""
        error = (
            DummyException(error_code="test-error", message="Test")
            .attach_context(key="op", value="read")
            .add_suggestion("Check permissions")
            .attach_context(key="file", value="data.txt")
            .add_suggestion("Verify path")
        )

        assert error.get_context("op") == "read"
        assert error.get_context("file") == "data.txt"
        assert len(error.get_suggestions()) == 2


class TestDetailsProperty:
    """Test details property."""

    def test_details_returns_copy(self) -> None:
        """Test that details property returns a copy."""
        original_details = {"key": "value"}
        error = DummyException(error_code="test-error", details=original_details)

        details = error.details
        details["new_key"] = "new_value"

        # Original should not be modified
        assert "new_key" not in error.details
