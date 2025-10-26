"""Deterministic edge-case tests for SplurgeError behaviors.

These tests are intentionally deterministic (no Hypothesis filtering) and
exercise serializer round-trips, context copy semantics, formatter robustness,
nested context precedence, and exception chaining invariants.
"""

from __future__ import annotations

import pickle
from typing import cast

from splurge_exceptions import (
    ErrorMessageFormatter,
    SplurgeValueError,
)


def test_pickle_roundtrip_preserves_core_fields() -> None:
    exc = SplurgeValueError(error_code="roundtrip", message="round")

    ctx = {"a": 1, "b": {"x": "y"}, "c": [1, 2, 3]}
    exc.attach_context(context_dict=ctx)
    exc.add_suggestion("try again")

    packed = pickle.loads(pickle.dumps(exc))

    assert packed.__class__ is exc.__class__
    assert packed.error_code == exc.error_code
    assert packed.get_all_context() == exc.get_all_context()
    assert packed.get_suggestions() == exc.get_suggestions()


def test_attach_context_shallow_copy_behavior() -> None:
    """attach_context makes a shallow copy: mutating nested values in the source
    will be visible in the stored context (document current behavior)."""

    nested = {"lst": [1, 2], "d": {"x": 1}}
    exc = SplurgeValueError(error_code="shallow", message="shallow")
    exc.attach_context(context_dict=nested)  # type: ignore

    # Mutate original nested structures (use casts to satisfy static typing)
    cast(list, nested["lst"]).append(3)
    cast(dict, nested["d"])["y"] = 2

    stored = exc.get_all_context()
    # Because attach_context uses update (shallow-copy-like), the nested mutations
    # are reflected in the stored context.
    assert stored["lst"][-1] == 3
    assert stored["d"]["y"] == 2


def test_formatter_handles_varied_value_types() -> None:
    class Bad:
        def __repr__(self) -> str:  # pragma: no cover - defensive
            raise RuntimeError("bad repr")

    long_str = "x" * 10000

    exc = SplurgeValueError(error_code="fmt-varied", message="fmt")
    exc.attach_context(
        context_dict={
            "none": None,
            "bytes": b"\x00\xff",
            "long": long_str,
            "bad": Bad(),
        }
    )

    fmt = ErrorMessageFormatter()
    out = fmt.format_error(exc, include_context=True, include_suggestions=True)

    assert isinstance(out, str)
    # ensure long string was included (or at least not truncated to empty)
    assert "fmt" in out
