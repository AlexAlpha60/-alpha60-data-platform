"""Shared types for the BigQuery warehouse."""

from dataclasses import dataclass
from enum import StrEnum


class BigQueryWriteDisposition(StrEnum):
    """Supported BigQuery write behaviours."""

    APPEND = "WRITE_APPEND"
    TRUNCATE = "WRITE_TRUNCATE"
    EMPTY = "WRITE_EMPTY"


class BigQueryLoadStatus(StrEnum):
    """Result status for a BigQuery load operation."""

    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class BigQueryLoadResult:
    """Result of a BigQuery load operation."""

    table_id: str
    status: BigQueryLoadStatus
    rows_loaded: int
    error_message: str | None = None