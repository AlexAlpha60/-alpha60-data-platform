SELECT
    ROW_NUMBER() OVER (ORDER BY rotation_score DESC) AS rotation_rank,

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
        'Move ', CAST(recommended_transfer_quantity AS STRING),
        ' unit from ', send_from_location_name,
        ' to ', send_to_location_name,
        '. ', send_to_location_name,
        ' has ', CAST(send_to_available_quantity AS STRING),
        ' units and sold ', CAST(send_to_style_units_12_weeks AS STRING),
        ' style units in 12 weeks. ',
        send_from_location_name,
        ' has ', CAST(send_from_available_quantity AS STRING),
        ' units and sold ', CAST(send_from_style_units_12_weeks AS STRING),
        ' style units. Warehouse has ',
        CAST(warehouse_available_quantity AS STRING),
        ' units.'
    ) AS recommendation_reason,

    modelled_at

FROM `alpha60-data-platform.warehouse.store_rotation_candidates`
WHERE candidate_rank = 1 AND donor_rank = 1
