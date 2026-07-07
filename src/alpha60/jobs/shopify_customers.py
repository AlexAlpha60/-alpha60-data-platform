"""Shopify customer ingestion jobs."""

from datetime import datetime
from typing import Protocol

from alpha60.core.models.record import Record
from alpha60.jobs.result import IngestionJobResult
from alpha60.warehouse.loader import WarehouseLoader


_DEFAULT_CUSTOMERS_TABLE_ID = "shopify_customers"


class ShopifyCustomersClient(Protocol):
    """Client capable of returning Shopify customer records."""

    def get_customer_records(
        self,
        updated_since: datetime | None = None,
        max_pages: int | None = None,
    ) -> list[Record]:
        """Fetch Shopify customers as platform records."""


def _extract_latest_updated_at(records: list[Record]) -> datetime | None:
    """Extract the latest Shopify updated_at cursor from records."""
    updated_at_values: list[datetime] = []

    for record in records:
        updated_at = record.payload.get("updated_at")

        if isinstance(updated_at, datetime):
            updated_at_values.append(updated_at)

    if not updated_at_values:
        return None

    return max(updated_at_values)


def load_shopify_customers(
    shopify_client: ShopifyCustomersClient,
    warehouse_loader: WarehouseLoader,
    table_id: str = _DEFAULT_CUSTOMERS_TABLE_ID,
    updated_since: datetime | None = None,
    max_pages: int | None = None,
) -> IngestionJobResult:
    """Load Shopify customer records into a warehouse table."""
    records = shopify_client.get_customer_records(
        updated_since=updated_since,
        max_pages=max_pages,
    )

    warehouse_result = warehouse_loader.load(
        table_id=table_id,
        records=records,
    )

    return IngestionJobResult(
        warehouse_result=warehouse_result,
        records_processed=len(records),
        latest_cursor=_extract_latest_updated_at(records),
    )
