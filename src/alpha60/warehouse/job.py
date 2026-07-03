"""Warehouse load job abstractions."""

from dataclasses import dataclass
from enum import StrEnum


class WarehouseJobStatus(StrEnum):
    """Lifecycle states for a warehouse load job."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class WarehouseLoadJob:
    """Represents a warehouse load job."""

    job_id: str
    table_id: str
    status: WarehouseJobStatus
    rows_loaded: int = 0
    error_message: str | None = None