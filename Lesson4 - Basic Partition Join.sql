/*

Create a temp table with a matching parttion

query to join on partition

compare bytescan

Lesson2: basic Joins support dynamic predicates.

*/

-- 225 MB (or 0.220 GB)
BEGIN
	CREATE TEMP TABLE FACADE (
		AD_YR_WK_NUM INTEGER,
		BU_VEND_NUM STRING
	) PARTITION BY RANGE_BUCKET(AD_YR_WK_NUM, GENERATE_ARRAY(201801, 203052, 1)) -- 624 partitions
	;
	INSERT INTO FACADE(AD_YR_WK_NUM,BU_VEND_NUM) VALUES 
	(202006, '0001028153');

	SELECT *
	FROM consume_tactical.ABI_BP_LCL_SALES_PROMO 
    INNER JOIN FACADE USING (AD_YR_WK_NUM,BU_VEND_NUM)
  limit 10;

END;


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
  AND query like 'FACADE'
  and user_email = 'dave.skura@loblaw.ca'
ORDER BY creation_time desc
LIMIT 10;