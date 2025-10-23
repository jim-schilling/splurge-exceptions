"""Core exception module."""

from splurge_exceptions.core.base import SplurgeError
from splurge_exceptions.core.exceptions import (
    SplurgeFrameworkError,
    SplurgeLookupError,
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeTypeError,
    SplurgeValueError,
)

__all__ = [
    "SplurgeError",
    "SplurgeValueError",
    "SplurgeOSError",
    "SplurgeLookupError",
    "SplurgeRuntimeError",
    "SplurgeTypeError",
    "SplurgeFrameworkError",
]
