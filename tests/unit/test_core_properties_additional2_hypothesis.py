"""Additional property tests: nested contexts, wrapping cause, formatter robustness, large contexts."""

from __future__ import annotations

from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from splurge_exceptions import (
    ErrorMessageFormatter,
    SplurgeValueError,
    error_context,
    wrap_exception,
)


def test_nested_error_context_precedence() -> None:
    """Inner error_context should override outer context keys for the raised exception."""

    caught: SplurgeValueError | None = None

    try:
        with error_context(exceptions={ValueError: (SplurgeValueError, "code")}, context={"k": "outer"}):
            with error_context(exceptions={ValueError: (SplurgeValueError, "code")}, context={"k": "inner"}):
                raise ValueError("boom")
    except SplurgeValueError as e:
        caught = e

    assert caught is not None
    # inner context should take precedence
    assert caught.get_context("k") == "inner"


def test_wrap_exception_preserves_cause() -> None:
    """wrap_exception should set __cause__ to the original exception."""

    orig = ValueError("original")
    wrapped = wrap_exception(orig, SplurgeValueError, error_code="wrapped")

    assert wrapped.__cause__ is orig


def test_formatter_handles_bad_object_repr() -> None:
    """Formatter should not raise if a context value has a broken __repr__ or __str__."""

    class Bad:
        def __repr__(self) -> str:  # pragma: no cover - defensive
            raise RuntimeError("bad repr")

    exc = SplurgeValueError(error_code="fmt-bad", message="msg")
    exc.attach_context(key="bad", value=Bad())

    fmt = ErrorMessageFormatter()

    # Should not raise; return a string. We accept any string result.
    out = fmt.format_error(exc, include_context=True)
    assert isinstance(out, str)


@given(n=st.integers(min_value=1, max_value=200))
def test_large_and_deep_contexts(n: int) -> None:
    """Large and deep nested context values should be handled by formatter without error."""

    # Build a nested dict of depth n
    nested: dict[str, Any] = {}
    curr = nested
    for i in range(n):
        curr["k"] = {"i": i}
        curr = curr["k"]

    exc = SplurgeValueError(error_code="large-context", message="big")
    exc.attach_context(key="nested", value=nested)

    fmt = ErrorMessageFormatter()
    out = fmt.format_error(exc, include_context=True)

    assert isinstance(out, str)
    # basic assertion that some part of nested structure appears
    assert "nested" in out
