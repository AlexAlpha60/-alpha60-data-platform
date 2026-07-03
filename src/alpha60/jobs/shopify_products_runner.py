"""Composition root for Shopify product ingestion."""

from alpha60.config.settings import Settings
from alpha60.connectors.shopify.client import ShopifyClient
from alpha60.jobs.shopify_products import load_shopify_products
from alpha60.warehouse.bigquery.config import BigQueryConfig
from alpha60.warehouse.bigquery.factory import create_bigquery_loader
from alpha60.warehouse.types import WarehouseLoadResult


def run_shopify_products_ingestion(settings: Settings) -> WarehouseLoadResult:
    """Run the Shopify products ingestion job using runtime settings."""
    shopify_client = ShopifyClient(
        shop_domain=settings.shopify.shop_domain,
        access_token=settings.shopify.access_token,
        api_version=settings.shopify.api_version,
    )

    bigquery_loader = create_bigquery_loader(
        config=BigQueryConfig(
            project_id=settings.bigquery.project_id,
            dataset_id=settings.bigquery.dataset_id,
            location=settings.bigquery.location,
        )
    )

    return load_shopify_products(
        shopify_client=shopify_client,
        warehouse_loader=bigquery_loader,
    )