"""Property-based tests using Hypothesis for core exception functionality."""

from hypothesis import given, settings
from hypothesis import strategies as st

from splurge_exceptions import SplurgeOSError, SplurgeValueError


@st.composite
def valid_error_codes(draw):
    """Generate valid semantic error codes."""
    start = draw(st.sampled_from("abcdefghijklmnopqrstuvwxyz"))
    middle_chars = st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789-")
    middle = draw(st.text(middle_chars, min_size=0, max_size=20))
    end = draw(st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789"))
    return start + middle + end


@st.composite
def valid_messages(draw):
    """Generate valid error messages."""
    return draw(st.text(min_size=1, max_size=1000))


class TestSplurgeErrorCoreProperties:
    """Property-based tests for core SplurgeError functionality."""

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=100)
    def test_message_always_preserved(self, message, error_code):
        """Property: Message is always preserved exactly as provided."""
        error = SplurgeValueError(message, error_code=error_code)
        assert error.message == message

    @given(message=valid_messages())
    @settings(max_examples=50)
    def test_error_code_none_when_not_provided(self, message):
        """Property: Error code is None when not provided."""
        error = SplurgeValueError(message)
        assert error.error_code is None

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=100)
    def test_full_code_format_consistency(self, message, error_code):
        """Property: full_code always has consistent format."""
        error = SplurgeValueError(message, error_code=error_code)
        assert isinstance(error.full_code, str)
        assert len(error.full_code) > 0

    @given(
        message=valid_messages(),
        error_code=valid_error_codes() | st.none(),
        details=st.dictionaries(st.text(min_size=1), st.text()),
    )
    @settings(max_examples=100)
    def test_details_preserved(self, message, error_code, details):
        """Property: Details dictionary is always preserved completely."""
        error = SplurgeValueError(message, error_code=error_code, details=details)
        assert error.details == details

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=100)
    def test_can_attach_context(self, message, error_code):
        """Property: Context can always be attached to any exception."""
        error = SplurgeValueError(message, error_code=error_code)
        error.attach_context(key="test_key", value="test_value")
        assert error.get_context("test_key") == "test_value"

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=100)
    def test_can_add_suggestions(self, message, error_code):
        """Property: Suggestions can always be added to any exception."""
        error = SplurgeValueError(message, error_code=error_code)
        error.add_suggestion("First suggestion")
        error.add_suggestion("Second suggestion")
        suggestions = error.get_suggestions()
        assert len(suggestions) == 2

    @given(
        message=valid_messages(),
        error_code=valid_error_codes() | st.none(),
        context_data=st.dictionaries(st.text(min_size=1), st.integers(), min_size=1),
    )
    @settings(max_examples=100)
    def test_context_dict_preserved(self, message, error_code, context_data):
        """Property: Context dictionary is preserved completely."""
        error = SplurgeValueError(message, error_code=error_code)
        error.attach_context(context_dict=context_data)
        all_context = error.get_all_context()
        assert all_context == context_data

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=100)
    def test_exception_can_be_raised(self, message, error_code):
        """Property: Exception can always be raised and caught."""
        error = SplurgeValueError(message, error_code=error_code)
        try:
            raise error
        except SplurgeValueError as caught:
            assert caught.message == message

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=50)
    def test_str_representation_valid(self, message, error_code):
        """Property: String representation is always valid."""
        error = SplurgeValueError(message, error_code=error_code)
        str_repr = str(error)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0


class TestErrorCodeNormalizationProperties:
    """Property-based tests for error code normalization."""

    @given(
        message=valid_messages(),
        base_code=st.text(st.sampled_from("abcdefghijklmnopqrstuvwxyz"), min_size=1, max_size=10),
    )
    @settings(max_examples=100)
    def test_lowercase_codes_normalized(self, message, base_code):
        """Property: All error codes are normalized to lowercase."""
        uppercase_code = base_code.upper()
        error = SplurgeValueError(message, error_code=uppercase_code)
        if error.error_code is not None:
            assert error.error_code == error.error_code.lower()

    @given(message=valid_messages())
    @settings(max_examples=50)
    def test_empty_code_becomes_none(self, message):
        """Property: Empty string codes become None after normalization."""
        error = SplurgeValueError(message, error_code="")
        assert error.error_code is None


class TestContextManagementProperties:
    """Property-based tests for context management."""

    @given(
        message=valid_messages(),
        context_items=st.dictionaries(
            st.text(min_size=1, max_size=20), st.integers(), min_size=1, max_size=10
        ),
    )
    @settings(max_examples=100)
    def test_context_retrieval_consistency(self, message, context_items):
        """Property: Retrieved context always matches attached context."""
        error = SplurgeValueError(message)
        for key, value in context_items.items():
            error.attach_context(key=key, value=value)
        retrieved = error.get_all_context()
        for key, value in context_items.items():
            assert retrieved[key] == value

    @given(
        message=valid_messages(),
        context_items=st.dictionaries(
            st.text(min_size=1, max_size=20), st.text(min_size=0, max_size=100), min_size=1, max_size=5
        ),
    )
    @settings(max_examples=100)
    def test_context_dict_attachment(self, message, context_items):
        """Property: Context dictionary is completely preserved."""
        error = SplurgeValueError(message)
        if context_items:  # Only test if dict is not empty
            error.attach_context(context_dict=context_items)
            retrieved = error.get_all_context()
            assert retrieved == context_items

    @given(
        message=valid_messages(),
        suggestions=st.lists(valid_messages(), min_size=1, max_size=10),
    )
    @settings(max_examples=100)
    def test_suggestions_order_preserved(self, message, suggestions):
        """Property: Suggestions are always preserved in order."""
        error = SplurgeValueError(message)
        for suggestion in suggestions:
            error.add_suggestion(suggestion)
        retrieved = error.get_suggestions()
        assert retrieved == suggestions


class TestMessageFormattingProperties:
    """Property-based tests for message formatting."""

    @given(
        message=valid_messages(),
        error_code=valid_error_codes() | st.none(),
    )
    @settings(max_examples=100)
    def test_get_full_message_valid(self, message, error_code):
        """Property: get_full_message always returns a valid string."""
        error = SplurgeValueError(message, error_code=error_code)
        full_message = error.get_full_message()
        assert isinstance(full_message, str)
        assert len(full_message) > 0

    @given(
        message=valid_messages(),
        error_code=valid_error_codes() | st.none(),
    )
    @settings(max_examples=100)
    def test_formatter_never_raises(self, message, error_code):
        """Property: Message formatter never raises on any valid message."""
        from splurge_exceptions import ErrorMessageFormatter

        error = SplurgeValueError(message, error_code=error_code)
        formatter = ErrorMessageFormatter()
        result = formatter.format_error(error)
        assert isinstance(result, str)
        assert len(result) > 0


class TestExceptionHierarchyProperties:
    """Property-based tests for exception type hierarchy."""

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=50)
    def test_splurge_value_error_is_exception(self, message, error_code):
        """Property: SplurgeValueError is always an Exception."""
        error = SplurgeValueError(message, error_code=error_code)
        assert isinstance(error, Exception)

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=50)
    def test_splurge_os_error_is_exception(self, message, error_code):
        """Property: SplurgeOSError is always an Exception."""
        error = SplurgeOSError(message, error_code=error_code)
        assert isinstance(error, Exception)

    @given(message=valid_messages(), error_code=valid_error_codes() | st.none())
    @settings(max_examples=50)
    def test_exception_chaining_works(self, message, error_code):
        """Property: Exception chaining always works."""
        original = ValueError("Original error")
        try:
            raise original
        except ValueError as e:
            error = SplurgeValueError(message, error_code=error_code)
            error.__cause__ = e
            assert error.__cause__ is original


class TestIntegrationProperties:
    """Integration property-based tests combining multiple features."""

    @given(
        message=valid_messages(),
        error_code=valid_error_codes() | st.none(),
        context=st.dictionaries(st.text(min_size=1), st.text(), max_size=5),
        suggestions=st.lists(valid_messages(), max_size=3),
    )
    @settings(max_examples=100)
    def test_full_workflow(self, message, error_code, context, suggestions):
        """Property: Full exception workflow works end-to-end."""
        error = SplurgeValueError(message, error_code=error_code)

        if context:
            error.attach_context(context_dict=context)

        for suggestion in suggestions:
            error.add_suggestion(suggestion)

        try:
            raise error
        except SplurgeValueError as caught:
            assert caught.message == message
            if context:
                assert caught.get_all_context() == context
            assert caught.get_suggestions() == suggestions

    @given(
        message=valid_messages(),
        error_code=valid_error_codes() | st.none(),
    )
    @settings(max_examples=100)
    def test_method_chaining_works(self, message, error_code):
        """Property: Method chaining always works."""
        error = (
            SplurgeValueError(message, error_code=error_code)
            .attach_context(key="key1", value="value1")
            .attach_context(key="key2", value="value2")
            .add_suggestion("Suggestion 1")
            .add_suggestion("Suggestion 2")
        )

        assert error.has_context("key1")
        assert error.has_context("key2")
        assert len(error.get_suggestions()) == 2
