"""Typed exceptions for the generic HTTP client."""

from __future__ import annotations


class HTTPClientError(Exception):
    """Base class for all HTTP client errors."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        super().__init__(message)


class AuthenticationError(HTTPClientError):
    """Authentication or authorization failed."""


class RateLimitError(HTTPClientError):
    """The remote API rate limit has been exceeded."""


class RequestTimeoutError(HTTPClientError):
    """The HTTP request timed out."""


class ServerError(HTTPClientError):
    """The remote server returned a 5xx response."""


class UnexpectedResponseError(HTTPClientError):
    """The HTTP response could not be processed."""