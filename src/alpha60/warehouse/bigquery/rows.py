"""BigQuery row conversion helpers."""

from typing import Any

from alpha60.core.models.record import Record


def _normalise_bigquery_value(key: str, value: Any) -> Any:
    """Normalise values that BigQuery may otherwise infer incorrectly."""
    if key == "phone" and value is not None:
        return str(value)

    if isinstance(value, dict):
        return _normalise_bigquery_payload(value)

    if isinstance(value, list):
        return [
            _normalise_bigquery_payload(item)
            if isinstance(item, dict)
            else item
            for item in value
        ]

    return value


def _normalise_bigquery_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a BigQuery-safe copy of a record payload."""
    return {
        key: _normalise_bigquery_value(key, value)
        for key, value in payload.items()
    }


def record_to_bigquery_row(record: Record) -> dict[str, Any]:
    """Convert a generic record into a BigQuery-compatible row."""
    return {
        "source": record.source,
        "entity": record.entity,
        "record_id": record.record_id,
        "extracted_at": record.extracted_at.isoformat(),
        "payload": _normalise_bigquery_payload(record.payload),
    }
