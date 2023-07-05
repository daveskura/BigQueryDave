/*
  -- Dave Skura, 2023

Find biggest table with partitions and clusters
check bytescan

find actual bytescan check jobs

Create a view as select *

compare bytescan.

* See views supporting pushdown predicates.

*/


SELECT project_id,table_schema as dataset_id, table_name
  ,total_rows,active_logical_bytes + long_term_logical_bytes as size
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE TOTAL_PARTITIONS > 0
ORDER BY 5 desc;

SELECT *
FROM consume_tactical.ABI_BP_LCL_SALES_PROMO A TABLESAMPLE SYSTEM (1 PERCENT)
WHERE AD_YR_WK_NUM = 202006 and BU_VEND_NUM = '0001028153'


-- 1.34 TB
SELECT *
FROM consume_tactical.ABI_BP_LCL_SALES_PROMO /* A TABLESAMPLE SYSTEM (1 PERCENT)  -- 59 MB*/
WHERE AD_YR_WK_NUM = 202006 -- 8.8 GB  (partition field)
 AND BU_VEND_NUM = '0001028153' -- 0.22 GB (including cluster field)


SELECT project_id
  ,user_email
  ,creation_time
  ,job_type
  ,total_bytes_billed/1024/1024/1024 as gigabytes_billed
  ,query
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.JOBS
WHERE date(creation_time) = current_date -- partition field
  AND project_id = 'lt-dia-lake-sbx' -- cluster field
  AND job_type = 'QUERY' AND statement_type != 'SCRIPT'
  AND query like '%0001028153%'
  and user_email = 'dave.skura@loblaw.ca'
ORDER BY creation_time desc
LIMIT 10;

CREATE VIEW daves_dataset.lesson1_view as
SELECT *
FROM consume_tactical.ABI_BP_LCL_SALES_PROMO;

SELECT *
FROM daves_dataset.lesson1_view;


-- 1.34 TB
SELECT *
FROM daves_dataset.lesson1_view -- TABLESAMPLE not available on views
WHERE AD_YR_WK_NUM = 202006 -- 8.8 GB  (partition field)
 AND BU_VEND_NUM = '0001028153' -- 0.22 GB (including cluster field)