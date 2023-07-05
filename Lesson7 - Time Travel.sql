/*
  -- Dave Skura, 2023

BigQuery time travel stores data every time the state changes for 2-7 days.

the default duration is 7 days.

For the logical billing method, you are not charged for time travel bytes, so 7 days is fine.

once we switch to physical byte billing mode, we should reduce the default time travel days to save the cost.

*/


SELECT *
FROM daves_dataset.tablea
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);


INSERT INTO daves_dataset.tablea
SELECT -1 as projectNumber
  ,'test case 1' as projectId
  ,lifecycleState					
  ,name	
  ,CURRENT_TIMESTAMP() as createTime					
  ,parent_type	
  ,parent_id
FROM daves_dataset.tablea
LIMIT 1;


SELECT *
FROM daves_dataset.tablea
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
WHERE projectNumber = -1


SELECT 
  A.time_travel_physical_bytes
  ,A.total_physical_bytes
  ,A.total_logical_bytes
  ,A.*
FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.TABLE_STORAGE A
WHERE A.time_travel_physical_bytes > 0
ORDER BY  A.time_travel_physical_bytes desc

-- in lt-dia-lake-prd-consume you can see this gets much bigger