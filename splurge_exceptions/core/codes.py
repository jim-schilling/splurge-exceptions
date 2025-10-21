"""Compatibility module - Error code registry no longer used.

DOMAINS: ["exceptions", "codes"]

NOTE: The ErrorCodeRegistry, ErrorCode, and related functions have been removed
in version 2025.0.0 as part of the error code system redesign.

The new system uses:
- Private _domain class attribute on exception classes
- Semantic user-provided error codes (e.g., "invalid-column")
- Full code computed as: "{domain}.{error_code}"
- No registry needed - codes are deterministic

This module is maintained for backward compatibility only.
"""

__all__: list[str] = []
