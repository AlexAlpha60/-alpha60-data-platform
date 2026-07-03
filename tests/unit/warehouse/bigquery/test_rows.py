"""Tests for BigQuery row conversion."""

from datetime import UTC, datetime

from alpha60.core.models.record import Record
from alpha60.warehouse.bigquery.rows import record_to_bigquery_row


def test_record_to_bigquery_row_converts_record() -> None:
    """A generic record is converted into a BigQuery-compatible row."""
    extracted_at = datetime(2026, 7, 3, 12, 30, tzinfo=UTC)
    record = Record(
        source="shopify",
        entity="products",
        record_id="123",
        extracted_at=extracted_at,
        payload={"title": "Black Jacket", "vendor": "ALPHA60"},
    )

    row = record_to_bigquery_row(record)

    assert row == {
        "source": "shopify",
        "entity": "products",
        "record_id": "123",
        "extracted_at": "2026-07-03T12:30:00+00:00",
        "payload": {"title": "Black Jacket", "vendor": "ALPHA60"},
    }