/*
  -- Dave Skura, 2023
  Selecting data from an external table
  showing the name of the source csvfile from the gcp bucket
  selecting only 1% of the rows
*/

SELECT _FILE_NAME as csv_filename,
A.* 
FROM `myproject-364517`.mydataset.mytablename  A TABLESAMPLE SYSTEM (1 PERCENT)
LIMIT 100
