"""Shopify customer resource."""

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


class CustomersResource:
    """Access Shopify customer resources."""

    def __init__(self, client: ShopifyRequestClient) -> None:
        """Initialize the resource."""
        self._client = client

    def get_customers(
        self,
        updated_since: datetime | None = None,
        max_pages: int | None = None,
    ) -> list[dict[str, object]]:
        """Fetch customers from Shopify."""
        records: list[dict[str, object]] = []
        pages_fetched = 0

        params: dict[str, str] = {
            "limit": "250",
        }

        if updated_since is not None:
            params["updated_at_min"] = updated_since.isoformat()

        while True:
            response = self._client.get("/customers.json", params=params)
            pages_fetched += 1

            data = response.json()
            page_records = data.get("customers", [])

            if isinstance(page_records, list):
                records.extend(page_records)

            if max_pages is not None and pages_fetched >= max_pages:
                break

            next_page_info = extract_next_page_info(response)

            if next_page_info is None:
                break

            params = {
                "limit": "250",
                "page_info": next_page_info,
            }

        return records

    def get_customer_records(
        self,
        updated_since: datetime | None = None,
        max_pages: int | None = None,
    ) -> list[Record]:
        """Fetch Shopify customers as platform records."""
        extracted_at = datetime.now(UTC)

        return [
            Record(
                source="shopify",
                entity="customer",
                record_id=str(customer["id"]),
                extracted_at=extracted_at,
                payload=customer,
            )
            for customer in self.get_customers(
                updated_since=updated_since,
                max_pages=max_pages,
            )
            if "id" in customer
        ]
