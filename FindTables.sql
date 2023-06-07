/*
  -- Dave Skura, 2023
*/

SELECT table_catalog as project_id
  ,table_Schema as dataset_id
  ,table_name
  ,table_type
  ,creation_time
  ,DATE_DIFF(CURRENT_DATE,date(creation_time),DAY) as age_in_days
  --,ddl
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLES
-- FROM `region-us`.INFORMATION_SCHEMA.TABLES


SELECT project_id
  ,table_schema as dataset_id
  ,table_name
  ,DATE_DIFF(CURRENT_DATE,date(creation_time),DAY) as creation_age_in_days
  ,total_rows
  ,active_logical_bytes
  ,long_term_logical_bytes
  ,DATE_DIFF(CURRENT_DATE,date(storage_last_modified_time),DAY) as sorage_modified_age_in_days
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLE_STORAGE

SELECT 
  table_schema as dataset_id
  ,sum(active_logical_bytes) as active_logical_bytes
  ,sum(long_term_logical_bytes) as long_term_logical_bytes
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLE_STORAGE
-- FROM `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE
GROUP BY 1;

