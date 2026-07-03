"""BigQuery-backed incremental state repository."""

from __future__ import annotations

from dataclasses import dataclass

from alpha60.state import IncrementalState


@dataclass(frozen=True, slots=True)
class BigQueryStateRepository:
    """Repository for reading and writing incremental state in BigQuery."""

    table_id: str

    def get_state(self, job_name: str) -> IncrementalState | None:
        """Return the latest incremental state for a job."""
        raise NotImplementedError

    def save_state(self, state: IncrementalState) -> None:
        """Persist incremental state for a job."""
        raise NotImplementedError