"""Shopify Admin API client."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import httpx

from alpha60.core.http.client import HTTPClient


class ShopifyClient:
    """Client for Shopify Admin API requests."""

    def __init__(
        self,
        shop_domain: str,
        access_token: str,
        api_version: str = "2025-01",
        http_client: HTTPClient | None = None,
    ) -> None:
        """Initialize the Shopify client."""
        self.shop_domain = shop_domain
        self.access_token = access_token
        self.api_version = api_version
        self.http_client = http_client or HTTPClient()

    def build_url(self, path: str) -> str:
        """Build a Shopify Admin API URL."""
        normalized_path = path if path.startswith("/") else f"/{path}"

        return (
            f"https://{self.shop_domain}"
            f"/admin/api/{self.api_version}"
            f"{normalized_path}"
        )

    def get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Perform an authenticated Shopify GET request."""
        return self.http_client.get(
            self.build_url(path),
            headers={
                "X-Shopify-Access-Token": self.access_token,
            },
            params=params,
        )

    def test_connection(self) -> bool:
        """Verify Shopify credentials."""
        response = self.get("/shop.json")
        return response.status_code == 200

    def get_products(self) -> list[dict[str, object]]:
        """Fetch all products from Shopify."""
        return self.get_paginated("/products.json", "products")

    def get_paginated(
        self,
        path: str,
        response_key: str,
    ) -> list[dict[str, object]]:
        """Fetch all paginated records for a Shopify endpoint."""
        records: list[dict[str, object]] = []
        params: dict[str, str] | None = {"limit": "250"}

        while True:
            response = self.get(path, params=params)
            data = response.json()

            page_records = data.get(response_key, [])
            if isinstance(page_records, list):
                records.extend(page_records)

            next_page_info = self._extract_next_page_info(response)

            if next_page_info is None:
                break

            params = {
                "limit": "250",
                "page_info": next_page_info,
            }

        return records

    def _extract_next_page_info(self, response: httpx.Response) -> str | None:
        """Extract the next page_info cursor from a Shopify Link header."""
        link_header = response.headers.get("Link")

        if link_header is None:
            return None

        for link_part in link_header.split(","):
            if 'rel="next"' not in link_part:
                continue

            url_start = link_part.find("<")
            url_end = link_part.find(">")

            if url_start == -1 or url_end == -1:
                return None

            next_url = link_part[url_start + 1 : url_end]
            query = parse_qs(urlparse(next_url).query)
            page_info = query.get("page_info")

            if page_info:
                return page_info[0]

        return None