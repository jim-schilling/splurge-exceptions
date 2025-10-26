"""Additional property tests: formatter robustness, large contexts."""

from __future__ import annotations

from typing import Any

from hypothesis import given
from hypothesis import strategies as st

from splurge_exceptions import (
    ErrorMessageFormatter,
    SplurgeValueError,
)


def test_formatter_handles_bad_object_repr() -> None:
    """Formatter should not raise if a context value has a broken __repr__ or __str__."""

    class Bad:
        def __repr__(self) -> str:  # pragma: no cover - defensive
            raise RuntimeError("bad repr")

    exc = SplurgeValueError("msg", error_code="fmt-bad")
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

    exc = SplurgeValueError("big", error_code="large-context")
    exc.attach_context(key="nested", value=nested)

    fmt = ErrorMessageFormatter()
    out = fmt.format_error(exc, include_context=True)

    assert isinstance(out, str)
    # basic assertion that some part of nested structure appears
    assert "nested" in out
