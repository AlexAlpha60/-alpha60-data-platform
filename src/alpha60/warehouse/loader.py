"""Generic warehouse loader interface."""

from collections.abc import Iterable
from typing import Protocol

from alpha60.core.models.record import Record


class WarehouseLoader(Protocol):
    """Interface for loading records into a warehouse."""

    def load(self, table_id: str, records: Iterable[Record]) -> None:
        """Load records into the specified warehouse table."""