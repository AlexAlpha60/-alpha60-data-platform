CREATE OR REPLACE TABLE `{project_id}.{staging_dataset_id}.shopify_products` AS
SELECT
  SAFE_CAST(record_id AS INT64) AS product_id,

  CAST(record_id AS STRING) AS product_key,

  JSON_VALUE(TO_JSON(payload), '$.title') AS product_title,
  JSON_VALUE(TO_JSON(payload), '$.handle') AS handle,
  JSON_VALUE(TO_JSON(payload), '$.vendor') AS vendor,
  JSON_VALUE(TO_JSON(payload), '$.product_type') AS product_type,
  JSON_VALUE(TO_JSON(payload), '$.status') AS status,
  JSON_VALUE(TO_JSON(payload), '$.tags') AS tags,

  SAFE_CAST(JSON_VALUE(TO_JSON(payload), '$.created_at') AS TIMESTAMP) AS product_created_at,
  SAFE_CAST(JSON_VALUE(TO_JSON(payload), '$.updated_at') AS TIMESTAMP) AS product_updated_at,
  SAFE_CAST(JSON_VALUE(TO_JSON(payload), '$.published_at') AS TIMESTAMP) AS product_published_at,

  source,
  entity,
  extracted_at,
  payload

FROM `{project_id}.{raw_dataset_id}.shopify_products`;
