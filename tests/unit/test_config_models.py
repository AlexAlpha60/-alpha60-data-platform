"""Tests for configuration models."""

from alpha60.config.bigquery import BigQuerySettings
from alpha60.config.shopify import ShopifySettings


def test_shopify_settings_defaults_optional_authentication_fields() -> None:
    """Shopify settings default optional authentication fields."""
    settings = ShopifySettings(
        shop_domain="alpha60.myshopify.com",
    )

    assert settings.access_token == ""
    assert settings.client_id == ""
    assert settings.client_secret == ""
    assert settings.api_version == "2025-01"


def test_bigquery_settings_defaults_location() -> None:
    """BigQuery settings default to the configured region."""
    settings = BigQuerySettings(
        project_id="alpha60-dev",
        dataset_id="raw",
    )

    assert settings.location == "australia-southeast1"