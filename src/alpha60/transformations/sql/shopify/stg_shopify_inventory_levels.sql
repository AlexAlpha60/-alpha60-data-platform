CREATE OR REPLACE TABLE `{project_id}.{staging_dataset_id}.shopify_inventory_levels` AS
SELECT
  SAFE_CAST(JSON_VALUE(payload, '$.inventory_item_id') AS INT64) AS inventory_item_id,
  SAFE_CAST(JSON_VALUE(payload, '$.location_id') AS INT64) AS location_id,

  CONCAT(
    JSON_VALUE(payload, '$.inventory_item_id'),
    '-',
    JSON_VALUE(payload, '$.location_id')
  ) AS inventory_level_key,

  SAFE_CAST(JSON_VALUE(payload, '$.available') AS INT64) AS available_quantity,

  SAFE_CAST(JSON_VALUE(payload, '$.updated_at') AS TIMESTAMP) AS inventory_level_updated_at,

  source,
  entity,
  extracted_at,
  payload

FROM `{project_id}.{raw_dataset_id}.shopify_inventory_levels`;
