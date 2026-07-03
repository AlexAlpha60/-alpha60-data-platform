"""Incremental loading state models for the ALPHA60 Data Platform."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class IncrementalState:
    """Represents the persisted state for an incremental ingestion job."""

    job_name: str
    cursor_field: str
    cursor_value: datetime | None = None