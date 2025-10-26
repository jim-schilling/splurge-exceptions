# Hypothesis Property-Based Testing Suite

This document describes the comprehensive hypothesis property-based tests for the
Splurge Exceptions Framework v2025.1.0. These tests validate framework behavior
across a wide range of automatically generated inputs using the Hypothesis library.

## Test Suite Overview

**File:** `tests/unit/test_core_properties_hypothesis.py`  
**Version:** v2025.1.0  
**Tests:** 21 property-based tests  
**Test Scenarios Generated:** 2,100+ automatically generated test cases  
**Strategy:** Custom hypothesis strategies for valid error codes and messages  
**Focus:** Core SplurgeError functionality with new v2025.1.0 signature  

## Custom Strategies

### valid_error_codes()
Generates valid semantic error codes for the v2025.1.0 signature.

- **Format:** `[a-z][a-z0-9-]*[a-z0-9]`
- **Characteristics:**
  - Must start with lowercase letter
  - Can contain lowercase letters, digits, and hyphens
  - Must end with lowercase letter or digit
  - Minimum length: 2 characters
  - No dots allowed (user-defined codes)
- **Examples:** `"invalid-value"`, `"timeout"`, `"file-not-found"`

### valid_messages()
Generates valid error messages for the v2025.1.0 signature.

- **Format:** Any non-empty Unicode string
- **Characteristics:**
  - Minimum length: 1 character
  - Maximum length: 1,000 characters
  - Supports all Unicode characters
  - Special characters and multi-line strings allowed

## Test Categories (6 Test Classes, 21 Tests)

### 1. TestSplurgeErrorCoreProperties (9 tests)

Core functionality tests for the v2025.1.0 signature:

- `test_message_always_preserved` - Message is preserved exactly as provided
- `test_error_code_none_when_not_provided` - Error code defaults to None
- `test_full_code_format_consistency` - full_code maintains consistent format
- `test_details_preserved` - Details dictionary is completely preserved
- `test_can_attach_context` - Context attachment works on any exception
- `test_can_add_suggestions` - Suggestions can always be added
- `test_context_dict_preserved` - Context dictionary is fully preserved
- `test_exception_can_be_raised` - Exceptions can be raised and caught
- `test_str_representation_valid` - String representation always valid

### 2. TestErrorCodeNormalizationProperties (2 tests)

Error code normalization validation:

- `test_lowercase_codes_normalized` - All codes normalized to lowercase
- `test_empty_code_becomes_none` - Empty string codes become None

### 3. TestContextManagementProperties (3 tests)

Context and suggestion management:

- `test_context_retrieval_consistency` - Retrieved context matches attached
- `test_context_dict_attachment` - Context dictionary completely preserved
- `test_suggestions_order_preserved` - Suggestions always in order

### 4. TestMessageFormattingProperties (2 tests)

Message formatting and display:

- `test_get_full_message_valid` - get_full_message always returns valid string
- `test_formatter_never_raises` - Formatter never raises on any valid message

### 5. TestExceptionHierarchyProperties (3 tests)

Exception type and chaining:

- `test_splurge_value_error_is_exception` - SplurgeValueError is Exception
- `test_splurge_os_error_is_exception` - SplurgeOSError is Exception  
- `test_exception_chaining_works` - Exception chaining always works

### 6. TestIntegrationProperties (2 tests)

Integration and end-to-end workflows:

- `test_full_workflow` - Full exception workflow end-to-end
- `test_method_chaining_works` - Method chaining always works

## Key Properties Validated

### Preservation Properties
- ✓ Message is always preserved exactly as provided
- ✓ Error code is None when not provided
- ✓ Error code is normalized when provided (lowercase, dash-normalized)
- ✓ Details dictionaries are completely preserved
- ✓ Context dictionaries are completely preserved
- ✓ Suggestions are preserved in order

### Normalization Properties
- ✓ Uppercase codes normalized to lowercase
- ✓ Empty codes normalized to None
- ✓ Code normalization is consistent

### State Management Properties
- ✓ Context can always be attached after creation
- ✓ Multiple context attachments accumulate without loss
- ✓ Context handles multiple value types correctly
- ✓ Suggestions can always be added after creation
- ✓ Suggestions maintain insertion order
- ✓ Multiple suggestions accumulate without loss

### Integration Properties
- ✓ Exceptions can be raised and caught correctly
- ✓ Both context and suggestions can coexist
- ✓ Exceptions can be properly chained (__cause__)
- ✓ Method chaining always works
- ✓ All exception instances are proper Exception types

### Format Properties
- ✓ Full code always has consistent format
- ✓ String representations are always valid
- ✓ get_full_message always returns valid string
- ✓ Message formatter never raises

## Error Code Normalization Rules

The v2025.1.0 signature normalizes error codes automatically:

- **Lowercase:** "InvalidCode" → "invalidcode"
- **Symbol replacement:** spaces/underscores/dots → dashes
- **Collapse duplicates:** "invalid---code" → "invalid-code"
- **Strip edges:** "-code-" → "code"
- **Empty handling:** "" → None (no validation error)

## Test Execution Results

**Suite Summary:**
- Total Tests: 102 (81 example-based + 21 hypothesis property)
- Hypothesis Tests: 21 property-based tests
- Total Test Scenarios: 2,100+ automatically generated cases
- Test Execution Time: ~2.47 seconds
- Success Rate: 100% (102/102 passing)
- Code Coverage: 99% (199/201 lines covered)

**Hypothesis Settings:**
- Profile: CI profile (500 examples per test)
- Examples per Test: ~100 on average
- Total Examples Generated: 2,100+ unique test cases
- Shrinking: Enabled (finds minimal failing examples)
- Deadline: 5 seconds per test

## Property-Based Testing Benefits

1. **Comprehensive Coverage**
   - Automatically generates 100+ examples per test
   - Tests 2,100+ unique scenarios without explicit enumeration
   - Covers edge cases humans might miss

2. **Shrinking & Minimization**
   - When hypothesis finds a failing case, it automatically shrinks it
   - Provides minimal reproducible examples
   - Makes debugging easier and faster

3. **Invariant Validation**
   - Tests properties that should ALWAYS hold true
   - Not just specific examples, but general principles
   - Catches regressions automatically

4. **Normalization Validation**
   - Validates error code normalization logic
   - Tests all normalization rules
   - Ensures consistent behavior

5. **State & Behavior Validation**
   - Tests exception state after operations
   - Validates method chaining works correctly
   - Ensures operations maintain invariants

## Integration with Existing Tests

The 21 hypothesis tests complement the 81 example-based tests:

**Example-Based Tests (81 tests):**
- Specific known scenarios
- Step-by-step workflows
- Integration scenarios
- Real-world usage patterns
- Coverage gap cases

**Property-Based Tests (21 tests):**
- General properties that always hold
- Normalization validation
- State management invariants
- Format consistency
- Behavior under generated data

**Combined Approach:**
- Example tests catch "this specific case breaks"
- Property tests catch "this property should always hold"
- Together they achieve 99% code coverage

## Running the Tests

**Run just property tests:**
```bash
pytest tests/unit/test_core_properties_hypothesis.py -v
```

**Run all unit tests:**
```bash
pytest tests/unit -q
```

**Run with hypothesis verbosity:**
```bash
pytest tests/unit/test_core_properties_hypothesis.py -v --hypothesis-verbosity=verbose
```

**Run with specific seed for reproducibility:**
```bash
pytest tests/unit/test_core_properties_hypothesis.py --hypothesis-seed=0
```

**Run with coverage:**
```bash
pytest tests/unit --cov=splurge_exceptions --cov-report=term-missing
```

## Version History

### v2025.1.0 (Current)
- **Status:** Active
- **Tests:** 21 property-based tests
- **Signature:** `__init__(message: str, error_code: str | None = None, details: dict | None = None)`
- **Focus:** Message-first signature with automatic error code normalization
- **Coverage:** 99% (199/201 lines)

### v2025.0.0 (Previous)
- **Status:** Archived
- **Tests:** 27 hypothesis property tests (deprecated)
- **Signature:** `__init__(error_code: str, *, message: str)`
- **Note:** Old tests removed due to breaking API changes in v2025.1.0
   - Unicode handling
   - Special character escaping

5. Performance Properties:
   - Exception creation performance
   - Context attachment scaling
   - Large suggestion lists handling
