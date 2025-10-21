# CLI Reference - Splurge Exceptions

Complete reference for Splurge Exceptions command-line interface.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Command Reference](#command-reference)
4. [Examples](#examples)
5. [Output Formats](#output-formats)
6. [Programmatic Usage](#programmatic-usage)

## Overview

The Splurge Exceptions CLI provides tools for:
- Browsing error codes
- Filtering codes by domain
- Generating documentation
- Exploring the error hierarchy

### Available Commands

| Command | Purpose |
|---------|---------|
| `show-code` | Display specific error code details |
| `list-codes` | List all error codes (with optional filtering) |
| `generate-docs` | Generate documentation for all codes |

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

### show-code

Display details for a specific error code.

**Usage:**
```bash
python -m splurge_exceptions show-code <error_code>
```

**Arguments:**
- `error_code` (string, required) - The error code to display (e.g., "validation.value.001")

**Output:**
- Error code
- Description
- Associated exception type
- Recovery suggestions

**Examples:**

Show a validation error code:
```bash
python -m splurge_exceptions show-code validation.value.001
```

Output:
```
Error Code: validation.value.001
Description: Invalid value provided
Exception Type: SplurgeValidationError
```

Show an OS error code:
```bash
python -m splurge_exceptions show-code os.file.001
```

Output:
```
Error Code: os.file.001
Description: File not found
Exception Type: SplurgeOSError
```

### list-codes

List all registered error codes with optional filtering.

**Usage:**
```bash
python -m splurge_exceptions list-codes [--domain DOMAIN]
```

**Arguments:**
- `--domain` (string, optional) - Filter by domain (e.g., "validation", "auth", "os")

**Output:**
- Formatted list of error codes
- Optional domain filtering
- Error type information

**Examples:**

List all error codes:
```bash
python -m splurge_exceptions list-codes
```

Output:
```
Error Codes:

Validation Errors:
  validation.value.001 - Invalid value provided
  validation.type.001 - Type mismatch
  validation.range.001 - Value out of range
  ...

Authentication Errors:
  auth.user.001 - User not found
  auth.token.001 - Invalid token
  ...

OS Errors:
  os.file.001 - File not found
  os.permission.001 - Permission denied
  ...
```

List codes in specific domain:
```bash
python -m splurge_exceptions list-codes --domain auth
```

Output:
```
Error Codes (domain: auth):

Authentication Errors:
  auth.user.001 - User not found
  auth.token.001 - Invalid token
  auth.expired.001 - Token expired
```

List codes in validation domain:
```bash
python -m splurge_exceptions list-codes --domain validation
```

Output:
```
Error Codes (domain: validation):

Validation Errors:
  validation.value.001 - Invalid value provided
  validation.type.001 - Type mismatch
  validation.range.001 - Value out of range
  validation.format.001 - Invalid format
  validation.email.001 - Invalid email
  validation.required.001 - Required field missing
```

### generate-docs

Generate comprehensive documentation for all error codes.

**Usage:**
```bash
python -m splurge_exceptions generate-docs [--format FORMAT]
```

**Arguments:**
- `--format` (string, optional) - Output format ("markdown", "json")
- Default format: "markdown"

**Output:**
- Complete documentation for all error codes
- Organized by domain and exception type
- Descriptions and recovery suggestions

**Examples:**

Generate Markdown documentation:
```bash
python -m splurge_exceptions generate-docs --format markdown
```

Output:
```
# Splurge Exceptions - Error Code Reference

## Validation Errors

### validation.value.001
- **Message**: Invalid value provided
- **Exception**: SplurgeValidationError
- **Severity**: MEDIUM
- **Recoverable**: Yes

### validation.type.001
- **Message**: Type mismatch
- **Exception**: SplurgeValidationError
- **Severity**: MEDIUM
- **Recoverable**: Yes

...
```

Generate JSON documentation:
```bash
python -m splurge_exceptions generate-docs --format json
```

Output:
```json
{
  "version": "2025.0.0",
  "error_codes": [
    {
      "code": "validation.value.001",
      "message": "Invalid value provided",
      "exception": "SplurgeValidationError",
      "domain": "validation",
      "category": "value",
      "severity": "MEDIUM",
      "recoverable": true
    },
    ...
  ]
}
```

## Examples

### Example 1: Find All Auth Error Codes

List all authentication error codes:
```bash
python -m splurge_exceptions list-codes --domain auth
```

Then examine a specific code:
```bash
python -m splurge_exceptions show-code auth.token.001
```

### Example 2: Generate Documentation

Create an error code reference document:
```bash
python -m splurge_exceptions generate-docs --format markdown > ERROR_CODES.md
```

This creates a complete reference of all error codes for your project documentation.

### Example 3: Export Error Codes to JSON

Export all codes for programmatic use:
```bash
python -m splurge_exceptions generate-docs --format json > error_codes.json
```

Then parse in your application:
```python
import json

with open("error_codes.json") as f:
    error_data = json.load(f)
    
for code_info in error_data["error_codes"]:
    print(f"{code_info['code']}: {code_info['message']}")
```

### Example 4: Search for Specific Error Type

Find all validation errors:
```bash
python -m splurge_exceptions list-codes --domain validation
```

Then show details for a specific error:
```bash
python -m splurge_exceptions show-code validation.email.001
```

### Example 5: Create Error Code Cheat Sheet

Generate documentation and save it:
```bash
python -m splurge_exceptions generate-docs --format markdown > docs/ERROR_CODES.md
```

Include in your project documentation for developers to reference.

## Output Formats

### Markdown Format

Used by `generate-docs --format markdown`:
- Headers for each domain
- Organized by exception type
- Clear formatting for readability
- Suitable for documentation sites

### JSON Format

Used by `generate-docs --format json`:
- Structured data format
- Programmatically parseable
- Includes all metadata
- Suitable for automation

### Text Format

Used by `show-code` and `list-codes`:
- Human-readable output
- Clear labeling
- Suitable for terminal viewing

## Programmatic Usage

### Using CLI Commands Programmatically

```python
from splurge_exceptions.cli import (
    cmd_show_code,
    cmd_list_codes,
    cmd_generate_docs,
)

# Show specific code
info = cmd_show_code("validation.value.001")
print(info)

# List codes
codes = cmd_list_codes()
print(codes)

# List codes in domain
auth_codes = cmd_list_codes(domain="auth")
print(auth_codes)

# Generate documentation
docs = cmd_generate_docs(format_type="markdown")
with open("ERROR_CODES.md", "w") as f:
    f.write(docs)
```

### Integrating with Your Application

```python
from splurge_exceptions.cli import cmd_list_codes, cmd_show_code

def display_error_help(error_code: str) -> None:
    """Display help for specific error code."""
    info = cmd_show_code(error_code)
    print(f"Help for {error_code}:")
    print(info)

def list_all_domains() -> None:
    """List all error codes organized by domain."""
    codes = cmd_list_codes()
    print(codes)

# Usage in error handling
try:
    some_operation()
except SplurgeValidationError as e:
    if "--help" in sys.argv:
        display_error_help(e.error_code)
    else:
        print(f"Error: {e}")
```

## Shell Integration

### Bash

Create a shell alias for easier access:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias splurge='python -m splurge_exceptions'

# Now you can use:
splurge list-codes --domain auth
splurge show-code validation.value.001
```

### Python REPL

Quick access in Python interpreter:

```python
>>> from splurge_exceptions.cli import cmd_list_codes, cmd_show_code
>>> print(cmd_list_codes(domain="validation"))
>>> print(cmd_show_code("validation.value.001"))
```

## Error Code Browsing Workflow

### 1. Find Error Code

```bash
# List all codes in a domain
python -m splurge_exceptions list-codes --domain validation
```

### 2. Get Details

```bash
# Show specific code details
python -m splurge_exceptions show-code validation.value.001
```

### 3. Generate Reference

```bash
# Create documentation
python -m splurge_exceptions generate-docs --format markdown > ERROR_CODES.md
```

## Tips & Best Practices

### Tip 1: Create a Helper Script

```bash
#!/bin/bash
# error_lookup.sh
if [ $# -eq 0 ]; then
    python -m splurge_exceptions list-codes
else
    python -m splurge_exceptions show-code "$1"
fi
```

Usage:
```bash
./error_lookup.sh                          # List all codes
./error_lookup.sh validation.value.001     # Show specific code
```

### Tip 2: Generate Documentation on Build

Add to your build pipeline:
```bash
python -m splurge_exceptions generate-docs --format markdown > docs/error_codes.md
```

### Tip 3: Integrate with IDE

Create IDE shortcuts to quickly look up error codes:
```python
# In IDE extension or plugin
error_code = selected_text  # Get selected error code
result = subprocess.run(
    ["python", "-m", "splurge_exceptions", "show-code", error_code],
    capture_output=True,
    text=True
)
show_popup(result.stdout)
```

## Troubleshooting

### Command Not Found

**Problem**: `python -m splurge_exceptions` not found

**Solution**: Ensure package is installed:
```bash
pip install splurge-exceptions
```

### Invalid Error Code

**Problem**: `show-code` returns no results

**Solution**: Check error code format (should be `domain.category.code`):
```bash
# List valid codes first
python -m splurge_exceptions list-codes

# Then use exact code format
python -m splurge_exceptions show-code validation.value.001
```

### Domain Filter Not Working

**Problem**: `list-codes --domain auth` returns nothing

**Solution**: Check domain name:
```bash
# List all codes to see valid domains
python -m splurge_exceptions list-codes
```

## See Also

- [API-REFERENCE.md](../api/API-REFERENCE.md) - Complete API documentation
- [README-DETAILS.md](../README-DETAILS.md) - Comprehensive feature documentation
- [CHANGELOG.md](../../CHANGELOG.md) - Version history
