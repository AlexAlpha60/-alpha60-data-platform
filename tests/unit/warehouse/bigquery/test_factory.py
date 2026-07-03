"""Tests for BigQuery warehouse factories."""

from unittest.mock import patch

from alpha60.warehouse.bigquery.config import BigQueryConfig
from alpha60.warehouse.bigquery.factory import create_bigquery_loader
from alpha60.warehouse.bigquery.loader import BigQueryLoader


def test_create_bigquery_loader_returns_loader() -> None:
    """The factory creates a BigQuery loader."""
    config = BigQueryConfig(
        project_id="alpha60-dev",
        dataset_id="raw",
    )

    with patch("alpha60.warehouse.bigquery.google_client.bigquery.Client"):
        loader = create_bigquery_loader(config=config)

    assert isinstance(loader, BigQueryLoader)