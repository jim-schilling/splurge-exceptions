"""Splurge Exceptions Framework - Core module.

This module provides the base exception class and core error handling infrastructure
for the Splurge family of Python libraries and tools.

DOMAINS: ["exceptions", "errors"]
"""

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
from splurge_exceptions.decorators.error_handler import handle_exceptions
from splurge_exceptions.formatting.message import ErrorMessageFormatter
from splurge_exceptions.managers.exception import error_context
from splurge_exceptions.wrappers.stdlib import wrap_exception

__version__ = "2025.0.0"
__domains__ = ["exceptions", "errors", "handlers"]

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
    "wrap_exception",
    "handle_exceptions",
    "error_context",
    "ErrorMessageFormatter",
]
