"""Tests for Shopify location ingestion jobs."""

from collections.abc import Iterable
from datetime import UTC, datetime

from alpha60.core.models.record import Record
from alpha60.jobs.shopify_locations import load_shopify_locations
from alpha60.warehouse.types import WarehouseLoadResult, WarehouseLoadStatus


class FakeShopifyClient:
    """Fake Shopify client for location job tests."""

    def get_location_records(self) -> list[Record]:
        """Return fake location records."""
        return [
            Record(
                source="shopify",
                entity="location",
                record_id="123",
                extracted_at=datetime(2026, 7, 8, 10, 0, tzinfo=UTC),
                payload={"id": 123, "name": "Melbourne Store"},
            )
        ]


class FakeWarehouseLoader:
    """Fake warehouse loader for job tests."""

    def __init__(self) -> None:
        """Create fake loader."""
        self.table_id: str | None = None
        self.records: list[Record] = []

    def load(
        self,
        table_id: str,
        records: Iterable[Record],
    ) -> WarehouseLoadResult:
        """Record load inputs and return success."""
        self.table_id = table_id
        self.records = list(records)

        return WarehouseLoadResult(
            table_id=table_id,
            status=WarehouseLoadStatus.SUCCESS,
            rows_loaded=len(self.records),
        )


def test_load_shopify_locations_loads_records_to_default_table() -> None:
    """Shopify location records are loaded into the default warehouse table."""
    warehouse_loader = FakeWarehouseLoader()

    result = load_shopify_locations(
        shopify_client=FakeShopifyClient(),
        warehouse_loader=warehouse_loader,
    )

    assert result.warehouse_result.status == WarehouseLoadStatus.SUCCESS
    assert result.warehouse_result.table_id == "shopify_locations"
    assert result.warehouse_result.rows_loaded == 1
    assert result.records_processed == 1
    assert result.latest_cursor is None

    assert warehouse_loader.table_id == "shopify_locations"
    assert warehouse_loader.records[0].record_id == "123"
