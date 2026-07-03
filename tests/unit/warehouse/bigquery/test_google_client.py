"""Tests for the Google BigQuery client adapter."""

from unittest.mock import Mock, patch

from google.cloud import bigquery

from alpha60.warehouse.bigquery.config import BigQueryConfig
from alpha60.warehouse.bigquery.google_client import GoogleBigQueryClient


def test_google_bigquery_client_accepts_injected_client() -> None:
    """The adapter can use an injected BigQuery client."""
    client = Mock(spec=bigquery.Client)

    adapter = GoogleBigQueryClient(
        config=BigQueryConfig(project_id="alpha60-dev", dataset_id="raw"),
        client=client,
    )

    assert adapter is not None


def test_google_bigquery_client_creates_sdk_client_from_config() -> None:
    """The adapter creates a Google SDK client from config."""
    with patch("alpha60.warehouse.bigquery.google_client.bigquery.Client") as client_class:
        GoogleBigQueryClient(
            config=BigQueryConfig(
                project_id="alpha60-dev",
                dataset_id="raw",
                location="australia-southeast1",
            ),
        )

    client_class.assert_called_once_with(
        project="alpha60-dev",
        location="australia-southeast1",
    )