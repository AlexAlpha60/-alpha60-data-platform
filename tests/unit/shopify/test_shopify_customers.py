"""Tests for Shopify customer resource."""

from unittest.mock import Mock

import httpx

from alpha60.connectors.shopify.customers import CustomersResource


def test_customers_resource_fetches_customer_records() -> None:
    """Customers are returned as platform records."""
    response = httpx.Response(
        status_code=200,
        json={
            "customers": [
                {
                    "id": 123,
                    "email": "test@example.com",
                    "phone": 61419999999,
                    "updated_at": "2026-07-07T12:00:00+00:00",
                }
            ]
        },
    )
    client = Mock()
    client.get.return_value = response

    resource = CustomersResource(client)

    records = resource.get_customer_records()

    assert len(records) == 1
    assert records[0].source == "shopify"
    assert records[0].entity == "customer"
    assert records[0].record_id == "123"
    assert records[0].payload["phone"] == "61419999999"


def test_customers_resource_normalises_nested_phone_numbers() -> None:
    """Customer phone numbers are always strings."""
    response = httpx.Response(
        status_code=200,
        json={
            "customers": [
                {
                    "id": 123,
                    "phone": 61419999999,
                    "default_address": {
                        "phone": "+61419 99999 5507883141",
                    },
                    "addresses": [
                        {
                            "phone": 61419999998,
                        }
                    ],
                }
            ]
        },
    )
    client = Mock()
    client.get.return_value = response

    resource = CustomersResource(client)

    customers = resource.get_customers()

    customer = customers[0]
    assert isinstance(customer, dict)

    default_address = customer["default_address"]
    assert isinstance(default_address, dict)

    addresses = customer["addresses"]
    assert isinstance(addresses, list)

    first_address = addresses[0]
    assert isinstance(first_address, dict)

    assert customer["phone"] == "61419999999"
    assert default_address["phone"] == "+61419 99999 5507883141"
    assert first_address["phone"] == "61419999998"


def test_customers_resource_respects_max_pages() -> None:
    """Customer pagination can be limited for testing."""
    response = httpx.Response(
        status_code=200,
        json={
            "customers": [
                {
                    "id": 123,
                }
            ]
        },
        headers={
            "Link": (
                '<https://alpha60.myshopify.com/admin/api/2025-01/'
                'customers.json?limit=250&page_info=next-page>; rel="next"'
            )
        },
    )
    client = Mock()
    client.get.return_value = response

    resource = CustomersResource(client)

    customers = resource.get_customers(max_pages=1)

    assert customers == [{"id": 123, "phone": None}]
    client.get.assert_called_once()
