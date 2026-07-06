"""Tests for Shopify order resource."""

from __future__ import annotations

from datetime import UTC, datetime

import httpx

from alpha60.connectors.shopify.client import ShopifyClient
from alpha60.core.http.client import HTTPClient


def test_get_orders_fetches_orders_from_shopify() -> None:
    """Orders are fetched from the Shopify orders endpoint."""
    seen_params: dict[str, str] | None = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_params
        seen_params = dict(request.url.params)

        return httpx.Response(
            status_code=200,
            json={
                "orders": [
                    {
                        "id": 123,
                        "name": "#1001",
                    }
                ]
            },
        )

    http_client = HTTPClient(transport=httpx.MockTransport(handler))
    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    orders = client.get_orders()

    assert orders == [{"id": 123, "name": "#1001"}]
    assert seen_params == {
        "limit": "250",
        "status": "any",
    }

    http_client.close()


def test_get_orders_passes_updated_since_filter() -> None:
    """Orders can be filtered by updated timestamp."""
    updated_since = datetime(2026, 7, 6, 10, 30, tzinfo=UTC)
    seen_params: dict[str, str] | None = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal seen_params
        seen_params = dict(request.url.params)

        return httpx.Response(
            status_code=200,
            json={"orders": []},
        )

    http_client = HTTPClient(transport=httpx.MockTransport(handler))
    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    assert client.get_orders(updated_since=updated_since) == []

    assert seen_params == {
        "limit": "250",
        "status": "any",
        "updated_at_min": updated_since.isoformat(),
    }

    http_client.close()


def test_get_order_records_returns_platform_records() -> None:
    """Shopify orders are converted into platform records."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={
                "orders": [
                    {
                        "id": 123,
                        "name": "#1001",
                    },
                    {
                        "name": "missing-id",
                    },
                ]
            },
        )

    http_client = HTTPClient(transport=httpx.MockTransport(handler))
    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    records = client.get_order_records()

    assert len(records) == 1
    assert records[0].source == "shopify"
    assert records[0].entity == "order"
    assert records[0].record_id == "123"
    assert records[0].payload == {
        "id": 123,
        "name": "#1001",
    }

    http_client.close()
    