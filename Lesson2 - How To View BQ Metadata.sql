/*
  -- Dave Skura, 2023
  
  Here are 3 ways to preview data free:
  1 - interactively, in the BQEditor, select the table, select preview
  	Select [hamburger menu][BigQuery][dataset][table]

  2 - Calling the BQ API you can ask for table metadata.  Metadata includes sample data.

  3 - query the views in INFORMATION_SCHEMA

	JOBS - find your queries,slot usage and cost.  qualify partition and project. 
	TABLE_STORAGE - find tables and size in rows and bytes, active and long term,physical & logical.
	TABLE_OPTIONS - find tables with no expiration date.
*/

-- find queries and the cost.  good pratice to qualify partition and project.
BEGIN
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
	  AND query like '%'
	  and user_email = 'dave.skura@loblaw.ca'
	ORDER BY creation_time desc
	LIMIT 10;
END;

-- find tables and size with no partitions 
BEGIN

	SELECT project_id,table_schema as dataset_id, table_name
	  ,total_rows,active_logical_bytes + long_term_logical_bytes as size
	FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLE_STORAGE
	WHERE TOTAL_PARTITIONS > 0
	ORDER BY 5 desc;

END;

-- find tables with no expiration date.
BEGIN

	WITH tables_with_expiration AS (
	SELECT 
	  table_catalog 
	  ,table_schema
	  ,table_name
	FROM `region-northamerica-northeast1.INFORMATION_SCHEMA.TABLE_OPTIONS` A
	WHERE option_name = 'expiration_timestamp')

	SELECT
	DISTINCT 
	  table_catalog 
	  ,table_schema
	  ,table_name
	FROM `region-northamerica-northeast1.INFORMATION_SCHEMA.TABLE_OPTIONS` A
		LEFT JOIN tables_with_expiration B USING (table_catalog ,table_schema,table_name)

	WHERE B.table_schema is null;

END;
