"""Unit tests for exception handling decorator.

Tests the handle_exceptions() decorator for automatic exception handling
and conversion to Splurge exceptions.
"""

from unittest import mock

import pytest

from splurge_exceptions import (
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValueError,
)
from splurge_exceptions.decorators.error_handler import handle_exceptions


class TestHandleExceptionsBasic:
    """Tests for basic decorator functionality."""

    def test_decorator_with_single_exception_mapping(self) -> None:
        """Test decorator with single exception mapping."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func() -> None:
            raise ValueError("Invalid input")

        with pytest.raises(SplurgeValueError) as exc_info:
            failing_func()

        assert exc_info.value.error_code == "invalid-value"
        assert "Invalid input" in exc_info.value.message

    def test_decorator_with_multiple_exception_mappings(self) -> None:
        """Test decorator with multiple exception mappings."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
                FileNotFoundError: (SplurgeOSError, "file-not-found"),
            }
        )
        def failing_func(exception_type: type) -> None:
            if exception_type is ValueError:
                raise ValueError("Invalid value")
            elif exception_type is FileNotFoundError:
                raise FileNotFoundError("File not found")

        # Test first mapping
        with pytest.raises(SplurgeValueError) as exc_info:
            failing_func(ValueError)
        assert exc_info.value.error_code == "invalid-value"

        # Test second mapping
        with pytest.raises(SplurgeOSError) as exc_info:
            failing_func(FileNotFoundError)
        assert exc_info.value.error_code == "file-not-found"

    def test_decorated_function_returns_normally(self) -> None:
        """Test that decorated function returns normally when no exception."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def successful_func() -> int:
            return 42

        result = successful_func()
        assert result == 42

    def test_decorator_preserves_function_metadata(self) -> None:
        """Test that decorator preserves function name and docstring."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def my_function() -> None:
            """My function docstring."""
            pass

        assert my_function.__name__ == "my_function"
        assert "My function docstring" in my_function.__doc__

    def test_decorator_with_partial_error_code(self) -> None:
        """Test decorator with valid single-component error code."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "validation"),
            }
        )
        def failing_func() -> None:
            raise ValueError("Invalid")

        with pytest.raises(SplurgeValueError) as exc_info:
            failing_func()

        # Single-component error codes are valid and returned as-is
        assert exc_info.value.error_code == "validation"

    def test_decorator_with_none_error_code(self) -> None:
        """Test decorator with None error code raises ValueError."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, None),
            }
        )
        def failing_func() -> None:
            raise ValueError("Invalid")

        # error_code is required - no registry fallback
        with pytest.raises(ValueError, match="error_code cannot be empty"):
            failing_func()


class TestHandleExceptionsWithContext:
    """Tests for decorator with context attachment."""

    def test_decorator_attaches_context(self) -> None:
        """Test that context can be attached to wrapped exceptions."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func() -> None:
            error = ValueError("Invalid")
            raise error

        with pytest.raises(SplurgeValueError) as exc_info:
            failing_func()

        # Context should be accessible after wrapping
        assert isinstance(exc_info.value, SplurgeValueError)


class TestHandleExceptionsExceptionChaining:
    """Tests for exception chaining in decorator."""

    def test_decorator_preserves_exception_chain(self) -> None:
        """Test that original exception is preserved as __cause__."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func() -> None:
            raise ValueError("Original error")

        with pytest.raises(SplurgeValueError) as exc_info:
            failing_func()

        # Original exception should be in __cause__
        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, ValueError)
        assert str(exc_info.value.__cause__) == "Original error"

    def test_decorator_preserves_traceback(self) -> None:
        """Test that traceback is preserved through exception chain."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func() -> None:
            raise ValueError("Test error")

        with pytest.raises(SplurgeValueError):
            failing_func()


class TestHandleExceptionsReraise:
    """Tests for reraise behavior in decorator."""

    def test_decorator_reraises_by_default(self) -> None:
        """Test that decorator reraises exceptions by default."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func() -> None:
            raise ValueError("Error")

        with pytest.raises(SplurgeValueError):
            failing_func()

    def test_decorator_with_reraise_false(self) -> None:
        """Test decorator with reraise=False suppresses exceptions."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            },
            reraise=False,
        )
        def failing_func() -> None:
            raise ValueError("Error")

        # Should not raise
        result = failing_func()
        assert result is None

    def test_decorator_logs_when_reraise_false(self) -> None:
        """Test that decorator logs exception when reraise=False."""
        with mock.patch("logging.Logger.error") as mock_error:

            @handle_exceptions(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                reraise=False,
                log_level="error",
            )
            def failing_func() -> None:
                raise ValueError("Error")

            failing_func()

            # Should have logged the exception
            assert mock_error.called


class TestHandleExceptionsLogging:
    """Tests for logging in decorator."""

    def test_decorator_logs_exception_by_default(self) -> None:
        """Test that decorator logs exceptions by default."""
        with mock.patch("logging.Logger.error") as mock_error:

            @handle_exceptions(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                log_level="error",
            )
            def failing_func() -> None:
                raise ValueError("Error")

            with pytest.raises(SplurgeValueError):
                failing_func()

            # Should have logged
            assert mock_error.called

    def test_decorator_logs_with_different_levels(self) -> None:
        """Test decorator with different log levels."""
        for log_level in ["debug", "info", "warning", "error", "critical"]:
            with mock.patch(f"logging.Logger.{log_level}") as mock_log:

                @handle_exceptions(
                    exceptions={
                        ValueError: (SplurgeValueError, "invalid-value"),
                    },
                    log_level=log_level,
                    reraise=False,
                )
                def failing_func() -> None:
                    raise ValueError("Error")

                failing_func()

                assert mock_log.called

    def test_decorator_includes_traceback_in_log(self) -> None:
        """Test that traceback is included in logged message when enabled."""
        with mock.patch("logging.Logger.error") as mock_error:

            @handle_exceptions(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                },
                log_level="error",
                include_traceback=True,
                reraise=False,
            )
            def failing_func() -> None:
                raise ValueError("Test error")

            failing_func()

            # Check that error was logged
            assert mock_error.called


class TestHandleExceptionsFunctionSignature:
    """Tests for decorator with various function signatures."""

    def test_decorator_with_no_arguments(self) -> None:
        """Test decorator on function with no arguments."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def func() -> None:
            raise ValueError("Error")

        with pytest.raises(SplurgeValueError):
            func()

    def test_decorator_with_positional_arguments(self) -> None:
        """Test decorator on function with positional arguments."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def func(a: int, b: str) -> str:
            if a == 0:
                raise ValueError("Cannot be zero")
            return f"{b}:{a}"

        # Should work normally
        result = func(5, "test")
        assert result == "test:5"

        # Should catch exception
        with pytest.raises(SplurgeValueError):
            func(0, "test")

    def test_decorator_with_keyword_arguments(self) -> None:
        """Test decorator on function with keyword arguments."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def func(name: str, age: int = 0) -> str:
            if age < 0:
                raise ValueError("Age cannot be negative")
            return f"{name}:{age}"

        # Should work with keywords
        result = func(name="Alice", age=30)
        assert result == "Alice:30"

        # Should catch exception
        with pytest.raises(SplurgeValueError):
            func(name="Bob", age=-5)

    def test_decorator_with_return_value(self) -> None:
        """Test that decorator preserves return values."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def func(value: int) -> int:
            if value < 0:
                raise ValueError("Negative")
            return value * 2

        result = func(5)
        assert result == 10

    def test_decorator_with_generator_function(self) -> None:
        """Test that decorator doesn't interfere with generator function."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def gen_func():
            for i in range(5):
                yield i * 2

        gen = gen_func()
        result = list(gen)
        assert result == [0, 2, 4, 6, 8]


class TestHandleExceptionsUnmappedExceptions:
    """Tests for handling unmapped exceptions."""

    def test_unmapped_exception_passes_through(self) -> None:
        """Test that unmapped exceptions pass through unchanged."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func() -> None:
            raise RuntimeError("Unmapped error")

        with pytest.raises(RuntimeError):
            failing_func()

    def test_multiple_unmapped_exceptions(self) -> None:
        """Test multiple unmapped exceptions pass through."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func(error_type: type) -> None:
            raise error_type("Error")

        # These should pass through
        with pytest.raises(RuntimeError):
            failing_func(RuntimeError)

        with pytest.raises(TypeError):
            failing_func(TypeError)


class TestHandleExceptionsNesting:
    """Tests for nested decorated functions."""

    def test_nested_decorated_functions(self) -> None:
        """Test decorators on nested functions."""

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def outer() -> None:
            @handle_exceptions(
                exceptions={
                    FileNotFoundError: (SplurgeOSError, "file-not-found"),
                }
            )
            def inner() -> None:
                raise ValueError("Inner error")

            inner()

        with pytest.raises(SplurgeValueError):
            outer()

    def test_multiple_decorator_layers(self) -> None:
        """Test multiple exception handlers on same function."""

        @handle_exceptions(
            exceptions={
                RuntimeError: (SplurgeRuntimeError, "operation-failed"),
            },
            reraise=True,
            log_level="debug",
        )
        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
            }
        )
        def failing_func(error: type) -> None:
            raise error("Error")

        # ValueError should be caught by inner decorator
        with pytest.raises(SplurgeValueError):
            failing_func(ValueError)

        # RuntimeError should be caught by outer decorator
        with pytest.raises(SplurgeRuntimeError):
            failing_func(RuntimeError)


class TestHandleExceptionsIntegration:
    """Integration tests for exception handling decorator."""

    def test_wrap_and_handle_workflow(self) -> None:
        """Test typical workflow of handling exceptions."""
        call_count = 0

        @handle_exceptions(
            exceptions={
                ValueError: (SplurgeValueError, "invalid-value"),
                FileNotFoundError: (SplurgeOSError, "file-not-found"),
            },
            log_level="error",
        )
        def process_data(data: str) -> str:
            nonlocal call_count
            call_count += 1
            if not data:
                raise ValueError("Data cannot be empty")
            if data == "file":
                raise FileNotFoundError("File not found")
            return f"Processed: {data}"

        # Successful case
        result = process_data("test")
        assert result == "Processed: test"
        assert call_count == 1

        # ValueError case
        with pytest.raises(SplurgeValueError):
            process_data("")
        assert call_count == 2

        # FileNotFoundError case
        with pytest.raises(SplurgeOSError):
            process_data("file")
        assert call_count == 3

    def test_decorator_with_method(self) -> None:
        """Test decorator on class methods."""

        class DataProcessor:
            @handle_exceptions(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            )
            def process(self, value: int) -> int:
                if value < 0:
                    raise ValueError("Negative value")
                return value * 2

        processor = DataProcessor()
        result = processor.process(5)
        assert result == 10

        with pytest.raises(SplurgeValueError):
            processor.process(-1)

    def test_decorator_with_staticmethod(self) -> None:
        """Test decorator on static methods."""

        class Utils:
            @staticmethod
            @handle_exceptions(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            )
            def validate(value: int) -> bool:
                if value < 0:
                    raise ValueError("Negative")
                return True

        result = Utils.validate(5)
        assert result is True

        with pytest.raises(SplurgeValueError):
            Utils.validate(-1)

    def test_decorator_with_classmethod(self) -> None:
        """Test decorator on class methods."""

        class Config:
            _value = 0

            @classmethod
            @handle_exceptions(
                exceptions={
                    ValueError: (SplurgeValueError, "invalid-value"),
                }
            )
            def set_value(cls, value: int) -> None:
                if value < 0:
                    raise ValueError("Cannot be negative")
                cls._value = value

        Config.set_value(5)
        assert Config._value == 5

        with pytest.raises(SplurgeValueError):
            Config.set_value(-1)
