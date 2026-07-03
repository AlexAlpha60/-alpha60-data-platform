"""Tests for the Shopify API client."""

from __future__ import annotations

import httpx

from alpha60.connectors.shopify.client import ShopifyClient
from alpha60.core.http.client import HTTPClient


def test_shopify_client_builds_admin_api_url() -> None:
    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
    )

    assert (
        client.build_url("/products.json")
        == "https://alpha60-test.myshopify.com/admin/api/2025-01/products.json"
    )


def test_shopify_client_sends_authenticated_get_request() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert (
            str(request.url)
            == "https://alpha60-test.myshopify.com/admin/api/2025-01/products.json"
        )
        assert request.headers["X-Shopify-Access-Token"] == "test-token"

        return httpx.Response(status_code=200, json={"products": []})

    http_client = HTTPClient(transport=httpx.MockTransport(handler))

    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    response = client.get("/products.json")

    assert response.status_code == 200
    assert response.json() == {"products": []}

    http_client.close()


def test_shopify_client_tests_connection() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == "https://alpha60-test.myshopify.com/admin/api/2025-01/shop.json"
        )
        assert request.headers["X-Shopify-Access-Token"] == "test-token"

        return httpx.Response(status_code=200, json={"shop": {"name": "ALPHA60"}})

    http_client = HTTPClient(transport=httpx.MockTransport(handler))

    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    assert client.test_connection() is True

    http_client.close()


def test_shopify_client_gets_products() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            str(request.url)
            == "https://alpha60-test.myshopify.com/admin/api/2025-01/products.json?limit=250"
        )
        assert request.headers["X-Shopify-Access-Token"] == "test-token"

        return httpx.Response(
            status_code=200,
            json={"products": [{"id": 123, "title": "Test Product"}]},
        )

    http_client = HTTPClient(transport=httpx.MockTransport(handler))

    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    products = client.get_products()

    assert products == [{"id": 123, "title": "Test Product"}]

    http_client.close()


def test_shopify_client_gets_paginated_products() -> None:
    request_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        request_urls.append(str(request.url))

        if len(request_urls) == 1:
            return httpx.Response(
                status_code=200,
                json={"products": [{"id": 1, "title": "Product 1"}]},
                headers={
                    "Link": (
                        '<https://alpha60-test.myshopify.com/admin/api/2025-01/'
                        'products.json?limit=250&page_info=next-page>; rel="next"'
                    )
                },
            )

        return httpx.Response(
            status_code=200,
            json={"products": [{"id": 2, "title": "Product 2"}]},
        )

    http_client = HTTPClient(transport=httpx.MockTransport(handler))

    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    products = client.get_products()

    assert products == [
        {"id": 1, "title": "Product 1"},
        {"id": 2, "title": "Product 2"},
    ]
    assert request_urls == [
        "https://alpha60-test.myshopify.com/admin/api/2025-01/products.json?limit=250",
        (
            "https://alpha60-test.myshopify.com/admin/api/2025-01/products.json"
            "?limit=250&page_info=next-page"
        ),
    ]

    http_client.close()


def test_shopify_client_gets_product_records() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={"products": [{"id": 123, "title": "Test Product"}]},
        )

    http_client = HTTPClient(transport=httpx.MockTransport(handler))

    client = ShopifyClient(
        shop_domain="alpha60-test.myshopify.com",
        access_token="test-token",
        http_client=http_client,
    )

    records = client.get_product_records()

    assert len(records) == 1
    assert records[0].source == "shopify"
    assert records[0].entity == "product"
    assert records[0].record_id == "123"
    assert records[0].payload == {"id": 123, "title": "Test Product"}

    http_client.close()