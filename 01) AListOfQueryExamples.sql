/*
  -- Dave Skura, 2023
*/

SELECT _FILE_NAME as csv_filename,
A.* 
FROM `myproject-364517`.mydataset.mytablename  A TABLESAMPLE SYSTEM (1 PERCENT)
LIMIT 100
