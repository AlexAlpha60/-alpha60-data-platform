"""Shopify product resource."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

import httpx

from alpha60.core.models.record import Record

from .pagination import extract_next_page_info


class ShopifyRequestClient(Protocol):
    """Protocol for Shopify request clients."""

    def get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Perform a Shopify GET request."""


class ProductsResource:
    """Access Shopify product resources."""

    def __init__(self, client: ShopifyRequestClient) -> None:
        """Initialize the resource."""
        self._client = client

    def get_products(
        self,
        updated_since: datetime | None = None,
    ) -> list[dict[str, object]]:
        """Fetch products from Shopify."""
        records: list[dict[str, object]] = []

        params: dict[str, str] = {
            "limit": "250",
        }

        if updated_since is not None:
            params["updated_at_min"] = updated_since.isoformat()

        while True:
            response = self._client.get("/products.json", params=params)
            data = response.json()

            page_records = data.get("products", [])
            if isinstance(page_records, list):
                records.extend(page_records)

            next_page_info = extract_next_page_info(response)

            if next_page_info is None:
                break

            params = {
                "limit": "250",
                "page_info": next_page_info,
            }

        return records

    def get_product_records(
        self,
        updated_since: datetime | None = None,
    ) -> list[Record]:
        """Fetch Shopify products as platform records."""
        extracted_at = datetime.now(UTC)

        return [
            Record(
                source="shopify",
                entity="product",
                record_id=str(product["id"]),
                extracted_at=extracted_at,
                payload=product,
            )
            for product in self.get_products(updated_since=updated_since)
            if "id" in product
        ]