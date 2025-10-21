# Splurge Exceptions - Complete Documentation Index

## 📚 Documentation Overview

This is the complete documentation library for Splurge Exceptions. Choose the document that best matches your needs.

---

## 🚀 Getting Started

### For New Users
👉 **Start here**: [README.md](README.md)
- 5-minute quick start
- Installation instructions  
- 4 basic usage examples
- Key features overview
- Exception types at a glance

### First-Time Setup
```bash
pip install splurge-exceptions
```

Then read: [README.md](README.md)

---

## 📖 Comprehensive Documentation

### Main Documentation: [README-DETAILS.md](docs/README-DETAILS.md)
Everything you need to know about Splurge Exceptions:
- ✅ All 9 exception types with examples
- ✅ 5 major features explained
- ✅ 3 real-world scenarios
- ✅ Advanced usage patterns
- ✅ Error codes reference
- ✅ Testing information
- ✅ Installation options

**Read this when**: Learning the full library capabilities

---

## 🔧 API Reference

### Complete API: [docs/api/API-REFERENCE.md](docs/api/API-REFERENCE.md)
Detailed technical documentation:
- ✅ All public classes and functions
- ✅ Complete method signatures
- ✅ Type hints and definitions
- ✅ Parameter descriptions
- ✅ Return value documentation
- ✅ Code examples for every function
- ✅ Best practices

**Read this when**: 
- Looking up a specific function
- Understanding parameter types
- Checking return values
- Learning API patterns

### Quick API Navigation
| Class/Function | Purpose |
|---|---|
| `SplurgeError` | Base exception class |
| `wrap_exception()` | Convert exceptions |
| `error_context()` | Context manager for errors |
| `handle_exceptions()` | Decorator for auto-conversion |
| `ErrorMessageFormatter` | Format error messages |
| `ErrorCodeRegistry` | Manage error codes |

---

## 💻 CLI Reference

### Command-Line Tools: [docs/cli/CLI-REFERENCE.md](docs/cli/CLI-REFERENCE.md)
Complete guide to CLI commands:
- ✅ `show-code` - Display error details
- ✅ `list-codes` - Browse error codes
- ✅ `generate-docs` - Create documentation
- ✅ Shell integration examples
- ✅ Programmatic usage examples
- ✅ Troubleshooting guide

**Read this when**:
- Using the command-line interface
- Integrating CLI with scripts
- Generating documentation
- Browsing error codes

### Quick CLI Commands
```bash
# Show specific error code
python -m splurge_exceptions show-code validation.value.001

# List all codes
python -m splurge_exceptions list-codes

# List codes in domain
python -m splurge_exceptions list-codes --domain auth

# Generate documentation
python -m splurge_exceptions generate-docs --format markdown
```

---

## 📝 Release Information

### Changelog: [CHANGELOG.md](CHANGELOG.md)
Version history and features:
- ✅ Current version: 2025.0.0
- ✅ All features added
- ✅ Testing metrics
- ✅ Code quality standards
- ✅ Compatibility info
- ✅ Future roadmap

**Read this when**:
- Checking what's new
- Understanding version changes
- Planning upgrades

---

## 🎯 Quick Reference by Use Case

### I want to...

#### Wrap an exception
**See**: [API-REFERENCE.md#wrap_exception](docs/api/API-REFERENCE.md#wrapping--conversion)
```python
from splurge_exceptions import wrap_exception, SplurgeValidationError

error = wrap_exception(
    ValueError("Invalid"),
    SplurgeValidationError,
    error_code="validation.value.001"
)
```

#### Use a context manager
**See**: [API-REFERENCE.md#error_context](docs/api/API-REFERENCE.md#context-managers)
```python
from splurge_exceptions import error_context, SplurgeValidationError

with error_context(
    exceptions={
        ValueError: (SplurgeValidationError, "validation.value.001"),
    },
):
    validate_input(data)
```

#### Use a decorator
**See**: [API-REFERENCE.md#handle_exceptions](docs/api/API-REFERENCE.md#decorators)
```python
from splurge_exceptions import handle_exceptions, SplurgeOSError

@handle_exceptions(
    exceptions={
        FileNotFoundError: (SplurgeOSError, "os.file.001"),
    }
)
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()
```

#### Format an error message
**See**: [API-REFERENCE.md#ErrorMessageFormatter](docs/api/API-REFERENCE.md#message-formatting)
```python
from splurge_exceptions import ErrorMessageFormatter

formatter = ErrorMessageFormatter()
message = formatter.format_error(
    error,
    include_context=True,
    include_suggestions=True
)
```

#### Browse error codes
**See**: [CLI-REFERENCE.md](docs/cli/CLI-REFERENCE.md)
```bash
python -m splurge_exceptions list-codes --domain validation
python -m splurge_exceptions show-code validation.value.001
```

#### Register custom error codes
**See**: [README-DETAILS.md#custom-error-codes](docs/README-DETAILS.md#custom-error-codes)
```python
from splurge_exceptions import get_global_registry, SplurgeValidationError

registry = get_global_registry()
registry.register_error_code(
    SplurgeValidationError,
    "billing.credit_card.001",
    "Invalid credit card number"
)
```

---

## 📊 Documentation Statistics

| Document | Lines | Size | Purpose |
|---|---|---|---|
| [README.md](README.md) | 146 | 4.2K | Quick start |
| [docs/README-DETAILS.md](docs/README-DETAILS.md) | 718 | 19K | Comprehensive guide |
| [docs/api/API-REFERENCE.md](docs/api/API-REFERENCE.md) | 791 | 21K | API documentation |
| [docs/cli/CLI-REFERENCE.md](docs/cli/CLI-REFERENCE.md) | 506 | 11K | CLI reference |
| [CHANGELOG.md](CHANGELOG.md) | 220 | 6.5K | Version history |
| **Total** | **2,381** | **61.7K** | **Complete documentation** |

---

## 🔍 Topic Index

### Exception Types
- [SplurgeError](docs/api/API-REFERENCE.md#splurgeerror)
- [SplurgeValidationError](docs/api/API-REFERENCE.md#splurgevalidationerror)
- [SplurgeOSError](docs/api/API-REFERENCE.md#splurgeoserror)
- [SplurgeConfigurationError](docs/api/API-REFERENCE.md#splurgeconfigurationerror)
- [SplurgeRuntimeError](docs/api/API-REFERENCE.md#splurgeruntimeerror)
- [SplurgeAuthenticationError](docs/api/API-REFERENCE.md#splurgeauthenticationerror)
- [SplurgeAuthorizationError](docs/api/API-REFERENCE.md#splurgeauthorizationerror)
- [SplurgeNotImplementedError](docs/api/API-REFERENCE.md#splurgenotimplementederror)
- [SplurgeFrameworkError](docs/api/API-REFERENCE.md#splurgeframeworkerror)

### Functions & Tools
- [wrap_exception()](docs/api/API-REFERENCE.md#wrap_exception)
- [error_context()](docs/api/API-REFERENCE.md#error_context)
- [handle_exceptions()](docs/api/API-REFERENCE.md#handle_exceptions)
- [ErrorMessageFormatter](docs/api/API-REFERENCE.md#errormessageformatter)
- [ErrorCodeRegistry](docs/api/API-REFERENCE.md#errorcoderegistry)

### CLI Commands
- [show-code](docs/cli/CLI-REFERENCE.md#show-code)
- [list-codes](docs/cli/CLI-REFERENCE.md#list-codes)
- [generate-docs](docs/cli/CLI-REFERENCE.md#generate-docs)

### Error Codes
- [Validation Domain](docs/README-DETAILS.md#validation-domain)
- [OS Domain](docs/README-DETAILS.md#os-domain)
- [Configuration Domain](docs/README-DETAILS.md#configuration-domain)
- [Authentication Domain](docs/README-DETAILS.md#authentication-domain)
- [Runtime Domain](docs/README-DETAILS.md#runtime-domain)

---

## 🧪 Testing & Quality

All documentation is backed by:
- ✅ **245 tests** - 100% pass rate
- ✅ **98% coverage** - Comprehensive testing
- ✅ **0 linting errors** - Clean code
- ✅ **0 type errors** - Full type safety

Run tests:
```bash
pytest tests/
pytest tests/ --cov=splurge_exceptions
```

---

## 📚 Related Documentation

### Internal Docs
- [STAGES-4-6-COMPLETION-REPORT.md](STAGES-4-6-COMPLETION-REPORT.md) - Implementation details
- [STAGES-4-6-SUMMARY.md](docs/STAGES-4-6-SUMMARY.md) - Feature summary
- [DOCUMENTATION-COMPLETE.md](DOCUMENTATION-COMPLETE.md) - Documentation status

### External Resources
- [GitHub Repository](https://github.com/jim-schilling/splurge-exceptions)
- [PyPI Package](https://pypi.org/project/splurge-exceptions/)

---

## 🆘 Getting Help

### Finding Answers

**Quick lookup**: Use Ctrl+F to search this index
**Specific question**: Check the Quick Reference by Use Case section
**API details**: See [docs/api/API-REFERENCE.md](docs/api/API-REFERENCE.md)
**CLI commands**: See [docs/cli/CLI-REFERENCE.md](docs/cli/CLI-REFERENCE.md)
**Examples**: See [docs/README-DETAILS.md](docs/README-DETAILS.md)

### Common Questions

**Q: How do I get started?**
A: Read [README.md](README.md)

**Q: How do I use exception wrapping?**
A: See [docs/README-DETAILS.md#exception-wrapping](docs/README-DETAILS.md#1-exception-wrapping)

**Q: What CLI commands are available?**
A: See [docs/cli/CLI-REFERENCE.md](docs/cli/CLI-REFERENCE.md)

**Q: Where are all the error codes?**
A: Run `python -m splurge_exceptions list-codes` or see [docs/README-DETAILS.md#error-codes](docs/README-DETAILS.md#error-codes)

**Q: How do I add custom error codes?**
A: See [docs/README-DETAILS.md#custom-error-codes](docs/README-DETAILS.md#custom-error-codes)

---

## 📋 Documentation Roadmap

- ✅ Quick-start guide (README.md)
- ✅ Comprehensive guide (README-DETAILS.md)
- ✅ Complete API reference (API-REFERENCE.md)
- ✅ CLI tools reference (CLI-REFERENCE.md)
- ✅ Release information (CHANGELOG.md)
- ✅ Documentation index (this file)

---

## 📞 Support

For issues, questions, or contributions:
- **GitHub**: https://github.com/jim-schilling/splurge-exceptions
- **License**: MIT

---

**Last Updated**: October 20, 2025  
**Version**: 2025.0.0  
**Status**: ✅ Complete
