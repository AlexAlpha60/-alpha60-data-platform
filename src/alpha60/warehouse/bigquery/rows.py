"""BigQuery row conversion helpers."""

from typing import Any

from alpha60.core.models.record import Record


def record_to_bigquery_row(record: Record) -> dict[str, Any]:
    """Convert a generic record into a BigQuery-compatible row."""
    return {
        "source": record.source,
        "entity": record.entity,
        "record_id": record.record_id,
        "extracted_at": record.extracted_at.isoformat(),
        "payload": record.payload,
    }