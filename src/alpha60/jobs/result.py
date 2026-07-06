"""Job result models for ALPHA60 ingestion jobs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from alpha60.warehouse.types import WarehouseLoadResult


@dataclass(frozen=True, slots=True)
class IngestionJobResult:
    """Result of an ingestion job."""

    warehouse_result: WarehouseLoadResult
    records_processed: int
    latest_cursor: datetime | None = None