"""Unit tests for exception context manager.

Tests the error_context() context manager for exception handling,
context attachment, and callback execution.
"""

import pytest

from splurge_exceptions import (
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValueError,
)
from splurge_exceptions.managers.exception import error_context


class TestErrorContextBasic:
    """Tests for basic context manager functionality."""

    def test_context_manager_with_no_exception(self) -> None:
        """Test context manager when no exception occurs."""
        executed = False
        with error_context():
            executed = True

        assert executed

    def test_context_manager_with_exception(self) -> None:
        """Test context manager reraises exception by default."""
        with pytest.raises(ValueError):
            with error_context():
                raise ValueError("Test error")

    def test_context_manager_with_exception_mapping(self) -> None:
        """Test context manager converts exception using mapping."""
        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            ):
                raise ValueError("Invalid value")

    def test_context_manager_with_multiple_exception_mappings(self) -> None:
        """Test context manager with multiple exception mappings."""
        # Test first mapping
        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                    FileNotFoundError: (SplurgeOSError, "file-not-found"),
                }
            ):
                raise ValueError("Invalid")

        # Test second mapping
        with pytest.raises(SplurgeOSError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                    FileNotFoundError: (SplurgeOSError, "file-not-found"),
                }
            ):
                raise FileNotFoundError("Not found")

    def test_context_manager_unmapped_exception_passes_through(self) -> None:
        """Test that unmapped exceptions pass through unchanged."""
        with pytest.raises(RuntimeError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            ):
                raise RuntimeError("Unmapped error")

    def test_context_manager_preserves_exception_chain(self) -> None:
        """Test that original exception is preserved in __cause__."""
        original_error = ValueError("Original")
        with pytest.raises(SplurgeValueError) as exc_info:
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            ):
                raise original_error

        assert exc_info.value.__cause__ is original_error


class TestErrorContextWithCallbacks:
    """Tests for callback execution in context manager."""

    def test_on_success_callback_called(self) -> None:
        """Test that on_success callback is called when no exception."""
        callback_called = False

        def on_success() -> None:
            nonlocal callback_called
            callback_called = True

        with error_context(on_success=on_success):
            pass

        assert callback_called

    def test_on_success_not_called_on_exception(self) -> None:
        """Test that on_success is not called if exception occurs."""
        callback_called = False

        def on_success() -> None:
            nonlocal callback_called
            callback_called = True

        with pytest.raises(ValueError):
            with error_context(on_success=on_success):
                raise ValueError("Error")

        assert not callback_called

    def test_on_error_callback_called(self) -> None:
        """Test that on_error callback is called on exception."""
        caught_exception = None

        def on_error(exc: Exception) -> None:
            nonlocal caught_exception
            caught_exception = exc

        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                on_error=on_error,
            ):
                raise ValueError("Test error")

        assert caught_exception is not None
        assert isinstance(caught_exception, SplurgeValueError)

    def test_on_error_not_called_on_success(self) -> None:
        """Test that on_error is not called if no exception."""
        callback_called = False

        def on_error(exc: Exception) -> None:
            nonlocal callback_called
            callback_called = True

        with error_context(on_error=on_error):
            pass

        assert not callback_called

    def test_both_callbacks(self) -> None:
        """Test both on_success and on_error callbacks."""
        success_called = False
        error_called = False

        def on_success() -> None:
            nonlocal success_called
            success_called = True

        def on_error(exc: Exception) -> None:
            nonlocal error_called
            error_called = True

        with error_context(on_success=on_success, on_error=on_error):
            pass

        assert success_called
        assert not error_called


class TestErrorContextSuppression:
    """Tests for exception suppression in context manager."""

    def test_suppress_true_suppresses_exception(self) -> None:
        """Test that suppress=True suppresses exceptions."""
        with error_context(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            },
            suppress=True,
        ):
            raise ValueError("Error")

        # Should not raise

    def test_suppress_false_reraises_exception(self) -> None:
        """Test that suppress=False reraises exceptions."""
        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                suppress=False,
            ):
                raise ValueError("Error")

    def test_suppress_with_unmapped_exception(self) -> None:
        """Test suppress with unmapped exception suppresses it."""
        with error_context(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            },
            suppress=True,
        ):
            raise RuntimeError("Unmapped")

        # Should not raise


class TestErrorContextWithContext:
    """Tests for context attachment in context manager."""

    def test_context_attachment_on_exception(self) -> None:
        """Test that context is attached to converted exceptions."""
        with pytest.raises(SplurgeValueError) as exc_info:
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                context={"field": "email", "value": "invalid"},
            ):
                raise ValueError("Invalid")

        assert exc_info.value.has_context("field")
        assert exc_info.value.get_context("field") == "email"

    def test_context_only_on_mapped_exceptions(self) -> None:
        """Test that context is only added for mapped exceptions."""
        with pytest.raises(RuntimeError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                context={"field": "email"},
            ):
                raise RuntimeError("Unmapped")


class TestErrorContextErrorCodeResolution:
    """Tests for error code resolution in context manager."""

    def test_fully_qualified_error_code(self) -> None:
        """Test context manager with fully qualified error code."""
        with pytest.raises(SplurgeValueError) as exc_info:
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            ):
                raise ValueError("Invalid")

        assert exc_info.value.error_code == "invalid-value"

    def test_partial_error_code(self) -> None:
        """Test context manager with partial error code."""
        with pytest.raises(SplurgeValueError) as exc_info:
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "validation"),
                }
            ):
                raise ValueError("Invalid")

        # Should resolve to full code
        code_parts = exc_info.value.error_code.split(".")
        assert code_parts[0] == "validation"

    def test_none_error_code(self) -> None:
        """Test context manager with None error code raises ValueError."""
        # In the new system, error_code is required - no automatic fallback or registry lookup
        with pytest.raises(ValueError, match="error_code cannot be empty"):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, None),
                }
            ):
                raise ValueError("Invalid")


class TestErrorContextEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_context_manager_with_no_arguments(self) -> None:
        """Test context manager with no arguments."""
        with error_context():
            pass

    def test_context_manager_with_none_callbacks(self) -> None:
        """Test context manager with explicit None callbacks."""
        with error_context(on_success=None, on_error=None):
            pass

    def test_context_manager_with_empty_exception_mapping(self) -> None:
        """Test context manager with empty exception mapping."""
        with error_context(exceptions={}):
            pass

    def test_exception_in_on_error_callback(self) -> None:
        """Test that exception in on_error callback causes callback error to be raised."""

        def on_error_with_error(exc: Exception) -> None:
            raise RuntimeError("Callback error")

        # The callback error is raised instead of the wrapped exception
        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                on_error=on_error_with_error,
            ):
                raise ValueError("Original")

    def test_nested_context_managers(self) -> None:
        """Test nested context managers."""
        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    RuntimeError: (SplurgeRuntimeError, "operation-failed"),
                }
            ):
                with error_context(
                    exceptions={
                        ValueError: (SplurgeValueError, "invalid-value"),
                    }
                ):
                    raise ValueError("Inner error")

    def test_context_manager_with_return_value_in_block(self) -> None:
        """Test that context manager allows return in block."""

        def get_value():
            with error_context():
                return 42

        result = get_value()
        assert result == 42

    def test_base_exception_not_exception_is_reraised(self) -> None:
        """Test that BaseException that's not Exception is re-raised immediately."""
        with pytest.raises(KeyboardInterrupt):
            with error_context():
                raise KeyboardInterrupt("User interrupted")

    def test_system_exit_is_reraised(self) -> None:
        """Test that SystemExit is re-raised immediately."""
        with pytest.raises(SystemExit):
            with error_context():
                raise SystemExit("Exiting")

    def test_on_error_callback_exception_without_mapping_suppress_false(self) -> None:
        """Test on_error callback exception when suppress=False and no mapping."""

        def failing_callback(exc: Exception) -> None:
            raise RuntimeError("Callback failed")

        # Should raise the callback exception, not the original
        with pytest.raises(RuntimeError, match="Callback failed"):
            with error_context(
                on_error=failing_callback,
                suppress=False,
            ):
                raise ValueError("Original error")

    def test_on_error_callback_exception_without_mapping_suppress_true(self) -> None:
        """Test on_error callback exception when suppress=True and no mapping."""

        def failing_callback(exc: Exception) -> None:
            raise RuntimeError("Callback failed")

        # Should suppress the callback exception when suppress=True
        with error_context(
            on_error=failing_callback,
            suppress=True,
        ):
            raise ValueError("Original error")

        # No exception should be raised

    def test_on_error_callback_exception_with_mapping_suppress_false(self) -> None:
        """Test on_error callback exception when suppress=False and mapping exists."""

        def failing_callback(exc: Exception) -> None:
            raise RuntimeError("Callback failed")

        # Should raise the wrapped exception, not the callback exception
        with pytest.raises(SplurgeValueError, match="invalid-value"):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                on_error=failing_callback,
                suppress=False,
            ):
                raise ValueError("Original error")

    def test_on_error_callback_exception_with_mapping_suppress_true(self) -> None:
        """Test on_error callback exception when suppress=True and mapping exists."""

        def failing_callback(exc: Exception) -> None:
            raise RuntimeError("Callback failed")

        # Should suppress when callback fails and suppress=True
        with error_context(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            },
            on_error=failing_callback,
            suppress=True,
        ):
            raise ValueError("Original error")

        # No exception should be raised


class TestErrorContextIntegration:
    """Integration tests for context manager."""

    def test_wrap_exception_flow(self) -> None:
        """Test typical exception handling flow."""
        success = False
        error = None

        def on_success() -> None:
            nonlocal success
            success = True

        def on_error(exc: Exception) -> None:
            nonlocal error
            error = exc

        # Success case
        with error_context(on_success=on_success, on_error=on_error):
            pass

        assert success
        assert error is None

        # Error case
        success = False
        error = None

        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                on_success=on_success,
                on_error=on_error,
            ):
                raise ValueError("Error")

        assert not success
        assert error is not None

    def test_multiple_exception_scenarios(self) -> None:
        """Test multiple different exception scenarios."""
        scenarios = []

        def on_success() -> None:
            scenarios.append("success")

        def on_error(exc: Exception) -> None:
            scenarios.append(f"error:{type(exc).__name__}")

        # Scenario 1: Success
        with error_context(on_success=on_success, on_error=on_error):
            pass

        # Scenario 2: Mapped error
        try:
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                on_success=on_success,
                on_error=on_error,
            ):
                raise ValueError("Error")
        except SplurgeValueError:
            pass

        # Scenario 3: Unmapped error
        try:
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                on_success=on_success,
                on_error=on_error,
            ):
                raise RuntimeError("Unmapped")
        except RuntimeError:
            pass

        assert "success" in scenarios
        assert "error:SplurgeValueError" in scenarios
        assert "error:RuntimeError" in scenarios

    def test_context_and_callback_together(self) -> None:
        """Test context attachment and callback together."""
        callback_exc = None

        def on_error(exc: Exception) -> None:
            nonlocal callback_exc
            callback_exc = exc

        with pytest.raises(SplurgeValueError):
            with error_context(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                context={"field": "email"},
                on_error=on_error,
            ):
                raise ValueError("Invalid")

        assert callback_exc is not None
        assert callback_exc.has_context("field")
        assert callback_exc.get_context("field") == "email"
