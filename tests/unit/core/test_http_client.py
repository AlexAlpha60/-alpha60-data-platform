"""Tests for the generic HTTP client."""

from __future__ import annotations

import httpx

from alpha60.core.http.client import HTTPClient
from alpha60.core.http.config import HTTPConfig


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

        return httpx.Response(
            status_code=200,
            json={"status": "ok"},
        )

    transport = httpx.MockTransport(handler)

    client = HTTPClient(transport=transport)

    response = client.get("https://example.com")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    client.close()