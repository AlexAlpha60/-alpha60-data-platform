"""Composition root for Shopify inventory level ingestion."""

from alpha60.config.settings import Settings
from alpha60.connectors.shopify.auth import ShopifyAuthenticator
from alpha60.connectors.shopify.client import ShopifyClient
from alpha60.jobs.shopify_inventory_levels import load_shopify_inventory_levels
from alpha60.warehouse.bigquery.config import BigQueryConfig
from alpha60.warehouse.bigquery.factory import (
    create_bigquery_client,
    create_bigquery_loader,
)
from alpha60.warehouse.types import WarehouseLoadResult


def _get_inventory_item_ids(
    project_id: str,
    staging_dataset_id: str,
    location: str,
) -> list[int]:
    """Fetch inventory item IDs from staged product variants."""
    bigquery_config = BigQueryConfig(
        project_id=project_id,
        dataset_id=staging_dataset_id,
        location=location,
    )
    client = create_bigquery_client(config=bigquery_config)

    rows = client.query(
        f"""
        SELECT DISTINCT inventory_item_id
        FROM `{project_id}.{staging_dataset_id}.shopify_product_variants`
        WHERE inventory_item_id IS NOT NULL
        ORDER BY inventory_item_id
        """
    )

    return [
        int(row["inventory_item_id"])
        for row in rows
        if row.get("inventory_item_id") is not None
    ]


def run_shopify_inventory_levels_ingestion(settings: Settings) -> WarehouseLoadResult:
    """Run the Shopify inventory levels ingestion job using runtime settings."""
    inventory_item_ids = _get_inventory_item_ids(
        project_id=settings.bigquery.project_id,
        staging_dataset_id=settings.bigquery.staging_dataset_id,
        location=settings.bigquery.location,
    )

    authenticator = ShopifyAuthenticator(
        shop_domain=settings.shopify.shop_domain,
        client_id=settings.shopify.client_id,
        client_secret=settings.shopify.client_secret,
    )

    shopify_client = ShopifyClient(
        shop_domain=settings.shopify.shop_domain,
        access_token=authenticator.get_access_token(),
        api_version=settings.shopify.api_version,
    )

    bigquery_config = BigQueryConfig(
        project_id=settings.bigquery.project_id,
        dataset_id=settings.bigquery.dataset_id,
        location=settings.bigquery.location,
    )

    bigquery_loader = create_bigquery_loader(config=bigquery_config)

    job_result = load_shopify_inventory_levels(
        shopify_client=shopify_client,
        warehouse_loader=bigquery_loader,
        inventory_item_ids=inventory_item_ids,
    )

    return job_result.warehouse_result
