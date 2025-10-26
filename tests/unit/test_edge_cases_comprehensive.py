"""Comprehensive edge case tests addressing specific coverage gaps.

Tests for:
1. Context size limits and deeply nested structures
2. Error code length boundaries (min/max)
3. Deep domain hierarchies
4. Context key edge cases (empty, special chars, etc.)
5. Suggestion edge cases (empty, duplicates, very long)
6. Exception chaining (circular refs, deep chains)
"""

from __future__ import annotations

import pytest

from splurge_exceptions import (
    ErrorMessageFormatter,
    SplurgeAttributeError,
    SplurgeImportError,
    SplurgeRuntimeError,
    SplurgeSubclassError,
    SplurgeTypeError,
    SplurgeValueError,
)


class TestContextSizeLimits:
    """Test context with large/deeply nested data structures."""

    def test_context_with_very_large_dictionary(self) -> None:
        """Test attaching context with large number of key-value pairs."""
        exc = SplurgeValueError(error_code="large-context", message="Large context test")

        # Create a context with 1000 key-value pairs
        large_context = {f"key_{i}": f"value_{i}" for i in range(1000)}
        exc.attach_context(context_dict=large_context)

        assert len(exc.get_all_context()) == 1000
        assert exc.get_context("key_500") == "value_500"
        assert exc.get_context("key_999") == "value_999"

    def test_context_with_deeply_nested_structure(self) -> None:
        """Test attaching deeply nested dictionary structures."""
        exc = SplurgeValueError(error_code="nested", message="Nested context test")

        # Create a deeply nested structure (10 levels)
        nested = {"level": 0}
        current = nested
        for i in range(1, 10):
            current["child"] = {"level": i}
            current = current["child"]

        exc.attach_context(context_dict={"deep_structure": nested})

        retrieved = exc.get_context("deep_structure")
        assert retrieved is not None
        assert retrieved["level"] == 0
        # Navigate to the deepest level
        current = retrieved
        for _ in range(9):
            assert "child" in current
            current = current["child"]
        assert current["level"] == 9

    def test_context_with_large_list_values(self) -> None:
        """Test context values containing large lists."""
        exc = SplurgeValueError(error_code="list-context", message="List context test")

        large_list = list(range(10000))
        exc.attach_context(context_dict={"items": large_list})

        retrieved = exc.get_context("items")
        assert len(retrieved) == 10000
        assert retrieved[0] == 0
        assert retrieved[9999] == 9999

    def test_context_with_nested_mutable_objects(self) -> None:
        """Test shallow copy behavior: nested mutable objects are shared."""
        exc1 = SplurgeValueError(error_code="iso1", message="Isolation test 1")

        # Shallow copy means nested structures ARE shared
        nested = {"status": ["pending"]}
        exc1.attach_context(context_dict=nested)

        # Modifying nested list in original affects exc1 (shallow copy behavior)
        nested["status"].append("modified")
        retrieved = exc1.get_context("status")
        assert retrieved == ["pending", "modified"]  # shallow copy - nested mutation visible

        # But top-level key changes don't affect stored context
        nested["new_key"] = "value"
        assert not exc1.has_context("new_key")


class TestErrorCodeLengthBoundaries:
    """Test error code minimum and maximum length boundaries."""

    def test_error_code_minimum_length_2_chars(self) -> None:
        """Test that 2-character error codes are valid (minimum)."""
        # Minimum valid: 2 chars, lowercase letter start/end
        exc = SplurgeValueError(error_code="ab", message="Two char code")
        assert exc.error_code == "ab"

    def test_error_code_1_char_invalid(self) -> None:
        """Test that 1-character error codes are invalid."""
        # Single char does not match pattern (needs start + end = 2 minimum)
        with pytest.raises(SplurgeSubclassError):
            SplurgeValueError(error_code="a", message="One char code")

    def test_error_code_very_long_valid(self) -> None:
        """Test that very long error codes (100+ chars) are valid."""
        long_code = "a" + "b" * 98 + "c"  # 100 chars, valid pattern
        exc = SplurgeValueError(error_code=long_code, message="Very long code")
        assert exc.error_code == long_code
        assert len(exc.error_code) == 100

    def test_error_code_with_all_hyphens_middle(self) -> None:
        """Test error code with maximum hyphens in middle."""
        # Pattern: starts with letter, ends with letter/digit, hyphens in middle
        code = "a" + "-" * 50 + "z"
        exc = SplurgeValueError(error_code=code, message="Max hyphens")
        assert exc.error_code == code

    def test_error_code_alternating_letters_and_hyphens(self) -> None:
        """Test error code with alternating pattern."""
        code = "a-b-c-d-e-f-g-h-i-j-k"
        exc = SplurgeValueError(error_code=code, message="Alternating")
        assert exc.error_code == code

    def test_error_code_with_many_digits(self) -> None:
        """Test error code with multiple digits."""
        code = "error-123-456-789"
        exc = SplurgeValueError(error_code=code, message="With digits")
        assert exc.error_code == code


class TestDeepDomainHierarchies:
    """Test exception handling with very deep domain hierarchies."""

    def test_domain_with_2_components(self) -> None:
        """Test valid 2-component domain."""
        exc = SplurgeValueError(error_code="test", message="Two component")
        exc._domain = "database.sql"
        assert exc.domain == "database.sql"
        assert exc.full_code == "database.sql.test"

    def test_domain_with_5_components(self) -> None:
        """Test valid 5-component domain hierarchy."""
        exc = SplurgeValueError(error_code="test", message="Five component")
        exc._domain = "app.service.database.query.validation"
        assert exc.domain == "app.service.database.query.validation"
        assert exc.full_code == "app.service.database.query.validation.test"

    def test_domain_with_10_components(self) -> None:
        """Test very deep 10-component domain hierarchy."""
        exc = SplurgeValueError(error_code="test", message="Deep hierarchy")
        exc._domain = "a.b.c.d.e.f.g.h.i.j"
        assert exc.domain == "a.b.c.d.e.f.g.h.i.j"
        assert exc.full_code == "a.b.c.d.e.f.g.h.i.j.test"

    def test_domain_with_15_components(self) -> None:
        """Test extremely deep 15-component domain."""
        components = ".".join([chr(ord("a") + (i % 26)) for i in range(15)])
        exc = SplurgeValueError(error_code="test", message="Extreme depth")
        exc._domain = components
        assert exc.full_code.startswith(components)

    def test_very_long_domain_component_names(self) -> None:
        """Test domain with long individual component names."""
        # Each component can be very long
        component = "a" + "b" * 48 + "c"  # 50 char valid component
        exc = SplurgeValueError(error_code="test", message="Long components")
        exc._domain = f"{component}.{component}"
        assert exc.domain == f"{component}.{component}"


class TestContextKeyEdgeCases:
    """Test edge cases in context key handling."""

    def test_context_key_with_special_characters(self) -> None:
        """Test context keys containing special characters."""
        exc = SplurgeValueError(error_code="special-keys", message="Special keys test")

        special_keys = {
            "key-with-hyphens": "value1",
            "key_with_underscores": "value2",
            "key.with.dots": "value3",
            "key/with/slashes": "value4",
            "key@with#special$chars": "value5",
            "key with spaces": "value6",
            "キー": "japanese",
            "钥匙": "chinese",
        }

        exc.attach_context(context_dict=special_keys)

        for key, expected in special_keys.items():
            assert exc.get_context(key) == expected

    def test_context_key_single_character(self) -> None:
        """Test context with single-character keys."""
        exc = SplurgeValueError(error_code="single-char-keys", message="Single char keys")

        exc.attach_context(context_dict={"a": 1, "b": 2, "c": 3})

        assert exc.get_context("a") == 1
        assert exc.get_context("b") == 2
        assert exc.get_context("c") == 3

    def test_context_key_very_long(self) -> None:
        """Test context with very long keys."""
        exc = SplurgeValueError(error_code="long-keys", message="Long keys test")

        long_key = "k" * 1000
        exc.attach_context(context_dict={long_key: "long-key-value"})

        assert exc.get_context(long_key) == "long-key-value"

    def test_context_key_numeric_string(self) -> None:
        """Test context with numeric string keys."""
        exc = SplurgeValueError(error_code="numeric-keys", message="Numeric string keys")

        exc.attach_context(
            context_dict={
                "0": "zero",
                "123": "one-two-three",
                "999": "large-number",
            }
        )

        assert exc.get_context("0") == "zero"
        assert exc.get_context("123") == "one-two-three"
        assert exc.get_context("999") == "large-number"

    def test_context_overwrite_existing_key(self) -> None:
        """Test overwriting existing context keys."""
        exc = SplurgeValueError(error_code="overwrite", message="Overwrite test")

        exc.attach_context(key="status", value="pending")
        assert exc.get_context("status") == "pending"

        exc.attach_context(key="status", value="active")
        assert exc.get_context("status") == "active"

        exc.attach_context(context_dict={"status": "complete"})
        assert exc.get_context("status") == "complete"


class TestSuggestionEdgeCases:
    """Test edge cases in suggestion handling."""

    def test_suggestion_empty_string(self) -> None:
        """Test adding empty string as suggestion."""
        exc = SplurgeValueError(error_code="empty-sugg", message="Empty suggestion")

        exc.add_suggestion("")
        exc.add_suggestion("Valid suggestion")

        suggestions = exc.get_suggestions()
        assert len(suggestions) == 2
        assert suggestions[0] == ""
        assert suggestions[1] == "Valid suggestion"

    def test_suggestion_very_long(self) -> None:
        """Test adding very long suggestion."""
        exc = SplurgeValueError(error_code="long-sugg", message="Long suggestion")

        long_suggestion = "Try this: " + ("x" * 10000)
        exc.add_suggestion(long_suggestion)

        assert exc.get_suggestions()[0] == long_suggestion
        assert len(exc.get_suggestions()[0]) > 10000

    def test_suggestion_duplicate_values(self) -> None:
        """Test adding duplicate suggestions (should be allowed)."""
        exc = SplurgeValueError(error_code="dup-sugg", message="Duplicate suggestions")

        exc.add_suggestion("Try again")
        exc.add_suggestion("Try again")
        exc.add_suggestion("Try again")

        suggestions = exc.get_suggestions()
        assert len(suggestions) == 3
        assert all(s == "Try again" for s in suggestions)

    def test_suggestion_with_special_characters(self) -> None:
        """Test suggestions with special characters."""
        exc = SplurgeValueError(error_code="special-sugg", message="Special suggestions")

        special_suggestions = [
            "Try: key=\"value\", other='data'",
            "Use regex: ^[a-z]+$",
            "Unicode: 日本語 中文 🚀",
            "Path: C:\\Users\\test\\file.txt",
            "SQL: SELECT * FROM users WHERE id=123",
        ]

        for sugg in special_suggestions:
            exc.add_suggestion(sugg)

        retrieved = exc.get_suggestions()
        assert len(retrieved) == len(special_suggestions)
        for i, sugg in enumerate(special_suggestions):
            assert retrieved[i] == sugg

    def test_many_suggestions(self) -> None:
        """Test adding many suggestions."""
        exc = SplurgeValueError(error_code="many-sugg", message="Many suggestions")

        for i in range(100):
            exc.add_suggestion(f"Suggestion {i}: try approach {i}")

        suggestions = exc.get_suggestions()
        assert len(suggestions) == 100
        assert suggestions[0] == "Suggestion 0: try approach 0"
        assert suggestions[99] == "Suggestion 99: try approach 99"

    def test_suggestion_with_newlines_and_tabs(self) -> None:
        """Test suggestions containing newlines and tabs."""
        exc = SplurgeValueError(error_code="whitespace-sugg", message="Whitespace suggestions")

        exc.add_suggestion("Line 1\nLine 2\nLine 3")
        exc.add_suggestion("Column1\tColumn2\tColumn3")

        suggestions = exc.get_suggestions()
        assert "\n" in suggestions[0]
        assert "\t" in suggestions[1]


class TestExceptionChaining:
    """Test exception chaining with deep chains and circular references."""

    def test_simple_exception_chain_two_levels(self) -> None:
        """Test basic exception chaining with 'raise from'."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise SplurgeValueError(error_code="chained", message="Chained error") from e
        except SplurgeValueError as exc:
            assert exc.__cause__.__class__ is ValueError
            assert str(exc.__cause__) == "Original error"

    def test_deep_exception_chain_five_levels(self) -> None:
        """Test deep exception chain with 5 levels."""
        try:
            try:
                try:
                    try:
                        try:
                            raise ValueError("Level 5")
                        except ValueError as e:
                            raise SplurgeTypeError(error_code="level-4", message="L4") from e
                    except SplurgeTypeError as e:
                        raise SplurgeAttributeError(error_code="level-3", message="L3") from e
                except SplurgeAttributeError as e:
                    raise SplurgeRuntimeError(error_code="level-2", message="L2") from e
            except SplurgeRuntimeError as e:
                raise SplurgeImportError(error_code="level-1", message="L1") from e
        except SplurgeImportError as exc:
            # Verify the chain
            assert isinstance(exc.__cause__, SplurgeRuntimeError)
            assert isinstance(exc.__cause__.__cause__, SplurgeAttributeError)
            assert isinstance(exc.__cause__.__cause__.__cause__, SplurgeTypeError)
            assert isinstance(exc.__cause__.__cause__.__cause__.__cause__, ValueError)

    def test_exception_chain_with_context_preservation(self) -> None:
        """Test that context and suggestions are preserved when chaining."""
        try:
            try:
                raise ValueError("Original")
            except ValueError as e:
                exc = SplurgeValueError(error_code="wrapped", message="Wrapped error")
                exc.attach_context(key="original_error", value=str(e))
                exc.add_suggestion("Check the original error")
                raise exc from e
        except SplurgeValueError as exc:
            assert exc.get_context("original_error") == "Original"
            assert exc.has_suggestions()
            assert "original error" in exc.get_suggestions()[0]

    def test_exception_chain_suppressed_context(self) -> None:
        """Test exception chaining with implicit context suppression."""
        try:
            try:
                raise ValueError("First error")
            except ValueError:
                # Explicitly suppress context
                raise SplurgeValueError(error_code="suppress", message="Suppressed") from None
        except SplurgeValueError as exc:
            # __cause__ should be None when explicitly suppressed
            assert exc.__cause__ is None

    def test_exception_chain_with_formatted_output(self) -> None:
        """Test that chained exceptions format correctly."""
        try:
            try:
                raise RuntimeError("Database connection failed")
            except RuntimeError as e:
                exc = SplurgeRuntimeError(error_code="db-error", message="DB Error")
                exc.add_suggestion("Retry connection")
                raise exc from e
        except SplurgeRuntimeError as exc:
            formatter = ErrorMessageFormatter()
            output = formatter.format_error(exc, include_context=True, include_suggestions=True)
            assert isinstance(output, str)
            assert "DB Error" in output

    def test_exception_with_cause_and_modifications_after_chain(self) -> None:
        """Test modifying exception after it's been chained."""
        try:
            try:
                raise KeyError("Missing key")
            except KeyError as e:
                exc = SplurgeValueError(error_code="key-error", message="Key missing")
                raise exc from e
        except SplurgeValueError as exc:
            # Modify after chaining
            exc.attach_context(key="key_name", value="user_id")
            exc.add_suggestion("Provide the missing key")

            assert exc.get_context("key_name") == "user_id"
            assert exc.has_suggestions()
            assert exc.__cause__.__class__ is KeyError
