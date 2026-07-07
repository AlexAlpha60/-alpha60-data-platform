"""Composition root for Shopify orders staging transformation."""

from alpha60.config.settings import Settings
from alpha60.transformations.result import TransformationResult
from alpha60.transformations.shopify_orders import (
    create_shopify_orders_staging_transformation,
)
from alpha60.warehouse.bigquery.config import BigQueryConfig
from alpha60.warehouse.bigquery.factory import create_bigquery_client


_DEFAULT_STAGING_DATASET_ID = "stg"


def run_shopify_orders_staging_transformation(
    settings: Settings,
    staging_dataset_id: str = _DEFAULT_STAGING_DATASET_ID,
) -> TransformationResult:
    """Run the Shopify orders staging transformation using runtime settings."""
    raw_config = BigQueryConfig(
        project_id=settings.bigquery.project_id,
        dataset_id=settings.bigquery.dataset_id,
        location=settings.bigquery.location,
    )

    client = create_bigquery_client(config=raw_config)
    transformation = create_shopify_orders_staging_transformation(
        client=client,
        raw_config=raw_config,
        staging_dataset_id=staging_dataset_id,
    )

    return transformation.run()
