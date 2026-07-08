WITH base AS (
    SELECT
        demand.*,
        locations.can_send_rotations,
        locations.can_receive_rotations,
        locations.rotation_priority
    FROM `alpha60-data-platform.warehouse.variant_location_demand` AS demand
    JOIN `alpha60-data-platform.warehouse.dim_locations` AS locations
      ON demand.location_id = locations.location_id
),

receivers AS (
    SELECT *
    FROM base
    WHERE can_receive_rotations = TRUE
      AND available_quantity <= 1
      AND style_demand_score > 0
),

senders AS (
    SELECT *
    FROM base
    WHERE can_send_rotations = TRUE
      AND available_quantity > 0
),

candidates AS (
    SELECT
        receiver.variant_id,
        receiver.product_id,
        receiver.product_title,
        receiver.variant_title,
        receiver.sku,

        sender.location_id AS send_from_location_id,
        sender.location_name AS send_from_location_name,
        sender.available_quantity AS send_from_available_quantity,
        sender.style_units_sold_12_weeks AS send_from_style_units_12_weeks,
        sender.style_demand_score AS send_from_style_demand_score,

        receiver.location_id AS send_to_location_id,
        receiver.location_name AS send_to_location_name,
        receiver.available_quantity AS send_to_available_quantity,
        receiver.style_units_sold_12_weeks AS send_to_style_units_12_weeks,
        receiver.style_demand_score AS send_to_style_demand_score,
        receiver.rotation_priority AS send_to_rotation_priority,

        receiver.warehouse_available_quantity,

        1 AS recommended_transfer_quantity,

        receiver.style_demand_score - sender.style_demand_score AS style_demand_gap,

        (
            (receiver.style_demand_score - sender.style_demand_score) * 10
            + receiver.rotation_priority
            + CASE
                WHEN receiver.available_quantity <= 0 THEN 50
                WHEN receiver.available_quantity = 1 THEN 25
                ELSE 0
              END
            + CASE
                WHEN receiver.warehouse_available_quantity <= 0 THEN 100
                ELSE 0
              END
        ) AS rotation_score,

        CASE
            WHEN receiver.warehouse_available_quantity <= 0
                THEN 'rotation_candidate_warehouse_empty'
            ELSE 'rotation_watchlist_warehouse_has_stock'
        END AS recommendation_type,

        CURRENT_TIMESTAMP() AS modelled_at

    FROM receivers AS receiver

    JOIN senders AS sender
      ON receiver.variant_id = sender.variant_id
     AND receiver.location_id != sender.location_id
     AND receiver.style_demand_score > sender.style_demand_score
)

SELECT *
FROM candidates
ORDER BY
    recommendation_type,
    rotation_score DESC,
    style_demand_gap DESC
