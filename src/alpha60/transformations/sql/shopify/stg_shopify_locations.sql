CREATE OR REPLACE TABLE `{project_id}.{staging_dataset_id}.shopify_locations` AS
WITH latest_locations AS (
  SELECT * EXCEPT(row_num)
  FROM (
    SELECT
      *,
      ROW_NUMBER() OVER (
        PARTITION BY record_id
        ORDER BY extracted_at DESC
      ) AS row_num
    FROM `{project_id}.{raw_dataset_id}.shopify_locations`
  )
  WHERE row_num = 1
)

SELECT
  SAFE_CAST(record_id AS INT64) AS location_id,

  JSON_VALUE(payload, '$.name') AS location_name,
  JSON_VALUE(payload, '$.address1') AS address1,
  JSON_VALUE(payload, '$.address2') AS address2,
  JSON_VALUE(payload, '$.city') AS city,
  JSON_VALUE(payload, '$.province') AS province,
  JSON_VALUE(payload, '$.province_code') AS province_code,
  JSON_VALUE(payload, '$.country') AS country,
  JSON_VALUE(payload, '$.country_code') AS country_code,
  JSON_VALUE(payload, '$.zip') AS postcode,

  SAFE_CAST(
    JSON_VALUE(payload, '$.active')
    AS BOOL
  ) AS is_active,

  SAFE_CAST(
    JSON_VALUE(payload, '$.legacy')
    AS BOOL
  ) AS is_legacy,

  SAFE_CAST(
    JSON_VALUE(payload, '$.created_at')
    AS TIMESTAMP
  ) AS location_created_at,

  SAFE_CAST(
    JSON_VALUE(payload, '$.updated_at')
    AS TIMESTAMP
  ) AS location_updated_at,

  source,
  entity,
  extracted_at,
  payload

FROM latest_locations;
