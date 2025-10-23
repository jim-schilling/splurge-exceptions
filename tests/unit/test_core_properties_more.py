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
    error_context,
    wrap_exception,
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


def test_nested_context_precedence_variations() -> None:
    # scenario 1: outer provides dict, inner provides scalar -> inner wins
    caught = None
    try:
        with error_context(exceptions={ValueError: (SplurgeValueError, "c1")}, context={"k": {"v": "outer"}}):
            with error_context(exceptions={ValueError: (SplurgeValueError, "c1")}, context={"k": "inner"}):
                raise ValueError("x")
    except SplurgeValueError as e:
        caught = e

    assert caught is not None
    assert caught.get_context("k") == "inner"

    # scenario 2: outer scalar, inner dict -> inner wins
    caught = None
    try:
        with error_context(exceptions={ValueError: (SplurgeValueError, "c2")}, context={"k": "outer"}):
            with error_context(exceptions={ValueError: (SplurgeValueError, "c2")}, context={"k": {"v": "inner"}}):
                raise ValueError("x")
    except SplurgeValueError as e:
        caught = e

    assert caught is not None
    assert isinstance(caught.get_context("k"), dict)
    assert caught.get_context("k")["v"] == "inner"


def test_nested_dict_vs_dict_replaces_outer() -> None:
    """When both outer and inner contexts provide dict values for the same
    key, the inner dict should replace the outer dict (no deep/recursive
    merge)."""

    caught = None
    try:
        with error_context(exceptions={ValueError: (SplurgeValueError, "c3")}, context={"k": {"a": 1}}):
            with error_context(exceptions={ValueError: (SplurgeValueError, "c3")}, context={"k": {"b": 2}}):
                raise ValueError("x")
    except SplurgeValueError as e:
        caught = e

    assert caught is not None
    val = caught.get_context("k")
    # Should be the inner dict only (replace semantics)
    assert isinstance(val, dict)
    assert "b" in val and val["b"] == 2
    assert "a" not in val


def test_exception_chaining_and_raise_from_semantics() -> None:
    orig = ValueError("orig")
    wrapped = wrap_exception(orig, SplurgeValueError, error_code="wrapped")
    # wrap_exception sets __cause__ to the original exception
    assert wrapped.__cause__ is orig

    # raising wrapped from orig should preserve cause identity when caught
    try:
        try:
            raise orig
        except ValueError as e:
            wrapped2 = wrap_exception(e, SplurgeValueError, error_code="wrapped2")
            raise wrapped2 from e
    except SplurgeValueError as ex:
        # The cause should be the original ValueError instance
        assert ex.__cause__ is orig
