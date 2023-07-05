/*
  -- Dave Skura, 2023

  There are ways to preview data free:
  1 - interactively, in the BQEditor, select the table, select preview
  	Select [hamburger menu][BigQuery][dataset][table]

  2 - Calling the BQ API you can ask for table metadata.  Metadata includes sample data.

  There is a way to query at a reduced cost, using TABLESAMPLE.
  * TABLESAMPLE only works on tables

*/


/* Table is 1.34 TB.
  table has 134 partitions, avg size ~ 10GB each
  smallest count 562 MB */
SELECT count(*) -- 16,336
FROM consume_tactical.ABI_BP_LCL_SALES_PROMO A -- TABLESAMPLE SYSTEM (1 PERCENT) -- 3.7 MB 
WHERE AD_YR_WK_NUM = 202006 and BU_VEND_NUM = '0001028153'  

-- Why 0 results ? because that partition/cluster is not in the randomly select 1% of the table

/*
SELECT TOTAL_PARTITIONS -- 134 partitions
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE project_id = 'lt-dia-lake-sbx' AND 
      table_schema = 'consume_tactical' AND
      table_name = 'ABI_BP_LCL_SALES_PROMO'
*/