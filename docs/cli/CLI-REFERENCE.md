# CLI Reference - Splurge Exceptions

Complete reference for Splurge Exceptions command-line interface.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Command Reference](#command-reference)
4. [Examples](#examples)
5. [Programmatic Usage](#programmatic-usage)

## Overview

The Splurge Exceptions CLI provides basic information and version details for the library.

### Available Commands

| Command | Purpose |
|---------|---------|
| `--version` | Display version information |
| `--help` | Display help information |

## Installation

The CLI is included with the library installation:

```bash
pip install splurge-exceptions
```

After installation, the CLI is available as:
```bash
python -m splurge_exceptions <command>
```

## Command Reference

### --version

Display version information for the Splurge Exceptions library.

**Usage:**
```bash
python -m splurge_exceptions --version
```

**Output:**
```
splurge-exceptions 2025.1.0
```

### --help

Display help information and available options.

**Usage:**
```bash
python -m splurge_exceptions --help
```

**Output:**
```
usage: splurge-exceptions [-h] [--version]

Splurge Exceptions - Python exception framework

options:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
```

## Examples

### Example 1: Check Version

Get the current version of the Splurge Exceptions library:
```bash
python -m splurge_exceptions --version
```

Output:
```
splurge-exceptions 2025.1.0
```

### Example 2: Get Help

View available CLI options:
```bash
python -m splurge_exceptions --help
```

Output:
```
usage: splurge-exceptions [-h] [--version]

Splurge Exceptions - Python exception framework

options:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
```

## Programmatic Usage

### Using CLI Commands Programmatically

```python
from splurge_exceptions.cli import main

# Get version programmatically
exit_code = main(["--version"])

# Get help programmatically
exit_code = main(["--help"])
```

### Integrating with Your Application

```python
from splurge_exceptions.cli import main

def show_library_info():
    """Display library version and help information."""
    print("Splurge Exceptions Library Info:")
    print("-" * 40)

    print("Version:")
    main(["--version"])

    print("\nAvailable Options:")
    main(["--help"])

# Usage
show_library_info()
```

## Shell Integration

### Bash

Create a shell alias for easier access:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias splurge='python -m splurge_exceptions'

# Now you can use:
splurge --version
splurge --help
```

### Python REPL

Quick access in Python interpreter:

```python
>>> from splurge_exceptions.cli import main
>>> main(["--version"])
splurge-exceptions 2025.0.0
>>> main(["--help"])
usage: splurge-exceptions [-h] [--version]

Splurge Exceptions - Python exception framework

options:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
```

## Tips & Best Practices

### Tip 1: Check Version in Build Scripts

Use the CLI to verify library version in automated scripts:
```bash
#!/bin/bash
# verify_splurge_version.sh
echo "Checking Splurge Exceptions version..."
python -m splurge_exceptions --version
```

### Tip 2: Integrate with CI/CD

Add version checking to your CI pipeline:
```yaml
# In your CI configuration (e.g., GitHub Actions)
- name: Check Splurge Exceptions version
  run: python -m splurge_exceptions --version
```

### Tip 3: Use in Documentation Generation

Include version information in generated documentation:
```python
# docs/generate_version_info.py
import subprocess
import sys

def get_splurge_version():
    result = subprocess.run(
        [sys.executable, "-m", "splurge_exceptions", "--version"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# Use in documentation generation
version = get_splurge_version()
print(f"Splurge Exceptions Version: {version}")
```

## Troubleshooting

### Command Not Found

**Problem**: `python -m splurge_exceptions` not found

**Solution**: Ensure package is installed:
```bash
pip install splurge-exceptions
```

### Version Not Showing

**Problem**: `--version` doesn't display anything

**Solution**: Check if the package is properly installed:
```bash
pip show splurge-exceptions
```

### Help Not Working

**Problem**: `--help` returns an error

**Solution**: Verify Python module path:
```bash
python -c "import splurge_exceptions.cli; print('CLI module found')"
```

## See Also

- [API-REFERENCE.md](../api/API-REFERENCE.md) - Complete API documentation
- [README-DETAILS.md](../README-DETAILS.md) - Comprehensive feature documentation
- [CHANGELOG.md](../../CHANGELOG.md) - Version history
