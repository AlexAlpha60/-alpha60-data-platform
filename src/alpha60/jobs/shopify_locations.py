"""Shopify location ingestion jobs."""

from typing import Protocol

from alpha60.core.models.record import Record
from alpha60.jobs.result import IngestionJobResult
from alpha60.warehouse.loader import WarehouseLoader


_DEFAULT_LOCATIONS_TABLE_ID = "shopify_locations"


class ShopifyLocationsClient(Protocol):
    """Client capable of returning Shopify location records."""

    def get_location_records(self) -> list[Record]:
        """Fetch Shopify locations as platform records."""


def load_shopify_locations(
    shopify_client: ShopifyLocationsClient,
    warehouse_loader: WarehouseLoader,
    table_id: str = _DEFAULT_LOCATIONS_TABLE_ID,
) -> IngestionJobResult:
    """Load Shopify location records into a warehouse table."""
    records = shopify_client.get_location_records()

    warehouse_result = warehouse_loader.load(
        table_id=table_id,
        records=records,
    )

    return IngestionJobResult(
        warehouse_result=warehouse_result,
        records_processed=len(records),
        latest_cursor=None,
    )
