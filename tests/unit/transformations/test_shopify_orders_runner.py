"""Tests for Shopify orders staging transformation composition."""

from unittest.mock import Mock, patch

from alpha60.config.bigquery import BigQuerySettings
from alpha60.config.settings import Settings
from alpha60.config.shopify import ShopifySettings
from alpha60.transformations.result import TransformationResult, TransformationStatus
from alpha60.transformations.shopify_orders_runner import (
    run_shopify_orders_staging_transformation,
)


def _settings() -> Settings:
    """Create test settings."""
    return Settings(
        environment="test",
        log_level="INFO",
        shopify=ShopifySettings(
            shop_domain="alpha60.myshopify.com",
            client_id="client-id",
            client_secret="client-secret",
            api_version="2025-01",
        ),
        bigquery=BigQuerySettings(
            project_id="alpha60-data-platform",
            dataset_id="raw",
            location="australia-southeast1",
        ),
    )


def test_run_shopify_orders_staging_transformation_wires_dependencies() -> None:
    """The runner builds dependencies from settings and runs the transformation."""
    expected_result = TransformationResult(
        target_table_id="alpha60-data-platform.stg.shopify_orders",
        status=TransformationStatus.SUCCESS,
    )

    with (
        patch(
            "alpha60.transformations.shopify_orders_runner.create_bigquery_client"
        ) as client_factory,
        patch(
            "alpha60.transformations.shopify_orders_runner."
            "create_shopify_orders_staging_transformation"
        ) as transformation_factory,
    ):
        client = Mock()
        transformation = Mock()
        client_factory.return_value = client
        transformation_factory.return_value = transformation
        transformation.run.return_value = expected_result

        result = run_shopify_orders_staging_transformation(settings=_settings())

    assert result == expected_result
    client_factory.assert_called_once()
    transformation_factory.assert_called_once()
    transformation.run.assert_called_once_with()

    raw_config = client_factory.call_args.kwargs["config"]
    assert raw_config.project_id == "alpha60-data-platform"
    assert raw_config.dataset_id == "raw"
    assert raw_config.location == "australia-southeast1"

    assert transformation_factory.call_args.kwargs["client"] == client
    assert transformation_factory.call_args.kwargs["raw_config"] == raw_config
    assert transformation_factory.call_args.kwargs["staging_dataset_id"] == "stg"


def test_run_shopify_orders_staging_transformation_uses_custom_staging_dataset() -> None:
    """The runner passes a custom staging dataset to the transformation."""
    expected_result = TransformationResult(
        target_table_id="alpha60-data-platform.alpha60_dev_staging.shopify_orders",
        status=TransformationStatus.SUCCESS,
    )

    with (
        patch(
            "alpha60.transformations.shopify_orders_runner.create_bigquery_client"
        ) as client_factory,
        patch(
            "alpha60.transformations.shopify_orders_runner."
            "create_shopify_orders_staging_transformation"
        ) as transformation_factory,
    ):
        transformation = Mock()
        client_factory.return_value = Mock()
        transformation_factory.return_value = transformation
        transformation.run.return_value = expected_result

        result = run_shopify_orders_staging_transformation(
            settings=_settings(),
            staging_dataset_id="alpha60_dev_staging",
        )

    assert result == expected_result
    assert (
        transformation_factory.call_args.kwargs["staging_dataset_id"]
        == "alpha60_dev_staging"
    )
