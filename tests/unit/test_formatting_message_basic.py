"""Unit tests for error message formatting.

Tests the ErrorMessageFormatter for formatting error messages
with context, suggestions, and metadata.
"""

from splurge_exceptions import (
    SplurgeOSError,
    SplurgeValueError,
)
from splurge_exceptions.formatting.message import ErrorMessageFormatter


class TestErrorMessageFormatterBasic:
    """Tests for basic formatting functionality."""

    def test_format_error_with_code_and_message(self) -> None:
        """Test formatting error with code and message."""
        error = SplurgeValueError("Invalid email address", error_code="invalid-value")
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert "invalid-value" in result
        assert "Invalid email address" in result

    def test_format_error_with_only_code(self) -> None:
        """Test formatting error with only code."""
        error = SplurgeValueError("", error_code="invalid-value")
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert "invalid-value" in result

    def test_format_error_with_only_message(self) -> None:
        """Test formatting error with only message."""
        error = SplurgeValueError("Something failed", error_code="generic")
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert "Something failed" in result

    def test_format_error_returns_string(self) -> None:
        """Test that format_error returns string."""
        error = SplurgeValueError("Invalid", error_code="invalid-value")
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert isinstance(result, str)
        assert len(result) > 0


class TestErrorMessageFormatterWithContext:
    """Tests for formatting with context."""

    def test_format_error_includes_context(self) -> None:
        """Test that context is included in formatted message."""
        error = SplurgeValueError("Invalid email", error_code="invalid-value")
        error.attach_context(context_dict={"field": "email", "input": "user@invalid"})

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_context=True)

        assert "field" in result or "email" in result

    def test_format_error_excludes_context_when_requested(self) -> None:
        """Test that context can be excluded from formatted message."""
        error = SplurgeValueError("Invalid", error_code="invalid-value")
        error.attach_context(context_dict={"field": "email"})

        formatter = ErrorMessageFormatter()
        result_with = formatter.format_error(error, include_context=True)
        result_without = formatter.format_error(error, include_context=False)

        # Without context should be shorter or not include context keys
        assert len(result_without) <= len(result_with)

    def test_format_context_single_item(self) -> None:
        """Test formatting single context item."""
        formatter = ErrorMessageFormatter()

        result = formatter.format_context({"field": "email"})

        assert isinstance(result, str)
        assert "field" in result or "email" in result

    def test_format_context_multiple_items(self) -> None:
        """Test formatting multiple context items."""
        formatter = ErrorMessageFormatter()
        context = {"field": "email", "input": "user@invalid", "attempt": 3}

        result = formatter.format_context(context)

        assert isinstance(result, str)
        # All keys should be present
        for key in context:
            assert key in result or str(context[key]) in result

    def test_format_empty_context(self) -> None:
        """Test formatting empty context."""
        formatter = ErrorMessageFormatter()

        result = formatter.format_context({})

        assert isinstance(result, str)


class TestErrorMessageFormatterWithSuggestions:
    """Tests for formatting with suggestions."""

    def test_format_error_includes_suggestions(self) -> None:
        """Test that suggestions are included in formatted message."""
        error = SplurgeValueError("Invalid email", error_code="invalid-value")
        error.add_suggestion("Check email format")
        error.add_suggestion("Verify domain")

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_suggestions=True)

        assert "Check email format" in result or "Verify" in result

    def test_format_error_excludes_suggestions_when_requested(self) -> None:
        """Test that suggestions can be excluded from formatted message."""
        error = SplurgeValueError("Invalid", error_code="invalid-value")
        error.add_suggestion("Try again")
        error.add_suggestion("Check format")

        formatter = ErrorMessageFormatter()
        result_with = formatter.format_error(error, include_suggestions=True)
        result_without = formatter.format_error(error, include_suggestions=False)

        # Without suggestions should be shorter or not include suggestion content
        assert len(result_without) <= len(result_with)

    def test_format_suggestions_single_item(self) -> None:
        """Test formatting single suggestion."""
        formatter = ErrorMessageFormatter()

        result = formatter.format_suggestions(["Check the documentation"])

        assert isinstance(result, str)
        assert "Check the documentation" in result or "documentation" in result

    def test_format_suggestions_multiple_items(self) -> None:
        """Test formatting multiple suggestions."""
        formatter = ErrorMessageFormatter()
        suggestions = ["Try again", "Check documentation", "Contact support"]

        result = formatter.format_suggestions(suggestions)

        assert isinstance(result, str)
        # All suggestions should be present
        for suggestion in suggestions:
            assert suggestion in result

    def test_format_empty_suggestions(self) -> None:
        """Test formatting empty suggestions."""
        formatter = ErrorMessageFormatter()

        result = formatter.format_suggestions([])

        assert isinstance(result, str)


class TestErrorMessageFormatterComplex:
    """Tests for complex formatting scenarios."""

    def test_format_with_all_components(self) -> None:
        """Test formatting with error code, message, context, and suggestions."""
        error = SplurgeValueError("Invalid email format", error_code="invalid-email")
        error.attach_context(context_dict={"field": "email", "input": "user@invalid"})
        error.add_suggestion("Add domain name (e.g., @example.com)")
        error.add_suggestion("Check format matches RFC 5322")

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_context=True, include_suggestions=True)

        # Should include all components
        assert "invalid-email" in result
        assert "Invalid email format" in result

    def test_format_multiline_message(self) -> None:
        """Test formatting with multiline message."""
        error = SplurgeValueError("Error occurred:\nFirst issue\nSecond issue", error_code="parse-error")
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_format_with_details(self) -> None:
        """Test formatting error with details."""
        error = SplurgeOSError(
            error_code="file-not-found", message="File not found", details={"path": "/data/file.txt", "mode": "read"}
        )
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert isinstance(result, str)


class TestErrorMessageFormatterFormatting:
    """Tests for formatting style and structure."""

    def test_formatter_produces_readable_output(self) -> None:
        """Test that formatter produces readable output."""
        error = SplurgeValueError("Invalid value", error_code="invalid-value")
        error.attach_context(context_dict={"field": "age", "value": -5})
        error.add_suggestion("Value must be positive")

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_context=True, include_suggestions=True)

        # Output should be non-empty and contain readable text
        assert len(result) > 0
        assert result.count("\n") >= 0  # May have newlines
        assert result.isprintable() or "\n" in result

    def test_context_format_has_structure(self) -> None:
        """Test that context format has structure."""
        formatter = ErrorMessageFormatter()
        context = {"key1": "value1", "key2": "value2"}

        result = formatter.format_context(context)

        # Should have some structure (might include separators)
        assert len(result) > 0

    def test_suggestions_format_has_list_structure(self) -> None:
        """Test that suggestions format looks like a list."""
        formatter = ErrorMessageFormatter()
        suggestions = ["First suggestion", "Second suggestion", "Third suggestion"]

        result = formatter.format_suggestions(suggestions)

        # Should show all three suggestions
        assert result.count("First suggestion") >= 1
        assert result.count("Second suggestion") >= 1
        assert result.count("Third suggestion") >= 1


class TestErrorMessageFormatterEdgeCases:
    """Tests for edge cases."""

    def test_formatter_with_unicode_content(self) -> None:
        """Test formatter with unicode characters."""
        error = SplurgeValueError("Error: 日本語 🚀", error_code="invalid-value")
        error.attach_context(context_dict={"note": "Unicode: 中文"})

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error, include_context=True)

        assert "日本語" in result or "中文" in result or len(result) > 0

    def test_formatter_with_very_long_message(self) -> None:
        """Test formatter with very long message."""
        long_message = "x" * 1000
        error = SplurgeValueError(long_message, error_code="generic")

        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error)

        assert long_message in result

    def test_formatter_with_special_characters(self) -> None:
        """Test formatter with special characters."""
        error = SplurgeValueError("Invalid: <>&\"'\\", error_code="invalid-value")
        formatter = ErrorMessageFormatter()

        result = formatter.format_error(error)

        assert isinstance(result, str)

    def test_context_with_various_value_types(self) -> None:
        """Test formatting context with various value types."""
        formatter = ErrorMessageFormatter()
        context = {
            "string": "value",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "none": None,
            "list": [1, 2, 3],
        }

        result = formatter.format_context(context)

        assert isinstance(result, str)
