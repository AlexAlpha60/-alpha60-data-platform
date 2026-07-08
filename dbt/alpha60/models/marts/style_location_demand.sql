WITH sales AS (
    SELECT
        fact_sales.product_id,
        locations.location_name,
        fact_sales.quantity,
        fact_sales.order_created_at
    FROM `alpha60-data-platform.warehouse.fact_sales` AS fact_sales

    JOIN `alpha60-data-platform.warehouse.dim_locations` AS locations
      ON fact_sales.sales_location_name = locations.sales_location_name

    WHERE fact_sales.sales_location_name IS NOT NULL
),

summary AS (
    SELECT
        product_id,
        location_name,

        SUM(
            CASE
                WHEN order_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 28 DAY)
                THEN quantity
                ELSE 0
            END
        ) AS style_units_4_weeks,

        SUM(
            CASE
                WHEN order_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 84 DAY)
                THEN quantity
                ELSE 0
            END
        ) AS style_units_12_weeks,

        MAX(order_created_at) AS last_sale_at

    FROM sales

    GROUP BY
        product_id,
        location_name
)

SELECT
    product_id,
    location_name,
    style_units_4_weeks,
    style_units_12_weeks,

    SAFE_DIVIDE(style_units_4_weeks, 4)
      + SAFE_DIVIDE(style_units_12_weeks, 12) AS demand_score,

    last_sale_at,
    CURRENT_TIMESTAMP() AS modelled_at

FROM summary
