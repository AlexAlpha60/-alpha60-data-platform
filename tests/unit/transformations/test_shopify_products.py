"""Tests for Shopify products staging transformation factory."""

from unittest.mock import Mock

from alpha60.transformations.result import TransformationStatus
from alpha60.transformations.shopify_products import (
    create_shopify_products_staging_transformation,
)
from alpha60.warehouse.bigquery.config import BigQueryConfig


def test_create_shopify_products_staging_transformation_runs_sql() -> None:
    """The factory creates a runnable Shopify products staging transformation."""
    client = Mock()
    config = BigQueryConfig(
        project_id="alpha60-data-platform",
        dataset_id="raw",
        location="australia-southeast1",
    )

    transformation = create_shopify_products_staging_transformation(
        client=client,
        raw_config=config,
        staging_dataset_id="stg",
    )

    result = transformation.run()

    assert result.status == TransformationStatus.SUCCESS
    assert result.target_table_id == "alpha60-data-platform.stg.shopify_products"

    sql = client.query.call_args.args[0]
    assert "CREATE OR REPLACE TABLE `alpha60-data-platform.stg.shopify_products`" in sql
    assert "FROM `alpha60-data-platform.raw.shopify_products`" in sql
    assert "SAFE_CAST(record_id AS INT64) AS product_id" in sql
    assert "CAST(record_id AS STRING) AS product_key" in sql
