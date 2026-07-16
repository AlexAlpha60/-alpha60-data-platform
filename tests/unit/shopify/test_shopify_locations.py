"""Tests for Shopify location resource."""

from unittest.mock import Mock

import httpx

from alpha60.connectors.shopify.locations import LocationsResource


def test_locations_resource_fetches_location_records() -> None:
    """Locations are returned as platform records."""
    response = httpx.Response(
        status_code=200,
        json={
            "locations": [
                {
                    "id": 123,
                    "name": "Melbourne Store",
                    "active": True,
                }
            ]
        },
    )
    client = Mock()
    client.get.return_value = response

    resource = LocationsResource(client)

    records = resource.get_location_records()

    assert len(records) == 1
    assert records[0].source == "shopify"
    assert records[0].entity == "location"
    assert records[0].record_id == "123"
    assert records[0].payload["name"] == "Melbourne Store"


def test_locations_resource_returns_empty_list_for_invalid_payload() -> None:
    """Invalid location payloads return an empty list."""
    response = httpx.Response(
        status_code=200,
        json={"locations": None},
    )
    client = Mock()
    client.get.return_value = response

    resource = LocationsResource(client)

    assert resource.get_locations() == []
