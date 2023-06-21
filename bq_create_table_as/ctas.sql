/*
  -- Dave Skura, 2022
*/
-- DROP TABLE `watchful-lotus-364517`.dave.samplelog_new ;

CREATE TABLE `watchful-lotus-364517`.dave.samplelog_new AS (
	SELECT _FILE_NAME as csv_filename,
		A.* 
	FROM `watchful-lotus-364517.dave.samplelog` A 
);
