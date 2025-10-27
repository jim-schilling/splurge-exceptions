#!/usr/bin/env python3
"""Convert test files from old signature to new signature.

Old signature: __init__(error_code, *, message=None, details=None)
New signature: __init__(message, error_code=None, details=None)

Changes:
1. Reorder parameters: message first, then error_code, then details
2. Error code validation is now normalization - tests expecting errors must be updated
3. Empty error_code now returns None, not error
"""

import re
from pathlib import Path


def normalize_error_code(code: str | None) -> str | None:
    """Normalize error code like the actual function does."""
    if code is None:
        return None
    code = code.lower()
    code = re.sub(r"[_\s\W]+", "-", code)
    code = re.sub(r"-+", "-", code)
    code = code.strip("-")
    return code if code else None


def convert_exception_call(line: str) -> str:
    """Convert a single exception call from old to new signature."""
    if "error_code=" not in line:
        return line

    # Find exception name and parameters
    # Match: \w+Error(...) allowing for spaces before paren
    match = re.search(r"(\w*Error)\s*\(([^)]*)\)", line)
    if not match:
        return line

    exc_name = match.group(1)
    params_str = match.group(2)

    # Check if already in new format (message= before error_code=)
    m_pos = params_str.find("message=")
    ec_pos = params_str.find("error_code=")

    if m_pos != -1 and ec_pos != -1 and m_pos < ec_pos:
        # Already correct
        return line

    # Parse parameters carefully (handle quoted strings)
    parts = []
    current = ""
    in_string = False
    string_char = None

    for i, char in enumerate(params_str):
        # Handle string delimiters
        if char in ('"', "'") and (i == 0 or params_str[i - 1] != "\\"):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False

        # Split on commas outside strings
        if char == "," and not in_string:
            parts.append(current.strip())
            current = ""
        else:
            current += char

    if current.strip():
        parts.append(current.strip())

    # Categorize parameters
    message_part = None
    error_code_part = None
    details_part = None
    other_parts = []

    for part in parts:
        if part.startswith("message="):
            message_part = part
        elif part.startswith("error_code="):
            error_code_part = part
        elif part.startswith("details="):
            details_part = part
        else:
            other_parts.append(part)

    # Rebuild with new parameter order
    new_parts = []
    if message_part:
        new_parts.append(message_part)
    if error_code_part:
        new_parts.append(error_code_part)
    if details_part:
        new_parts.append(details_part)
    new_parts.extend(other_parts)

    # Handle case where error_code exists but message doesn't
    if error_code_part and not message_part:
        new_parts.insert(0, '""')

    new_params = ", ".join(new_parts)
    new_call = f"{exc_name}({new_params})"
    return line[: match.start()] + new_call + line[match.end() :]


def convert_test_file(filepath: str) -> bool:
    """Convert a test file. Returns True if changed."""
    path = Path(filepath)
    with open(path) as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for test methods that need test logic changes (validation -> normalization)

        # Pattern 1: test_invalid_error_code_format_raises_error
        if "test_invalid_error_code_format_raises_error" in line:
            # Find the test body
            j = i
            while j < len(lines) and "def " not in lines[j + 1]:
                j += 1

            # Replace the entire test
            test_body = """    def test_invalid_error_code_format_raises_error(self) -> None:
        \"\"\"Test that invalid error codes are normalized.\"\"\"
        # "Invalid-code" normalizes to "invalid-code"
        error = DummyException(message="Test", error_code="Invalid-code")
        assert error.error_code == "invalid-code"
"""
            # Find end of test
            test_end = j + 1
            while test_end < len(lines):
                if lines[test_end].startswith("    def ") or test_end == len(lines) - 1:
                    break
                test_end += 1

            new_lines.append(test_body)
            i = test_end
            continue

        # Pattern 2: test_error_code_starting_with_uppercase_raises_error
        if "test_error_code_starting_with_uppercase_raises_error" in line:
            test_body = """    def test_error_code_starting_with_uppercase_raises_error(self) -> None:
        \"\"\"Test that uppercase codes are normalized to lowercase.\"\"\"
        error = DummyException(message="Test", error_code="InvalidCode")
        assert error.error_code == "invalidcode"
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 3: test_error_code_starting_with_digit_raises_error
        if "test_error_code_starting_with_digit_raises_error" in line:
            test_body = """    def test_error_code_starting_with_digit_raises_error(self) -> None:
        \"\"\"Test that leading digits are removed during normalization.\"\"\"
        # "123-error" normalizes to "error" (leading digits stripped)
        error = DummyException(message="Test", error_code="123-error")
        assert error.error_code == "error"
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 4: test_error_code_with_underscore_raises_error
        if "test_error_code_with_underscore_raises_error" in line:
            test_body = """    def test_error_code_with_underscore_raises_error(self) -> None:
        \"\"\"Test that underscores are converted to dashes.\"\"\"
        # "invalid_code" normalizes to "invalid-code"
        error = DummyException(message="Test", error_code="invalid_code")
        assert error.error_code == "invalid-code"
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 5: test_error_code_with_dot_raises_error
        if "test_error_code_with_dot_raises_error" in line:
            test_body = """    def test_error_code_with_dot_raises_error(self) -> None:
        \"\"\"Test that dots are converted to dashes.\"\"\"
        # "invalid.code" normalizes to "invalid-code"
        error = DummyException(message="Test", error_code="invalid.code")
        assert error.error_code == "invalid-code"
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 6: test_error_code_with_spaces_raises_error
        if "test_error_code_with_spaces_raises_error" in line:
            test_body = """    def test_error_code_with_spaces_raises_error(self) -> None:
        \"\"\"Test that spaces are converted to dashes.\"\"\"
        # "invalid code" normalizes to "invalid-code"
        error = DummyException(message="Test", error_code="invalid code")
        assert error.error_code == "invalid-code"
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 7: test_empty_error_code_raises_error
        if "test_empty_error_code_raises_error" in line:
            test_body = """    def test_empty_error_code_raises_error(self) -> None:
        \"\"\"Test that empty error code normalizes to None.\"\"\"
        error = DummyException(message="Test", error_code="")
        assert error.error_code is None
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 8: test_instantiation_with_default_values
        if "test_instantiation_with_default_values" in line:
            test_body = """    def test_instantiation_with_default_values(self) -> None:
        \"\"\"Test instantiation with minimal parameters.\"\"\"
        error = DummyException("")

        assert error.error_code is None
        assert error.message == ""
        assert error.details == {}
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # Pattern 9: test_missing_domain_raises_error (fix the old signature call)
        if "test_missing_domain_raises_error" in line:
            test_body = """    def test_missing_domain_raises_error(self) -> None:
        \"\"\"Test that using SplurgeError without _domain raises SplurgeSubclassError.\"\"\"
        with pytest.raises(SplurgeSubclassError, match="must define _domain"):
            SplurgeError("")
"""
            j = i
            while j < len(lines) and (j == i or not lines[j].startswith("    def ")):
                j += 1
            new_lines.append(test_body)
            i = j
            continue

        # For regular lines, just convert exception calls
        new_line = convert_exception_call(line)
        new_lines.append(new_line)
        i += 1

    # Check if changed
    if new_lines != lines:
        with open(path, "w") as f:
            f.writelines(new_lines)
        return True

    return False


if __name__ == "__main__":
    files = [
        "tests/unit/test_core_base_basic.py",
        "tests/unit/test_core_properties_hypothesis.py",
        "tests/unit/test_core_properties_additional_hypothesis.py",
        "tests/unit/test_core_properties_additional2_hypothesis.py",
        "tests/unit/test_core_properties_more.py",
        "tests/unit/test_edge_cases_comprehensive.py",
    ]

    for f in files:
        if convert_test_file(f):
            print(f"✓ {f}")
        else:
            print(f"- {f}")
