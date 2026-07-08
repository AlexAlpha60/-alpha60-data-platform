WITH sales AS (
    SELECT
        variant_id,
        product_id,
        customer_email,
        order_created_at,
        quantity
    FROM `alpha60-data-platform.warehouse.fact_sales`
),

sales_by_variant AS (
    SELECT
        variant_id,

        SUM(
            CASE
                WHEN order_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
                THEN quantity
                ELSE 0
            END
        ) AS units_sold_4_weeks,

        SUM(
            CASE
                WHEN order_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 84 DAY)
                THEN quantity
                ELSE 0
            END
        ) AS units_sold_12_weeks,

        MIN(order_created_at) AS first_sale_at,
        MAX(order_created_at) AS last_sale_at

    FROM sales
    GROUP BY variant_id
),

warehouse_stock AS (
    SELECT
        variant_id,
        SUM(available_quantity) AS warehouse_available_quantity
    FROM `alpha60-data-platform.warehouse.fact_inventory_snapshot`
    WHERE location_name = 'Online / Warehouse'
    GROUP BY variant_id
)

SELECT
    inventory.location_id,
    inventory.location_name,

    inventory.product_id,
    inventory.variant_id,
    inventory.inventory_item_id,

    inventory.product_title,
    inventory.variant_title,
    inventory.sku,
    inventory.vendor,
    inventory.product_type,
    inventory.product_status,

    inventory.available_quantity,

    COALESCE(sales_by_variant.units_sold_4_weeks, 0) AS units_sold_4_weeks,
    COALESCE(sales_by_variant.units_sold_12_weeks, 0) AS units_sold_12_weeks,

    sales_by_variant.first_sale_at,
    sales_by_variant.last_sale_at,

    DATE_DIFF(
        CURRENT_DATE(),
        DATE(sales_by_variant.last_sale_at),
        DAY
    ) AS days_since_last_sale,

    COALESCE(sales_by_variant.units_sold_12_weeks, 0) > 0 AS has_recent_demand,

    inventory.available_quantity <= 0 AS currently_out_of_stock,

    COALESCE(warehouse_stock.warehouse_available_quantity, 0) AS warehouse_available_quantity,

    COALESCE(warehouse_stock.warehouse_available_quantity, 0) <= 0 AS warehouse_out_of_stock,

    CURRENT_TIMESTAMP() AS modelled_at

FROM `alpha60-data-platform.warehouse.fact_inventory_snapshot` AS inventory

LEFT JOIN sales_by_variant
    ON inventory.variant_id = sales_by_variant.variant_id

LEFT JOIN warehouse_stock
    ON inventory.variant_id = warehouse_stock.variant_id
