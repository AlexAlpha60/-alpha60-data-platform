"""Shopify Admin API client."""

from __future__ import annotations

from datetime import datetime

import httpx

from alpha60.core.http.client import HTTPClient
from alpha60.core.models.record import Record

from .products import ProductsResource


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
        self.products = ProductsResource(self)

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
            headers={"X-Shopify-Access-Token": self.access_token},
            params=params,
        )

    def test_connection(self) -> bool:
        """Verify Shopify credentials."""
        response = self.get("/shop.json")
        return response.status_code == 200

    def get_products(
        self,
        updated_since: datetime | None = None,
    ) -> list[dict[str, object]]:
        """Fetch products from Shopify."""
        return self.products.get_products(updated_since=updated_since)

    def get_product_records(
        self,
        updated_since: datetime | None = None,
    ) -> list[Record]:
        """Fetch Shopify products as platform records."""
        return self.products.get_product_records(updated_since=updated_since)