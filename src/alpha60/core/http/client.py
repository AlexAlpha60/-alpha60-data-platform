"""Generic HTTP client."""

from __future__ import annotations

import httpx

from alpha60.core.http.config import HTTPConfig


class HTTPClient:
    """Reusable HTTP client for external APIs."""

    def __init__(
        self,
        config: HTTPConfig | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        """Initialize the HTTP client."""
        self.config = config or HTTPConfig()

        self._client = httpx.Client(
            timeout=self.config.timeout,
            transport=transport,
            headers={
                "User-Agent": self.config.user_agent,
            },
        )

    def get(self, url: str) -> httpx.Response:
        """Perform an HTTP GET request."""
        return self._client.get(url)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()