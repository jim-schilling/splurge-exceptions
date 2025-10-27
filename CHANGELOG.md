# Changelog

All notable changes to Splurge Exceptions will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

## [2025.2.0] - 2025-10-27

### Updated
- Package version updated to `2025.2.0` in `splurge_exceptions/__init__.py`.
- Bumped version to `2025.2.0` in `pyproject.toml` for new release.

### Refactored
- **`full_code` property logic** in `SplurgeError` refined:
  - Now checks if `error_code` is part of `domain` before appending.
  - Returns just the domain if `error_code` is already included in it.

### Added
- Additional unit tests for `full_code` property covering new logic paths.

## [2025.1.0] - 2025-10-26

### Changed (BREAKING)
- **`SplurgeError` constructor signature completely redesigned** for v2.0:
  - OLD: `__init__(error_code, *, message=None, details=None)`
  - NEW: `__init__(message, error_code=None, details=None)`
  - Message is now **required positional argument** (was optional keyword-only)
  - Error code is now **optional keyword argument** (was required positional)
  - This fixes the design flaw where invalid error codes at construction time would mask the original error

### Added
- **Error code normalization** replaces validation:
  - Automatic lowercase conversion: `"InvalidCode"` → `"invalidcode"`
  - Symbol replacement: spaces/underscores/dots → dashes
  - Duplicate dash collapse: `"invalid---code"` → `"invalid-code"`
  - Edge dash stripping: `"-code-"` → `"code"`
  - Empty codes become `None` (no validation error raised)
- **34 comprehensive coverage gap tests** for edge cases and error paths
- **21 Hypothesis property-based tests** validating core exception properties across 2,100+ auto-generated test cases:
  - Core properties (message preservation, error code normalization)
  - Context and suggestion management
  - Message formatting consistency
  - Exception hierarchy and chaining
  - Full workflow integration tests
- **99% test coverage** with 102 total unit tests (81 example-based + 21 property-based)
- Complete documentation updates for all examples and API references

### Fixed
- **Critical design issue**: Error code validation errors now won't mask the original exception the user was trying to report
- **full_code property**: Now returns domain only (no error_code suffix) when error_code is None

### Updated
- All example files (examples/api_client_usage.py, examples/api_integrator_usage.py)
- All documentation files (README.md, docs/README-DETAILS.md, docs/api/API-REFERENCE.md, docs/cli/CLI-REFERENCE.md)
- CLI entry point in pyproject.toml: `run_cli` → `main`
- All docstring examples in core modules
- Test suite with fresh tests for new signature

### Removed
- 5 old test files that used the previous signature (replaced with fresh tests using new signature)

## [2025.0.1] - 2025-10-24

### Changed
- `SplurgeError` constructor signature updated to keyword-only arguments after `error_code`.
- Updated all relevant documentation (API reference, detailed README) to reflect all changes for this feature branch.

### Removed
- `recoverable` parameter from `SplurgeError` constructor.
- `is_recoverable()` property from `SplurgeError`.
- `_recoverable` internal attribute from `SplurgeError`.
- All references to recoverability in documentation.
- `wrap_exception()` has been removed from public API and documentation.

## [2025.0.0] - 2025-10-23

### Initial Release ✨

This is the inaugural release of Splurge Exceptions, a comprehensive Python exception management library.

#### Added

##### Core Exception Classes
- `SplurgeError` - Base exception class
- `SplurgeValueError` - Input validation errors
- `SplurgeOSError` - Operating system errors
- `SplurgeRuntimeError` - Runtime execution errors
- `SplurgeTypeError` - Type errors
- `SplurgeLookupError` - Lookup failures
- `SplurgeAttributeError` - For missing object attributes/methods (domain: "attribute")
- `SplurgeImportError` - For module import failures (domain: "import")
- `SplurgeFrameworkError` - Framework-level errors

##### Exception Features
- Semantic error codes (e.g., "invalid-value", "file-not-found")
- Context attachment with flexible data
- Recovery suggestions
- Severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Recoverability flags
- Full exception chaining support

##### Exception Management Tools

**Exception Wrapping** (`wrap_exception`)
- Convert any exception to Splurge exceptions
- Automatic error code resolution
- Context and suggestion attachment
- Preserves exception chains

**Context Manager** (`error_context`)
- Exception mapping and automatic conversion
- Context attachment to exceptions
- Callback support (on_success, on_error)
- Exception suppression capability
- Support for nested contexts

**Decorator** (`handle_exceptions`)
- Automatic exception conversion on decorated functions
- Configurable logging
- Optional exception re-raising
- Traceback inclusion control
- Works with methods, classmethods, staticmethods

**Message Formatter** (`ErrorMessageFormatter`)
- Multi-line structured error output
- Optional context and suggestions display
- Proper formatting with indentation
- Unicode and special character support

##### Error Code Management
- Semantic error code system with domain prefix and hyphenated names
- Custom error codes via explicit parameters
- User-defined domain support
- Support for custom exception hierarchies

##### Public API
- Clean, type-safe API
- 17 public exports
- Full type annotations
- Google-style docstrings
- Domain organization (`__domains__`)

##### Documentation
- Comprehensive README.md with quick-start
- Detailed README-DETAILS.md with features and examples
- Complete API-REFERENCE.md with all methods
- Hypothesis property-based testing documentation (HYPOTHESIS_TESTING.md)
- Inline code documentation and examples

##### Testing
- 168 example-based unit tests across 8 test suites
- 27 hypothesis property-based tests with custom strategies
- 195 total tests with 100% pass rate
- 100% code coverage (tested components)
- 2,700+ automatically generated test scenarios via hypothesis
- Comprehensive test scenarios:
  - Basic functionality
  - Edge cases
  - Integration scenarios
  - Error conditions
  - Complex workflows
  - Property-based invariant testing

##### Code Quality
- Full type annotations with MyPy strict mode
- Ruff linting with 0 errors
- PEP 8 compliance
- Automatic exception chaining
- Consistent error handling patterns

##### Project Structure
- Well-organized package layout
- Modular architecture:
  - `core/` - Base exceptions and error codes
  - `wrappers/` - Exception conversion utilities
  - `decorators/` - Function decorators
  - `managers/` - Context managers
  - `formatting/` - Message formatting
  - `cli.py` - Command-line interface
- Comprehensive test suite organization
- Documentation hierarchy

##### Development Standards
- MIT License
- Calendar versioning (YYYY.0.0)
- Git version control
- Development ready with editable install
- Build system: pyproject.toml
- Python 3.10+ compatibility

#### Features

**Exception Hierarchy**
- 9 specialized exception types
- Clear error domain organization
- Automatic inheritance chain
- Backward-compatible with standard exceptions

**Error Code Organization**
- Semantic format: `domain-error-code` (e.g., "database.sql-syntax-error")
- User-specified codes with domain prefix (e.g., "database", "os", "framework")
- Support for domain hierarchies
- No automatic registry lookups

**Integration Patterns**
- Explicit wrapping via `wrap_exception()`
- Decorator-based via `@handle_exceptions`
- Context manager-based via `error_context()`

**Message Formatting**
- Structured multi-line output
- Optional context inclusion
- Optional suggestions inclusion
- Unicode-safe formatting
- Proper indentation and formatting

**Type Safety**
- Full type annotations on public API
- MyPy strict mode compatible
- Generic type support
- Protocol definitions where appropriate

#### Performance
- Test suite: 195 tests in 2.73 seconds
- Unit tests: 168 example-based tests in ~1.94 seconds
- Property tests: 27 hypothesis tests in ~0.79 seconds
- Zero performance overhead for exception creation
- Minimal memory footprint

#### Compatibility
- Python 3.10+
- No external runtime dependencies
- Optional development dependencies:
  - pytest for testing
  - mypy for type checking
  - ruff for linting

### Documentation

- Quick-start guide in README.md
- Comprehensive feature documentation in README-DETAILS.md
- Complete API reference in docs/api/API-REFERENCE.md
- Property-based testing guide in tests/unit/HYPOTHESIS_TESTING.md
- Inline code documentation with examples
- Type hints as inline documentation

### Testing

- 195 tests (100% pass rate)
- 100% code coverage (tested components)
- Composition: 168 example-based + 27 hypothesis property-based tests
- All edge cases covered
- Integration scenarios validated
- Property-based invariants validated with 2,700+ generated scenarios
- Code quality checks passed:
  - Ruff: 0 errors
  - MyPy strict: 0 errors

### Known Limitations

None known in initial release.

### Future Roadmap

Potential features for future releases:
- Async error handling utilities
- Error aggregation and batching
- Custom formatter plugins
- Web dashboard for error browsing
- Error telemetry and monitoring
- Multi-language support for messages

---

## Version Information

- **Release Date**: October 20, 2025
- **Version**: 2025.0.0
- **Status**: Stable
- **License**: MIT
- **Author**: Jim Schilling
- **Repository**: https://github.com/jim-schilling/splurge-exceptions
