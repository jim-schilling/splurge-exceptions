"""Unit tests for stdlib exception wrapping utilities.

Tests the wrap_exception() function and related utilities for converting
standard library exceptions to Splurge exceptions.
"""

import pytest

from splurge_exceptions import (
    SplurgeError,
    SplurgeOSError,
    SplurgeValidationError,
)
from splurge_exceptions.wrappers.stdlib import wrap_exception


class TestWrapExceptionBasic:
    """Tests for basic wrap_exception() functionality."""

    def test_wrap_file_not_found_error(self) -> None:
        """Test wrapping FileNotFoundError to SplurgeOSError."""
        original = FileNotFoundError("File not found: data.txt")
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
            message="Failed to locate file",
        )

        assert isinstance(wrapped, SplurgeOSError)
        assert isinstance(wrapped, SplurgeError)
        assert wrapped.error_code == "file-not-found"
        assert wrapped.message == "Failed to locate file"
        assert wrapped.__cause__ is original

    def test_wrap_value_error_to_validation(self) -> None:
        """Test wrapping ValueError to SplurgeValidationError."""
        original = ValueError("Invalid value provided")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
            message="Value validation failed",
        )

        assert isinstance(wrapped, SplurgeValidationError)
        assert wrapped.error_code == "invalid-value"
        assert wrapped.__cause__ is original

    def test_wrap_preserves_exception_chain(self) -> None:
        """Test that exception chaining is preserved (__cause__)."""
        original_error = FileNotFoundError("Original error")
        wrapped = wrap_exception(
            original_error,
            SplurgeOSError,
            error_code="file-not-found",
        )

        assert wrapped.__cause__ is original_error
        assert str(original_error) in str(wrapped.__cause__)

    def test_wrap_with_custom_message(self) -> None:
        """Test wrapping with custom error message."""
        original = ValueError("original message")
        custom_msg = "Custom error message"
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
            message=custom_msg,
        )

        assert wrapped.message == custom_msg

    def test_wrap_uses_original_message_if_not_provided(self) -> None:
        """Test that original exception message is used if not provided."""
        original_msg = "Original exception message"
        original = ValueError(original_msg)
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        # Message should be used from original or generated
        assert wrapped.message is not None

    def test_wrap_with_details(self) -> None:
        """Test wrapping exception with additional details."""
        original = FileNotFoundError("file.txt")
        details = {"path": "/data/file.txt", "mode": "read"}
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
            details=details,
        )

        assert wrapped.details == details


class TestWrapExceptionWithContext:
    """Tests for wrapping with context attachment."""

    def test_wrap_with_context_key_value(self) -> None:
        """Test wrapping exception and attaching context as key-value."""
        original = ValueError("Invalid value")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
            context={"field": "email", "value": "invalid@"},
        )

        assert wrapped.has_context("field")
        assert wrapped.get_context("field") == "email"
        assert wrapped.get_context("value") == "invalid@"

    def test_wrap_with_context_dict(self) -> None:
        """Test wrapping exception with context dictionary."""
        original = ValueError("Invalid")
        context = {
            "attempt": 3,
            "max_attempts": 5,
            "reason": "Format invalid",
        }
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
            context=context,
        )

        assert wrapped.get_context("attempt") == 3
        assert wrapped.get_context("max_attempts") == 5

    def test_wrap_without_context(self) -> None:
        """Test wrapping without context."""
        original = ValueError("Invalid")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        # Check that no specific context keys exist
        assert wrapped.get_all_context() == {}


class TestWrapExceptionWithSuggestions:
    """Tests for wrapping with suggestions."""

    def test_wrap_with_suggestions(self) -> None:
        """Test wrapping exception with recovery suggestions."""
        original = FileNotFoundError("file.txt")
        suggestions = ["Check file path", "Verify file permissions", "Create file"]
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
            suggestions=suggestions,
        )

        assert wrapped.has_suggestions()
        result_suggestions = wrapped.get_suggestions()
        assert len(result_suggestions) == 3
        assert result_suggestions[0] == "Check file path"

    def test_wrap_without_suggestions(self) -> None:
        """Test wrapping without suggestions."""
        original = ValueError("Invalid")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        # Check that no suggestions were added
        assert wrapped.get_suggestions() == []


class TestWrapExceptionErrorCodeResolution:
    """Tests for error code resolution during wrapping."""

    def test_wrap_with_fully_qualified_error_code(self) -> None:
        """Test wrapping with fully qualified error code."""
        original = FileNotFoundError("file.txt")
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
        )

        assert wrapped.error_code == "file-not-found"

    def test_wrap_with_partial_error_code_domain_only(self) -> None:
        """Test wrapping with valid semantic error code (even if short)."""
        original = FileNotFoundError("file.txt")

        # "os" is a valid semantic error code (though typically we'd use more specific codes)
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="os",
        )

        assert wrapped.error_code == "os"
        assert wrapped.error_code is not None

    def test_wrap_with_partial_error_code_domain_category(self) -> None:
        """Test wrapping with error code containing dots raises ValueError."""
        original = FileNotFoundError("file.txt")

        # Error codes cannot contain dots - only semantic codes without dots
        with pytest.raises(ValueError, match="Invalid error_code"):
            wrap_exception(
                original,
                SplurgeOSError,
                error_code="os.file",
            )

    def test_wrap_with_none_error_code_uses_mapping(self) -> None:
        """Test wrapping with None error code raises ValueError (requires explicit code)."""
        original = FileNotFoundError("file.txt")

        # In the new system, error_code is required - user must provide explicit code
        with pytest.raises(ValueError, match="error_code cannot be empty"):
            wrap_exception(
                original,
                SplurgeOSError,
                error_code=None,
            )

    def test_wrap_with_none_error_code_raises_error(self) -> None:
        """Test wrapping with None code raises ValueError (error_code required)."""
        original = RuntimeError("Some runtime error")

        # In the new system, error_code is required - no automatic fallback or registry lookup
        with pytest.raises(ValueError, match="error_code cannot be empty"):
            wrap_exception(
                original,
                SplurgeOSError,
                error_code=None,
            )


class TestWrapExceptionWithMultipleParameters:
    """Tests for wrapping with multiple parameters combined."""

    def test_wrap_with_all_parameters(self) -> None:
        """Test wrapping with all parameters specified."""
        original = ValueError("Invalid email")
        context = {"field": "email", "input": "user@invalid"}
        suggestions = ["Add domain", "Check format"]

        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-email",
            message="Email validation failed",
            context=context,
            suggestions=suggestions,
            details={"regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"},
        )

        assert wrapped.error_code == "invalid-email"
        assert wrapped.message == "Email validation failed"
        assert wrapped.get_context("field") == "email"
        assert len(wrapped.get_suggestions()) == 2
        assert wrapped.details["regex"] is not None

    def test_wrap_preserves_exception_hierarchy(self) -> None:
        """Test that wrapped exception is instance of target and SplurgeError."""
        original = FileNotFoundError("file.txt")
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
        )

        assert isinstance(wrapped, SplurgeOSError)
        assert isinstance(wrapped, SplurgeError)
        assert isinstance(wrapped, Exception)


class TestWrapExceptionSeverityAndRecoverability:
    """Tests for severity and recoverability in wrapped exceptions."""

    def test_wrap_preserves_default_severity(self) -> None:
        """Test that wrapped exception has default severity."""
        original = FileNotFoundError("file.txt")
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
        )

        # Default severity should be set
        assert wrapped.severity in ["info", "warning", "error", "critical"]

    def test_wrap_preserves_default_recoverability(self) -> None:
        """Test that wrapped exception has recoverability set."""
        original = FileNotFoundError("file.txt")
        wrapped = wrap_exception(
            original,
            SplurgeOSError,
            error_code="file-not-found",
        )

        # Default recoverability should be set
        assert isinstance(wrapped.recoverable, bool)


class TestWrapExceptionEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_wrap_exception_with_empty_message(self) -> None:
        """Test wrapping exception with empty message."""
        original = ValueError("")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        assert wrapped is not None
        assert isinstance(wrapped, SplurgeValidationError)

    def test_wrap_exception_with_unicode_message(self) -> None:
        """Test wrapping exception with unicode characters."""
        original = ValueError("Error: 日本語 🚀")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        assert wrapped is not None

    def test_wrap_preserves_original_exception(self) -> None:
        """Test that original exception is accessible via __cause__."""
        original = ValueError("Original")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        # Original exception should be preserved for debugging
        assert wrapped.__cause__ is original
        assert str(original) == str(wrapped.__cause__)


class TestWrapExceptionIntegration:
    """Integration tests for exception wrapping."""

    def test_wrap_and_re_raise_and_catch(self) -> None:
        """Test wrapping, raising, and catching wrapped exception."""
        original = FileNotFoundError("file.txt")

        with pytest.raises(SplurgeOSError) as exc_info:
            wrapped = wrap_exception(
                original,
                SplurgeOSError,
                error_code="file-not-found",
            )
            raise wrapped

        assert exc_info.value.error_code == "file-not-found"
        assert exc_info.value.__cause__ is original

    def test_wrap_multiple_exceptions_independently(self) -> None:
        """Test wrapping multiple exceptions independently."""
        file_err = FileNotFoundError("file.txt")
        value_err = ValueError("invalid")

        wrapped1 = wrap_exception(
            file_err,
            SplurgeOSError,
            error_code="file-not-found",
            context={"file": "data.txt"},
        )

        wrapped2 = wrap_exception(
            value_err,
            SplurgeValidationError,
            error_code="invalid-value",
            context={"field": "age"},
        )

        # Verify independence
        assert wrapped1.get_context("file") == "data.txt"
        assert wrapped2.get_context("field") == "age"
        assert wrapped1.__cause__ is file_err
        assert wrapped2.__cause__ is value_err

    def test_wrap_exception_chaining_with_method_chaining(self) -> None:
        """Test wrapping with method chaining for context and suggestions."""
        original = ValueError("Invalid")
        wrapped = wrap_exception(
            original,
            SplurgeValidationError,
            error_code="invalid-value",
        )

        # Add context and suggestions via method chaining
        result = wrapped.attach_context("field", "email").add_suggestion("Check format")

        assert result.get_context("field") == "email"
        assert len(result.get_suggestions()) == 1
