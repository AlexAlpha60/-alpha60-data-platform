"""Shopify inventory level ingestion jobs."""

from typing import Protocol

from alpha60.core.models.record import Record
from alpha60.jobs.result import IngestionJobResult
from alpha60.warehouse.loader import WarehouseLoader


_DEFAULT_INVENTORY_LEVELS_TABLE_ID = "shopify_inventory_levels"


class ShopifyInventoryLevelsClient(Protocol):
    """Client capable of returning Shopify inventory level records."""

    def get_inventory_level_records(
        self,
        inventory_item_ids: list[int],
    ) -> list[Record]:
        """Fetch Shopify inventory levels as platform records."""


def load_shopify_inventory_levels(
    shopify_client: ShopifyInventoryLevelsClient,
    warehouse_loader: WarehouseLoader,
    inventory_item_ids: list[int],
    table_id: str = _DEFAULT_INVENTORY_LEVELS_TABLE_ID,
) -> IngestionJobResult:
    """Load Shopify inventory level records into a warehouse table."""
    records = shopify_client.get_inventory_level_records(
        inventory_item_ids=inventory_item_ids,
    )

    warehouse_result = warehouse_loader.load(
        table_id=table_id,
        records=records,
    )

    return IngestionJobResult(
        warehouse_result=warehouse_result,
        records_processed=len(records),
        latest_cursor=None,
    )
