"""Unit tests for core exception types.

DOMAINS: ["core", "exceptions"]
"""

from splurge_exceptions import (
    SplurgeAuthenticationError,
    SplurgeAuthorizationError,
    SplurgeConfigurationError,
    SplurgeError,
    SplurgeFrameworkError,
    SplurgeNotImplementedError,
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValidationError,
)


class TestSplurgeValidationError:
    """Test SplurgeValidationError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeValidationError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeValidationError(
            error_code="invalid-value",
            message="Invalid value",
        )

        assert error.error_code == "invalid-value"
        assert error.full_code == "validation.invalid-value"
        assert error.message == "Invalid value"
        assert error.domain == "validation"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeValidationError("invalid-input", "Invalid")
        except SplurgeError:
            pass


class TestSplurgeOSError:
    """Test SplurgeOSError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeOSError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeOSError(
            error_code="file-not-found",
            message="File not found",
        )

        assert error.error_code == "file-not-found"
        assert error.message == "File not found"
        assert error.domain == "os"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeOSError("file-error", "File error")
        except SplurgeError:
            pass


class TestSplurgeConfigurationError:
    """Test SplurgeConfigurationError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeConfigurationError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeConfigurationError(
            error_code="parse-error",
            message="Invalid configuration",
        )

        assert error.error_code == "parse-error"
        assert error.message == "Invalid configuration"
        assert error.domain == "config"


class TestSplurgeRuntimeError:
    """Test SplurgeRuntimeError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeRuntimeError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeRuntimeError(
            error_code="operation-failed",
            message="Operation failed",
        )

        assert error.error_code == "operation-failed"
        assert error.message == "Operation failed"
        assert error.domain == "runtime"


class TestSplurgeAuthenticationError:
    """Test SplurgeAuthenticationError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeAuthenticationError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeAuthenticationError(
            error_code="invalid-credentials",
            message="Invalid credentials",
        )

        assert error.error_code == "invalid-credentials"
        assert error.message == "Invalid credentials"
        assert error.domain == "authentication"


class TestSplurgeAuthorizationError:
    """Test SplurgeAuthorizationError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeAuthorizationError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeAuthorizationError(
            error_code="access-denied",
            message="Access denied",
        )

        assert error.error_code == "access-denied"
        assert error.message == "Access denied"
        assert error.domain == "authorization"


class TestSplurgeNotImplementedError:
    """Test SplurgeNotImplementedError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeNotImplementedError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeNotImplementedError(
            error_code="not-implemented",
            message="Feature not implemented",
        )

        assert error.error_code == "not-implemented"
        assert error.message == "Feature not implemented"
        assert error.domain == "runtime"


class TestSplurgeFrameworkError:
    """Test SplurgeFrameworkError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeFrameworkError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeFrameworkError(
            error_code="framework-error",
            message="Framework error",
        )

        assert error.error_code == "framework-error"
        assert error.message == "Framework error"
        assert error.domain == "framework"

    def test_can_be_subclassed_for_custom_framework(self) -> None:
        """Test that it can be subclassed for custom frameworks."""

        class SplurgeDsvError(SplurgeFrameworkError):
            domain = "dsv"

        error = SplurgeDsvError(
            error_code="parse-failed",
            message="Failed to parse DSV",
        )

        assert error.domain == "dsv"
        assert isinstance(error, SplurgeFrameworkError)
        assert isinstance(error, SplurgeError)


class TestExceptionHierarchy:
    """Test exception hierarchy and inheritance."""

    def test_all_exceptions_inherit_from_splurge_error(self) -> None:
        """Test all core exceptions inherit from SplurgeError."""
        exception_classes = [
            SplurgeValidationError,
            SplurgeOSError,
            SplurgeConfigurationError,
            SplurgeRuntimeError,
            SplurgeAuthenticationError,
            SplurgeAuthorizationError,
            SplurgeNotImplementedError,
            SplurgeFrameworkError,
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, SplurgeError)

    def test_all_exceptions_inherit_from_exception(self) -> None:
        """Test all core exceptions inherit from Exception."""
        exception_classes = [
            SplurgeValidationError,
            SplurgeOSError,
            SplurgeConfigurationError,
            SplurgeRuntimeError,
            SplurgeAuthenticationError,
            SplurgeAuthorizationError,
            SplurgeNotImplementedError,
            SplurgeFrameworkError,
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, Exception)

    def test_context_management_inherited(self) -> None:
        """Test that context management is inherited."""
        error = SplurgeValidationError("invalid-field", "Invalid")
        error.attach_context(key="field", value="email")

        assert error.get_context("field") == "email"

    def test_suggestions_inherited(self) -> None:
        """Test that suggestions are inherited."""
        error = SplurgeOSError("file-error", "File error")
        error.add_suggestion("Check file path")

        assert error.get_suggestions() == ["Check file path"]


class TestCatchingBySpecificType:
    """Test catching exceptions by specific type."""

    def test_catch_validation_error_specifically(self) -> None:
        """Test catching validation error by type."""
        caught = False

        try:
            raise SplurgeValidationError("invalid-input", "Invalid")
        except SplurgeValidationError:
            caught = True

        assert caught is True

    def test_catch_os_error_specifically(self) -> None:
        """Test catching OS error by type."""
        caught = False

        try:
            raise SplurgeOSError("file-error", "File error")
        except SplurgeOSError:
            caught = True

        assert caught is True

    def test_catch_generic_splurge_error(self) -> None:
        """Test catching all Splurge errors generically."""
        exception_types = [
            SplurgeValidationError("invalid-data", "Invalid"),
            SplurgeOSError("file-error", "File error"),
            SplurgeConfigurationError("parse-error", "Config error"),
        ]

        for exc in exception_types:
            caught = False

            try:
                raise exc
            except SplurgeError:
                caught = True

            assert caught is True
