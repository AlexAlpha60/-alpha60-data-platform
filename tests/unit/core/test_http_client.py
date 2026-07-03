"""Tests for the generic HTTP client."""

from __future__ import annotations

import httpx
import pytest

from alpha60.core.http.client import HTTPClient
from alpha60.core.http.config import HTTPConfig
from alpha60.core.http.exceptions import (
    AuthenticationError,
    RateLimitError,
    RequestTimeoutError,
    ServerError,
)


def test_http_client_uses_default_configuration() -> None:
    client = HTTPClient()

    assert client.config == HTTPConfig()

    client.close()


def test_http_client_accepts_custom_configuration() -> None:
    config = HTTPConfig(timeout=10.0)

    client = HTTPClient(config=config)

    assert client.config is config

    client.close()


def test_get_returns_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert str(request.url) == "https://example.com"

        return httpx.Response(status_code=200, json={"status": "ok"})

    client = HTTPClient(transport=httpx.MockTransport(handler))

    response = client.get("https://example.com")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    client.close()


@pytest.mark.parametrize("status_code", [401, 403])
def test_get_raises_authentication_error(status_code: int) -> None:
    client = HTTPClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(status_code=status_code)
        )
    )

    with pytest.raises(AuthenticationError, match="Authentication failed"):
        client.get("https://example.com")

    client.close()


def test_get_raises_rate_limit_error() -> None:
    client = HTTPClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status_code=429))
    )

    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        client.get("https://example.com")

    client.close()


def test_get_raises_server_error() -> None:
    client = HTTPClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status_code=500))
    )

    with pytest.raises(ServerError, match="Remote server error"):
        client.get("https://example.com")

    client.close()


def test_get_raises_timeout_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timeout")

    client = HTTPClient(transport=httpx.MockTransport(handler))

    with pytest.raises(RequestTimeoutError, match="HTTP request timed out"):
        client.get("https://example.com")

    client.close()