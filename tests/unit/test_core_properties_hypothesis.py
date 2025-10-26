"""Property-based tests using Hypothesis for SplurgeError base class.

Tests core error handling and validation behavior using property-based testing
to validate framework behavior across a wide range of automatically generated inputs.
"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from splurge_exceptions import SplurgeError, SplurgeValueError

# ============================================================================
# Custom Strategies
# ============================================================================


@st.composite
def valid_error_codes(draw) -> str:
    """Generate valid error codes.

    Error codes must:
    - Start with lowercase letter
    - Contain only lowercase letters, digits, and hyphens
    - End with lowercase letter or digit
    - Be at least 2 characters
    """
    first_char = draw(st.sampled_from("abcdefghijklmnopqrstuvwxyz"))
    middle_chars = draw(st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789-", min_size=0, max_size=20))
    last_char = draw(st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789"))
    return f"{first_char}{middle_chars}{last_char}"


@st.composite
def valid_domains(draw) -> str:
    """Generate valid domain identifiers.

    Domains can have multiple dot-separated components.
    """
    num_components = draw(st.integers(min_value=1, max_value=4))
    components = [draw(valid_error_codes()) for _ in range(num_components)]
    return ".".join(components)


# ============================================================================
# SplurgeError Core Properties
# ============================================================================


class TestSplurgeErrorCoreProperties:
    """Property-based tests for SplurgeError core functionality."""

    @given(valid_error_codes())
    def test_valid_error_code_accepted(self, error_code: str) -> None:
        """Property: Valid error codes are always accepted."""
        error = SplurgeValueError(error_code=error_code)
        assert error.error_code == error_code

    @given(valid_domains())
    def test_valid_domain_in_subclass(self, domain: str) -> None:
        """Property: Valid domains work in dynamic exception classes."""
        exc_class = type("TestError", (SplurgeError,), {"_domain": domain})
        error = exc_class(error_code="test-code")
        assert error.domain == domain

    @given(valid_error_codes(), st.text(min_size=0, max_size=200))
    def test_error_code_and_message_preserved(self, error_code: str, message: str) -> None:
        """Property: Error code and message are always preserved."""
        error = SplurgeValueError(error_code=error_code, message=message)
        assert error.error_code == error_code
        assert error._message == message

    @given(valid_error_codes())
    def test_full_code_combines_domain_and_code(self, error_code: str) -> None:
        """Property: Full code combines domain and error code with dot."""
        error = SplurgeValueError(error_code=error_code)
        assert error.full_code == f"splurge.value.{error_code}"
        assert error.full_code.endswith(error_code)

    @given(valid_error_codes(), st.dictionaries(st.text(min_size=1, max_size=30), st.text(max_size=100), max_size=10))
    def test_details_preserved(self, error_code: str, details: dict[str, str]) -> None:
        """Property: Details dictionary is always preserved."""
        error = SplurgeValueError(error_code=error_code, details=details)
        for key, value in details.items():
            assert error.details[key] == value

    @given(valid_error_codes())
    def test_context_attachment(self, error_code: str) -> None:
        """Property: Context can always be attached after creation."""
        error = SplurgeValueError(error_code=error_code)
        error.attach_context(key="field", value="value")
        assert error.has_context("field")
        assert error.get_context("field") == "value"
        assert "field" in error.get_all_context()

    @given(valid_error_codes(), st.lists(st.text(min_size=1, max_size=100), max_size=10))
    def test_suggestions_addition(self, error_code: str, suggestions: list[str]) -> None:
        """Property: Suggestions can always be added after creation."""
        error = SplurgeValueError(error_code=error_code)
        for suggestion in suggestions:
            error.add_suggestion(suggestion)
        for suggestion in suggestions:
            assert suggestion in error.get_suggestions()

    @given(valid_error_codes())
    def test_exception_base_types(self, error_code: str) -> None:
        """Property: Splurge errors are always proper Exception instances."""
        error = SplurgeValueError(error_code=error_code)
        assert isinstance(error, Exception)
        assert isinstance(error, SplurgeError)

    @given(valid_error_codes(), st.text(min_size=0, max_size=200))
    def test_message_includes_full_code(self, error_code: str, message: str) -> None:
        """Property: Exception message always includes full code."""
        error = SplurgeValueError(error_code=error_code, message=message)
        error_message = str(error)
        assert error.full_code in error_message

    @given(valid_error_codes())
    def test_can_be_raised_and_caught(self, error_code: str) -> None:
        """Property: Exceptions can always be raised and caught."""
        error = SplurgeValueError(error_code=error_code)
        with pytest.raises(SplurgeValueError):
            raise error

    @given(valid_error_codes())
    def test_multiple_context_items_accumulate(self, error_code: str) -> None:
        """Property: Multiple context attachments accumulate."""
        error = SplurgeValueError(error_code=error_code)
        error.attach_context(key="key1", value="value1")
        error.attach_context(key="key2", value="value2")
        error.attach_context(key="key3", value="value3")
        context = error.get_all_context()
        assert context["key1"] == "value1"
        assert context["key2"] == "value2"
        assert context["key3"] == "value3"


# ============================================================================
# Error Code Validation Properties
# ============================================================================


class TestErrorCodeValidationProperties:
    """Property-based tests for error code validation."""

    @given(valid_error_codes())
    def test_no_dots_in_code(self, error_code: str) -> None:
        """Property: Valid error codes never contain dots."""
        assert "." not in error_code

    @given(valid_error_codes())
    def test_starts_with_lowercase(self, error_code: str) -> None:
        """Property: Valid error codes start with lowercase letter."""
        assert error_code[0].islower()
        assert error_code[0].isalpha()

    @given(valid_error_codes())
    def test_ends_with_alphanumeric(self, error_code: str) -> None:
        """Property: Valid error codes end with letter or digit."""
        assert error_code[-1].isalnum()

    @given(valid_error_codes())
    def test_only_valid_chars(self, error_code: str) -> None:
        """Property: Valid error codes only contain valid characters."""
        valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-")
        assert all(c in valid_chars for c in error_code)

    @given(valid_error_codes())
    def test_min_length_two(self, error_code: str) -> None:
        """Property: Valid error codes are at least 2 characters."""
        assert len(error_code) >= 2


# ============================================================================
# Domain Validation Properties
# ============================================================================


class TestDomainValidationProperties:
    """Property-based tests for domain validation."""

    @given(valid_domains())
    def test_starts_with_lowercase(self, domain: str) -> None:
        """Property: Valid domains start with lowercase letter."""
        assert domain[0].islower()
        assert domain[0].isalpha()

    @given(valid_domains())
    def test_components_valid(self, domain: str) -> None:
        """Property: All domain components are individually valid."""
        components = domain.split(".")
        for component in components:
            assert "." not in component
            assert component[0].islower()
            assert component[-1].isalnum()

    @given(valid_domains())
    def test_no_empty_components(self, domain: str) -> None:
        """Property: Valid domains don't have empty components."""
        assert ".." not in domain

    @given(valid_domains())
    def test_only_valid_chars(self, domain: str) -> None:
        """Property: Valid domains only contain valid characters."""
        valid_chars = set("abcdefghijklmnopqrstuvwxyz0123456789-.")
        assert all(c in valid_chars for c in domain)


# ============================================================================
# State Management Properties
# ============================================================================


class TestStateManagementProperties:
    """Property-based tests for exception state management."""

    @given(valid_error_codes(), st.lists(st.text(min_size=1), max_size=10))
    def test_suggestions_order_preserved(self, error_code: str, suggestions: list[str]) -> None:
        """Property: Suggestions maintain insertion order."""
        error = SplurgeValueError(error_code=error_code)
        for suggestion in suggestions:
            error.add_suggestion(suggestion)
        for i, suggestion in enumerate(suggestions):
            assert error.get_suggestions()[i] == suggestion

    @given(valid_error_codes(), st.dictionaries(st.text(min_size=1), st.integers(), min_size=1, max_size=5))
    def test_context_multiple_types(self, error_code: str, context: dict[str, int]) -> None:
        """Property: Context handles different value types."""
        error = SplurgeValueError(error_code=error_code)
        error.attach_context(context_dict=context)
        retrieved = error.get_all_context()
        for key, value in context.items():
            assert retrieved[key] == value


# ============================================================================
# Integration Properties
# ============================================================================


class TestIntegrationProperties:
    """Property-based tests for integration scenarios."""

    @given(valid_error_codes(), st.text(min_size=0, max_size=100))
    def test_raised_and_caught(self, error_code: str, message: str) -> None:
        """Property: Exceptions can be raised and caught correctly."""
        error = SplurgeValueError(error_code=error_code, message=message)

        with pytest.raises(SplurgeValueError) as exc_info:
            raise error

        assert exc_info.value.error_code == error_code

    @given(
        valid_error_codes(),
        st.dictionaries(st.text(min_size=1), st.text(), min_size=1, max_size=3),
        st.lists(st.text(min_size=1), max_size=3),
    )
    def test_full_context_and_suggestions(
        self, error_code: str, context: dict[str, str], suggestions: list[str]
    ) -> None:
        """Property: Exceptions can have both context and suggestions."""
        error = SplurgeValueError(error_code=error_code)
        error.attach_context(context_dict=context)
        for suggestion in suggestions:
            error.add_suggestion(suggestion)

        retrieved_context = error.get_all_context()
        for key, value in context.items():
            assert retrieved_context[key] == value
        retrieved_suggestions = error.get_suggestions()
        for suggestion in suggestions:
            assert suggestion in retrieved_suggestions

    @given(valid_error_codes())
    def test_exception_chaining(self, error_code: str) -> None:
        """Property: Exceptions can be properly chained."""
        error1 = SplurgeValueError(error_code="first-error")
        error2 = SplurgeValueError(error_code="second-error")

        try:
            raise error1
        except SplurgeValueError as e:
            try:
                raise error2 from e
            except SplurgeValueError as e2:
                assert e2.__cause__ is e
                assert e.__cause__ is None
