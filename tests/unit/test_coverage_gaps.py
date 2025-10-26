"""Tests for coverage gaps identified in v2025.1.0 refactoring.

These tests focus on covering edge cases, error paths, and special scenarios
that were previously untested but are now essential for 100% coverage.
"""

import subprocess
import sys

import pytest

from splurge_exceptions import SplurgeError, SplurgeSubclassError, SplurgeValueError
from splurge_exceptions.formatting.message import ErrorMessageFormatter


class TestModuleEntryPoint:
    """Tests for __main__.py module entry point."""

    def test_module_can_be_run_as_main(self):
        """Test that module can be executed as __main__."""
        # Use subprocess to actually run the module
        result = subprocess.run(
            [sys.executable, "-m", "splurge_exceptions", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "2025.1.0" in result.stdout

    def test_main_function_exit_code_propagated(self):
        """Test that main() exit codes are properly propagated in __main__."""
        # Test by running with invalid args (should return non-zero)
        result = subprocess.run(
            [sys.executable, "-m", "splurge_exceptions", "--invalid-arg"],
            capture_output=True,
            text=True,
        )
        # Invalid args should return error code
        assert result.returncode != 0


class TestDomainValidation:
    """Tests for domain validation in base.py."""

    def test_empty_domain_raises_error(self):
        """Test that empty domain raises SplurgeSubclassError."""

        class EmptyDomainError(SplurgeError):
            _domain = ""

        with pytest.raises(SplurgeSubclassError, match="cannot be empty"):
            EmptyDomainError("Error message")

    def test_domain_with_empty_components_raises_error(self):
        """Test that domain with empty dot-separated components raises error."""

        class BadDomainError(SplurgeError):
            _domain = "valid..invalid"

        with pytest.raises(SplurgeSubclassError, match="empty components"):
            BadDomainError("Error message")

    def test_domain_with_invalid_component_format_raises_error(self):
        """Test that domain with invalid component format raises error."""

        class InvalidComponentError(SplurgeError):
            _domain = "_invalid.component"

        with pytest.raises(SplurgeSubclassError, match="Invalid _domain"):
            InvalidComponentError("Error message")

    def test_domain_with_uppercase_raises_error(self):
        """Test that domain with uppercase letters raises error."""

        class UppercaseDomainError(SplurgeError):
            _domain = "Invalid.Component"

        with pytest.raises(SplurgeSubclassError):
            UppercaseDomainError("Error message")

    def test_domain_with_numbers_only_invalid(self):
        """Test that domain component with only numbers is invalid."""

        class OnlyNumbersError(SplurgeError):
            _domain = "123.456"

        with pytest.raises(SplurgeSubclassError):
            OnlyNumbersError("Error message")

    def test_domain_ending_with_dash_invalid(self):
        """Test that domain ending with dash is invalid."""

        class DashEndError(SplurgeError):
            _domain = "invalid-"

        with pytest.raises(SplurgeSubclassError):
            DashEndError("Error message")


class TestContextManagement:
    """Tests for context attachment and retrieval."""

    def test_attach_context_with_key_value(self):
        """Test attaching context with key-value pair."""
        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(key="user_id", value=123)

        assert error.get_context("user_id") == 123

    def test_attach_context_with_dict(self):
        """Test attaching context with dictionary."""
        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(context_dict={"operation": "read", "retry": 3})

        assert error.get_context("operation") == "read"
        assert error.get_context("retry") == 3

    def test_attach_context_without_key_or_dict_raises_error(self):
        """Test that attaching context without key or dict raises ValueError."""
        error = SplurgeValueError("Error", error_code="test")

        with pytest.raises(ValueError, match="Either 'key' or 'context_dict'"):
            error.attach_context()

    def test_get_context_with_default(self):
        """Test getting context with default value."""
        error = SplurgeValueError("Error", error_code="test")

        assert error.get_context("nonexistent", default="default_value") == "default_value"

    def test_get_all_context(self):
        """Test retrieving all context data."""
        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(key="a", value=1)
        error.attach_context(context_dict={"b": 2, "c": 3})

        all_context = error.get_all_context()
        assert all_context == {"a": 1, "b": 2, "c": 3}

    def test_has_context_returns_true_for_existing_key(self):
        """Test has_context returns True for existing keys."""
        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(key="exists", value="yes")

        assert error.has_context("exists") is True
        assert error.has_context("notexists") is False

    def test_clear_context(self):
        """Test clearing all context data."""
        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(context_dict={"a": 1, "b": 2})

        error.clear_context()
        assert error.get_all_context() == {}

    def test_context_method_chaining(self):
        """Test that context methods support chaining."""
        error = SplurgeValueError("Error", error_code="test")

        result = error.attach_context(key="a", value=1).attach_context(
            context_dict={"b": 2}
        ).clear_context()

        assert result is error
        assert error.get_all_context() == {}


class TestSuggestionManagement:
    """Tests for suggestion attachment and retrieval."""

    def test_add_suggestion(self):
        """Test adding a single suggestion."""
        error = SplurgeValueError("Error", error_code="test")
        error.add_suggestion("Check the input format")

        suggestions = error.get_suggestions()
        assert len(suggestions) == 1
        assert suggestions[0] == "Check the input format"

    def test_add_multiple_suggestions(self):
        """Test adding multiple suggestions."""
        error = SplurgeValueError("Error", error_code="test")
        error.add_suggestion("First suggestion")
        error.add_suggestion("Second suggestion")
        error.add_suggestion("Third suggestion")

        suggestions = error.get_suggestions()
        assert len(suggestions) == 3
        assert suggestions[0] == "First suggestion"
        assert suggestions[2] == "Third suggestion"

    def test_suggestion_method_chaining(self):
        """Test that suggestion methods support chaining."""
        error = SplurgeValueError("Error", error_code="test")

        result = error.add_suggestion("First").add_suggestion("Second")

        assert result is error
        assert len(error.get_suggestions()) == 2

    def test_has_suggestions(self):
        """Test checking if suggestions exist."""
        error = SplurgeValueError("Error", error_code="test")

        assert error.has_suggestions() is False

        error.add_suggestion("Suggestion 1")

        assert error.has_suggestions() is True


class TestGetFullMessage:
    """Tests for get_full_message method."""

    def test_get_full_message_with_all_components(self):
        """Test full message includes code, message, and details."""
        error = SplurgeValueError("Invalid input", error_code="bad-input")
        error._details = {"field": "email", "value": "invalid"}

        message = error.get_full_message()

        assert "[splurge.value.bad-input]" in message
        assert "Invalid input" in message
        assert "field=" in message

    def test_get_full_message_with_only_code(self):
        """Test full message with only error code."""
        error = SplurgeValueError("Error", error_code="code")
        error._message = None

        message = error.get_full_message()

        assert "[splurge.value.code]" in message

    def test_get_full_message_with_no_components(self):
        """Test full message with no message and no error_code still has domain."""
        error = SplurgeError.__new__(SplurgeError)
        error._domain = "test"
        error._error_code = None
        error._message = None
        error._details = {}

        message = error.get_full_message()

        # Even with no message and no error_code, domain is still included
        assert "[test]" in message

    def test_get_full_message_with_empty_details(self):
        """Test full message skips empty details."""
        error = SplurgeValueError("Message", error_code="code")
        error._details = {}

        message = error.get_full_message()

        assert "message" in message.lower()
        assert "(" not in message


class TestFormattingEdgeCases:
    """Tests for error formatting edge cases."""

    def test_formatter_handles_object_with_broken_str(self):
        """Test formatter handles objects with broken __str__."""

        class BrokenStr:
            def __str__(self):
                raise RuntimeError("Broken __str__")

            def __repr__(self):
                return "<BrokenStr>"

        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(key="broken", value=BrokenStr())

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_context=True)

        assert "broken" in result
        assert "<BrokenStr>" in result or "unrepresentable" in result

    def test_formatter_handles_object_with_broken_repr(self):
        """Test formatter handles objects with broken __repr__."""

        class BrokenRepr:
            def __str__(self):
                raise RuntimeError("Broken __str__")

            def __repr__(self):
                raise RuntimeError("Broken __repr__")

        error = SplurgeValueError("Error", error_code="test")
        error.attach_context(key="broken", value=BrokenRepr())

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_context=True)

        assert "unrepresentable" in result

    def test_format_context_with_empty_dict(self):
        """Test format_context with empty dictionary."""
        formatter = ErrorMessageFormatter()
        result = formatter.format_context({})

        assert result == ""

    def test_format_suggestions_with_empty_list(self):
        """Test format_suggestions with empty list."""
        formatter = ErrorMessageFormatter()
        result = formatter.format_suggestions([])

        assert result == ""


class TestPickleSupport:
    """Tests for exception pickle support."""

    def test_error_can_be_pickled_and_unpickled(self):
        """Test that exceptions can be pickled and unpickled."""
        import pickle

        error = SplurgeValueError("Test error", error_code="test-code")
        error.attach_context(key="user_id", value=123)
        error.add_suggestion("Fix it")

        pickled = pickle.dumps(error)
        unpickled = pickle.loads(pickled)

        # Verify basic properties are preserved
        assert unpickled.message == "Test error"
        assert unpickled.get_context("user_id") == 123
        assert unpickled.get_suggestions() == ["Fix it"]

    def test_setstate_with_none_state(self):
        """Test __setstate__ handles None state gracefully."""
        error = SplurgeValueError("Error", error_code="test")
        error.__setstate__(None)
        # Should not raise any errors

    def test_setstate_with_empty_state(self):
        """Test __setstate__ handles empty state gracefully."""
        error = SplurgeValueError("Error", error_code="test")
        error.__setstate__({})
        # Should not raise any errors

    def test_setstate_with_invalid_details_type(self):
        """Test __setstate__ handles invalid details type."""
        error = SplurgeValueError("Error", error_code="test")
        error.__setstate__({"details": "not a dict"})
        # Should use empty dict instead
        assert error.details == {}


class TestExceptionStringRepresentation:
    """Tests for exception string representations."""

    def test_str_representation(self):
        """Test string representation of exception."""
        error = SplurgeValueError("Something failed", error_code="fail")

        str_repr = str(error)

        assert "fail" in str_repr or "failed" in str_repr

    def test_repr_representation(self):
        """Test repr representation of exception."""
        error = SplurgeValueError("Error message", error_code="test")

        repr_str = repr(error)

        assert "SplurgeValueError" in repr_str
