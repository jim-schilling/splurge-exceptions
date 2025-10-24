"""Unit tests for core exception types.

DOMAINS: ["core", "exceptions"]
"""

from splurge_exceptions import (
    SplurgeAttributeError,
    SplurgeError,
    SplurgeFrameworkError,
    SplurgeImportError,
    SplurgeLookupError,
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeTypeError,
    SplurgeValueError,
)


class TestSplurgeValueError:
    """Test SplurgeValueError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeValueError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeValueError(
            error_code="invalid-value",
            message="Invalid value",
        )

        assert error.error_code == "invalid-value"
        assert error.full_code == "value.invalid-value"
        assert error.message == "Invalid value"
        assert error.domain == "value"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeValueError("invalid-input", message="Invalid")
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
            raise SplurgeOSError("file-error", message="File error")
        except SplurgeError:
            pass


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
            _domain = "dsv"

        error = SplurgeDsvError(
            error_code="parse-failed",
            message="Failed to parse DSV",
        )

        assert error.domain == "dsv"
        assert isinstance(error, SplurgeFrameworkError)
        assert isinstance(error, SplurgeError)


class TestSplurgeTypeError:
    """Test SplurgeTypeError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeTypeError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeTypeError(
            error_code="invalid-type",
            message="Invalid type provided",
        )

        assert error.error_code == "invalid-type"
        assert error.full_code == "type.invalid-type"
        assert error.message == "Invalid type provided"
        assert error.domain == "type"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeTypeError("type-mismatch", message="Type mismatch")
        except SplurgeError:
            pass


class TestSplurgeAttributeError:
    """Test SplurgeAttributeError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeAttributeError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeAttributeError(
            error_code="missing-attribute",
            message="Attribute does not exist",
        )

        assert error.error_code == "missing-attribute"
        assert error.full_code == "attribute.missing-attribute"
        assert error.message == "Attribute does not exist"
        assert error.domain == "attribute"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeAttributeError("attribute-not-found", message="Attribute not found")
        except SplurgeError:
            pass


class TestSplurgeImportError:
    """Test SplurgeImportError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeImportError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeImportError(
            error_code="module-not-found",
            message="Module could not be imported",
        )

        assert error.error_code == "module-not-found"
        assert error.full_code == "import.module-not-found"
        assert error.message == "Module could not be imported"
        assert error.domain == "import"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeImportError("import-failed", message="Import failed")
        except SplurgeError:
            pass


class TestSplurgeLookupError:
    """Test SplurgeLookupError."""

    def test_is_subclass_of_splurge_error(self) -> None:
        """Test that it's a subclass of SplurgeError."""
        assert issubclass(SplurgeLookupError, SplurgeError)

    def test_instantiation(self) -> None:
        """Test instantiation."""
        error = SplurgeLookupError(
            error_code="item-not-found",
            message="Item not found in collection",
        )

        assert error.error_code == "item-not-found"
        assert error.full_code == "lookup.item-not-found"
        assert error.message == "Item not found in collection"
        assert error.domain == "lookup"

    def test_can_catch_as_splurge_error(self) -> None:
        """Test catching as SplurgeError."""
        try:
            raise SplurgeLookupError("lookup-failed", message="Lookup failed")
        except SplurgeError:
            pass


class TestExceptionHierarchy:
    """Test exception hierarchy and inheritance."""

    def test_all_exceptions_inherit_from_splurge_error(self) -> None:
        """Test all core exceptions inherit from SplurgeError."""
        exception_classes = [
            SplurgeValueError,
            SplurgeOSError,
            SplurgeLookupError,
            SplurgeRuntimeError,
            SplurgeTypeError,
            SplurgeAttributeError,
            SplurgeImportError,
            SplurgeFrameworkError,
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, SplurgeError)

    def test_all_exceptions_inherit_from_exception(self) -> None:
        """Test all core exceptions inherit from Exception."""
        exception_classes = [
            SplurgeValueError,
            SplurgeOSError,
            SplurgeLookupError,
            SplurgeRuntimeError,
            SplurgeTypeError,
            SplurgeAttributeError,
            SplurgeImportError,
            SplurgeFrameworkError,
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, Exception)

    def test_context_management_inherited(self) -> None:
        """Test that context management is inherited."""
        error = SplurgeValueError("invalid-field", message="Invalid")
        error.attach_context(key="field", value="email")

        assert error.get_context("field") == "email"
        assert error.domain == "value"

    def test_suggestions_inherited(self) -> None:
        """Test that suggestions are inherited."""
        error = SplurgeOSError("file-error", message="File error")
        error.add_suggestion("Check file path")

        assert error.get_suggestions() == ["Check file path"]
        assert error.domain == "os"

    def test_type_error_inherited(self) -> None:
        """Test that type error is inherited."""
        error = SplurgeTypeError("type-error", message="Type error")
        error.add_suggestion("Check type")

        assert error.get_suggestions() == ["Check type"]
        assert error.domain == "type"

    def test_lookup_error_inherited(self) -> None:
        """Test that lookup error is inherited."""
        error = SplurgeLookupError("lookup-error", message="Lookup error")
        error.add_suggestion("Check lookup")

        assert error.get_suggestions() == ["Check lookup"]
        assert error.domain == "lookup"

    def test_runtime_error_inherited(self) -> None:
        """Test that runtime error is inherited."""
        error = SplurgeRuntimeError("runtime-error", message="Runtime error")
        error.add_suggestion("Check runtime")

        assert error.get_suggestions() == ["Check runtime"]
        assert error.domain == "runtime"

    def test_framework_error_inherited(self) -> None:
        """Test that framework error is inherited."""
        error = SplurgeFrameworkError("framework-error", message="Framework error")
        error.add_suggestion("Check framework")

        assert error.get_suggestions() == ["Check framework"]
        assert error.domain == "framework"


class TestCatchingBySpecificType:
    """Test catching exceptions by specific type."""

    def test_catch_value_error_specifically(self) -> None:
        """Test catching validation error by type."""
        caught = False

        try:
            raise SplurgeValueError("invalid-input", message="Invalid")
        except SplurgeValueError:
            caught = True

        assert caught is True

    def test_catch_os_error_specifically(self) -> None:
        """Test catching OS error by type."""
        caught = False

        try:
            raise SplurgeOSError("file-error", message="File error")
        except SplurgeOSError:
            caught = True

        assert caught is True

    def test_catch_lookup_error_specifically(self) -> None:
        """Test catching lookup error by type."""
        caught = False

        try:
            raise SplurgeLookupError("lookup-error", message="Lookup error")
        except SplurgeLookupError:
            caught = True

        assert caught is True

    def test_catch_type_error_specifically(self) -> None:
        """Test catching type error by type."""
        caught = False

        try:
            raise SplurgeTypeError("type-error", message="Type error")
        except SplurgeTypeError:
            caught = True

        assert caught is True

    def test_catch_runtime_error_specifically(self) -> None:
        """Test catching runtime error by type."""
        caught = False

        try:
            raise SplurgeRuntimeError("runtime-error", message="Runtime error")
        except SplurgeRuntimeError:
            caught = True

        assert caught is True

    def test_catch_framework_error_specifically(self) -> None:
        """Test catching framework error by type."""
        caught = False

        try:
            raise SplurgeFrameworkError("framework-error", message="Framework error")
        except SplurgeFrameworkError:
            caught = True

        assert caught is True

    def test_catch_attribute_error_specifically(self) -> None:
        """Test catching attribute error by type."""
        caught = False

        try:
            raise SplurgeAttributeError("attribute-error", message="Attribute error")
        except SplurgeAttributeError:
            caught = True

        assert caught is True

    def test_catch_import_error_specifically(self) -> None:
        """Test catching import error by type."""
        caught = False

        try:
            raise SplurgeImportError("import-error", message="Import error")
        except SplurgeImportError:
            caught = True

        assert caught is True

    def test_catch_generic_splurge_error(self) -> None:
        """Test catching all Splurge errors generically."""
        exception_types = [
            SplurgeValueError("invalid-data", message="Invalid"),
            SplurgeOSError("file-error", message="File error"),
            SplurgeLookupError("parse-error", message="Lookup error"),
            SplurgeTypeError("type-error", message="Type error"),
            SplurgeAttributeError("attribute-error", message="Attribute error"),
            SplurgeImportError("import-error", message="Import error"),
            SplurgeFrameworkError("framework-error", message="Framework error"),
            SplurgeRuntimeError("runtime-error", message="Runtime error"),
        ]

        for exc in exception_types:
            caught = False

            try:
                raise exc
            except SplurgeError:
                caught = True

            assert caught is True
