"""Tests for Shopify order staging transformation factory."""

from unittest.mock import Mock

from alpha60.transformations.result import TransformationStatus
from alpha60.transformations.shopify_orders import (
    create_shopify_orders_staging_transformation,
)
from alpha60.warehouse.bigquery.config import BigQueryConfig


def test_create_shopify_orders_staging_transformation_runs_sql() -> None:
    """The factory creates a runnable Shopify orders staging transformation."""
    client = Mock()
    config = BigQueryConfig(
        project_id="alpha60-data-platform",
        dataset_id="raw",
        location="australia-southeast1",
    )

    transformation = create_shopify_orders_staging_transformation(
        client=client,
        raw_config=config,
        staging_dataset_id="stg",
    )

    result = transformation.run()

    assert result.status == TransformationStatus.SUCCESS
    assert result.target_table_id == "alpha60-data-platform.stg.shopify_orders"

    sql = client.query.call_args.args[0]
    assert "CREATE OR REPLACE TABLE `alpha60-data-platform.stg.shopify_orders`" in sql
    assert "FROM `alpha60-data-platform.raw.shopify_orders`" in sql
    assert "SAFE_CAST(record_id AS INT64) AS order_id" in sql
