"""Unit tests for the BigQuery incremental state repository."""

from __future__ import annotations

from alpha60.warehouse.bigquery.state_repository import BigQueryStateRepository


def test_bigquery_state_repository_stores_table_id() -> None:
    """BigQueryStateRepository stores the configured state table ID."""
    repository = BigQueryStateRepository(
        table_id="alpha60_dev_warehouse.platform_state",
    )

    assert repository.table_id == "alpha60_dev_warehouse.platform_state"