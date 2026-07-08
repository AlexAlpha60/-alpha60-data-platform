"""Shopify location resource."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol

import httpx

from alpha60.core.models.record import Record


class ShopifyRequestClient(Protocol):
    """Protocol for Shopify request clients."""

    def get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Perform a Shopify GET request."""


class LocationsResource:
    """Access Shopify location resources."""

    def __init__(self, client: ShopifyRequestClient) -> None:
        """Initialize the resource."""
        self._client = client

    def get_locations(self) -> list[dict[str, object]]:
        """Fetch locations from Shopify."""
        response = self._client.get("/locations.json")
        data = response.json()

        locations = data.get("locations", [])
        if not isinstance(locations, list):
            return []

        return [
            location
            for location in locations
            if isinstance(location, dict)
        ]

    def get_location_records(self) -> list[Record]:
        """Fetch Shopify locations as platform records."""
        extracted_at = datetime.now(UTC)

        return [
            Record(
                source="shopify",
                entity="location",
                record_id=str(location["id"]),
                extracted_at=extracted_at,
                payload=location,
            )
            for location in self.get_locations()
            if "id" in location
        ]
