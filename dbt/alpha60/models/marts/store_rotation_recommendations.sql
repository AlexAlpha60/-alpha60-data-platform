SELECT
    ROW_NUMBER() OVER (
        ORDER BY rotation_score DESC
    ) AS rotation_rank,

    recommendation_type,

    product_title,
    variant_title,
    sku,

    send_from_location_name,
    send_to_location_name,

    recommended_transfer_quantity,

    send_from_available_quantity,
    send_to_available_quantity,
    warehouse_available_quantity,

    send_from_style_units_12_weeks,
    send_to_style_units_12_weeks,

    ROUND(rotation_score, 1) AS rotation_score,

    CONCAT(
        'Move ',
        CAST(recommended_transfer_quantity AS STRING),
        ' unit from ',
        send_from_location_name,
        ' to ',
        send_to_location_name,
        '. Warehouse has ',
        CAST(warehouse_available_quantity AS STRING),
        ' units remaining.'
    ) AS recommendation_reason,

    modelled_at

FROM `alpha60-data-platform.warehouse.store_rotation_candidates`

WHERE warehouse_available_quantity <= 0

ORDER BY rotation_rank
