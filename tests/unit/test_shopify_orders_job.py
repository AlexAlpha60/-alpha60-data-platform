"""Tests for Shopify order ingestion jobs."""

from collections.abc import Iterable
from datetime import UTC, datetime

from alpha60.core.models.record import Record
from alpha60.jobs.shopify_orders import load_shopify_orders
from alpha60.warehouse.types import WarehouseLoadResult, WarehouseLoadStatus


class FakeShopifyClient:
    """Fake Shopify client for job tests."""

    def __init__(self) -> None:
        """Create a fake Shopify client."""
        self.updated_since: datetime | None = None
        self.max_pages: int | None = None

    def get_order_records(
        self,
        updated_since: datetime | None = None,
        max_pages: int | None = None,
    ) -> list[Record]:
        """Return fake order records."""
        self.updated_since = updated_since
        self.max_pages = max_pages

        return [
            Record(
                source="shopify",
                entity="order",
                record_id="1001",
                extracted_at=datetime(2026, 7, 6, 12, 30, tzinfo=UTC),
                payload={
                    "name": "#1001",
                    "updated_at": datetime(2026, 7, 6, 13, 30, tzinfo=UTC),
                },
            )
        ]


class FakeWarehouseLoader:
    """Fake warehouse loader for job tests."""

    def __init__(self) -> None:
        """Create a fake warehouse loader."""
        self.table_id: str | None = None
        self.records: list[Record] = []

    def load(
        self,
        table_id: str,
        records: Iterable[Record],
    ) -> WarehouseLoadResult:
        """Record load inputs and return a successful result."""
        self.table_id = table_id
        self.records = list(records)

        return WarehouseLoadResult(
            table_id=table_id,
            status=WarehouseLoadStatus.SUCCESS,
            rows_loaded=len(self.records),
        )


def test_load_shopify_orders_loads_records_to_default_table() -> None:
    """Shopify order records are loaded into the default warehouse table."""
    shopify_client = FakeShopifyClient()
    warehouse_loader = FakeWarehouseLoader()

    result = load_shopify_orders(
        shopify_client=shopify_client,
        warehouse_loader=warehouse_loader,
    )

    assert result.warehouse_result.status == WarehouseLoadStatus.SUCCESS
    assert result.warehouse_result.table_id == "shopify_orders"
    assert result.warehouse_result.rows_loaded == 1
    assert result.records_processed == 1
    assert result.latest_cursor == datetime(2026, 7, 6, 13, 30, tzinfo=UTC)

    assert shopify_client.updated_since is None
    assert shopify_client.max_pages is None
    assert warehouse_loader.table_id == "shopify_orders"
    assert warehouse_loader.records[0].record_id == "1001"


def test_load_shopify_orders_allows_custom_table_id() -> None:
    """Shopify order records can be loaded into a custom table."""
    warehouse_loader = FakeWarehouseLoader()

    result = load_shopify_orders(
        shopify_client=FakeShopifyClient(),
        warehouse_loader=warehouse_loader,
        table_id="raw_shopify_orders",
    )

    assert result.warehouse_result.table_id == "raw_shopify_orders"
    assert warehouse_loader.table_id == "raw_shopify_orders"


def test_load_shopify_orders_passes_updated_since_to_client() -> None:
    """Shopify orders can be filtered by updated timestamp."""
    updated_since = datetime(2026, 7, 6, 12, 30, tzinfo=UTC)
    shopify_client = FakeShopifyClient()
    warehouse_loader = FakeWarehouseLoader()

    result = load_shopify_orders(
        shopify_client=shopify_client,
        warehouse_loader=warehouse_loader,
        updated_since=updated_since,
    )

    assert result.warehouse_result.status == WarehouseLoadStatus.SUCCESS
    assert shopify_client.updated_since == updated_since


def test_load_shopify_orders_passes_max_pages_to_client() -> None:
    """Shopify order ingestion can limit the number of fetched pages."""
    shopify_client = FakeShopifyClient()
    warehouse_loader = FakeWarehouseLoader()

    result = load_shopify_orders(
        shopify_client=shopify_client,
        warehouse_loader=warehouse_loader,
        max_pages=2,
    )

    assert result.warehouse_result.status == WarehouseLoadStatus.SUCCESS
    assert shopify_client.max_pages == 2
