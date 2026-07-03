"""Factory helpers for BigQuery warehouse components."""

from alpha60.warehouse.bigquery.config import BigQueryConfig
from alpha60.warehouse.bigquery.google_client import GoogleBigQueryClient
from alpha60.warehouse.bigquery.loader import BigQueryLoader


def create_bigquery_loader(config: BigQueryConfig) -> BigQueryLoader:
    """Create a BigQuery loader using the Google BigQuery client."""
    return BigQueryLoader(
        config=config,
        client=GoogleBigQueryClient(config=config),
    )