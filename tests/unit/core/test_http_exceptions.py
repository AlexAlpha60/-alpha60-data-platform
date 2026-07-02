"""Tests for HTTP exception hierarchy."""

from alpha60.core.http.exceptions import (
    AuthenticationError,
    HTTPClientError,
    RateLimitError,
    RequestTimeoutError,
    ServerError,
    UnexpectedResponseError,
)


def test_all_exceptions_inherit_from_http_client_error() -> None:
    assert issubclass(AuthenticationError, HTTPClientError)
    assert issubclass(RateLimitError, HTTPClientError)
    assert issubclass(RequestTimeoutError, HTTPClientError)
    assert issubclass(ServerError, HTTPClientError)
    assert issubclass(UnexpectedResponseError, HTTPClientError)


def test_exception_message_is_preserved() -> None:
    message = "Authentication failed"
    exception = AuthenticationError(message)

    assert str(exception) == message