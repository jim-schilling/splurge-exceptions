"""Core exception module."""

from splurge_exceptions.core.base import SplurgeError
from splurge_exceptions.core.exceptions import (
    SplurgeAuthenticationError,
    SplurgeAuthorizationError,
    SplurgeConfigurationError,
    SplurgeFrameworkError,
    SplurgeNotImplementedError,
    SplurgeOSError,
    SplurgeRuntimeError,
    SplurgeValidationError,
)

__all__ = [
    "SplurgeError",
    "SplurgeValidationError",
    "SplurgeOSError",
    "SplurgeConfigurationError",
    "SplurgeRuntimeError",
    "SplurgeAuthenticationError",
    "SplurgeAuthorizationError",
    "SplurgeNotImplementedError",
    "SplurgeFrameworkError",
]
