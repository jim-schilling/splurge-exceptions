"""Additional property-based tests for core exception behaviors.

These tests cover:
- Pickle roundtrip preserves core fields
- attach_context with context_dict does not copy later-added keys
- Unicode and long strings in codes/messages/context
- Invalid error_code inputs raise ValueError

These complement the existing `test_core_properties_hypothesis.py` suite.
"""

from __future__ import annotations

import pickle
import re
from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from splurge_exceptions import ErrorMessageFormatter, SplurgeSubclassError, SplurgeValueError


@given(
    # match library's VALID_COMPONENT_PATTERN: start with letter, end with letter/digit
    code=st.from_regex(r"^[a-z][a-z0-9-]{0,18}[a-z0-9]$", fullmatch=True),
    message=st.text(min_size=1, max_size=200),
    ctx=st.dictionaries(st.text(min_size=1, max_size=10), st.one_of(st.integers(), st.text()), min_size=1, max_size=5),
    suggestions=st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5),
)
def test_exception_pickle_roundtrip_preserves_core_fields(
    code: str, message: str, ctx: dict[str, Any], suggestions: list[str]
) -> None:
    """Pickling and unpickling should preserve error_code, context and suggestions."""

    exc = SplurgeValueError(message, error_code=code)

    # attach context via context_dict API
    exc.attach_context(context_dict=ctx)

    for s in suggestions:
        exc.add_suggestion(s)

    # exercise formatter too (should not raise)
    fmt = ErrorMessageFormatter()
    _ = fmt.format_error(exc, include_context=True)

    packed = pickle.loads(pickle.dumps(exc))

    assert packed.error_code == exc.error_code
    assert packed.get_all_context() == exc.get_all_context()
    assert packed.get_suggestions() == exc.get_suggestions()


@given(d=st.dictionaries(st.text(min_size=1, max_size=10), st.integers() | st.text(), min_size=1, max_size=5))
def test_attach_context_with_context_dict_does_not_reflect_future_keys(d: dict[str, Any]) -> None:
    """When passing a dict to `attach_context(context_dict=...)`, later additions to the source dict are not reflected."""

    exc = SplurgeValueError("immutability", error_code="immutability-test")

    # attach by passing the dict; attach_context should copy current keys
    exc.attach_context(context_dict=d)

    # mutate the original dict by adding a new key
    d["__new_key__"] = "new"

    # the exception's context should NOT contain the newly-added key
    assert "__new_key__" not in exc.get_all_context()


@given(
    code=st.text(min_size=1, max_size=50),
    message=st.text(min_size=1, max_size=1000),
    ctx_key=st.text(min_size=1, max_size=20),
    ctx_value=st.text(min_size=0, max_size=500),
)
def test_unicode_and_long_strings_in_codes_messages_and_context(
    code: str, message: str, ctx_key: str, ctx_value: str
) -> None:
    """Unicode (including emoji) and long strings should be supported in messages and context values.

    Note: We do not assert the exact acceptance of arbitrary `code` values here because
    `error_code` must still satisfy validation; instead we exercise storing and
    formatting of unicode content in message and context.
    """

    # create a valid code falling back to a safe value if validation would fail
    if code and re.fullmatch(r"[a-z][a-z0-9-]{0,18}[a-z0-9]", code):
        safe_code = code
    else:
        safe_code = "unicode-test"

    exc = SplurgeValueError(message, error_code=safe_code)

    exc.attach_context(key=ctx_key, value=ctx_value)

    fmt = ErrorMessageFormatter()
    rendered = fmt.format_error(exc, include_context=True, include_suggestions=True)

    # rendered output must be a string and include the message
    assert isinstance(rendered, str)
    if message:
        assert message in rendered


@given(
    bad=st.one_of(
        # contains a space
        st.builds(lambda a, b: f"{a} {b}", st.text(min_size=1, max_size=10), st.text(min_size=0, max_size=10)),
        # contains a dot
        st.builds(lambda a, b: f"{a}.{b}", st.text(min_size=1, max_size=10), st.text(min_size=0, max_size=10)),
        # starts with a digit
        st.builds(
            lambda d, rest: f"{d}{rest}", st.sampled_from([str(i) for i in range(10)]), st.text(min_size=0, max_size=20)
        ),
    )
)
def test_invalid_error_codes_raise_value_error(bad: str) -> None:
    """User-supplied invalid error_code values should raise SplurgeSubclassError on construction."""

    try:
        # Attempt to construct with invalid code - constructor should validate
        SplurgeValueError("bad", error_code=bad)
    except SplurgeSubclassError:
        # expected
        return

    # If no SplurgeSubclassError was raised, ensure the code actually matched the allowed pattern
    # (this is defensive: if Hypothesis produced a valid component, accept it)
    assert all(c.islower() or c.isdigit() or c == "-" for c in bad) and bad and bad[0].islower()
