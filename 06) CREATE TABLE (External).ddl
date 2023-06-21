
-- DROP TABLE `myproject-364517`.mydataset.mytablename;

CREATE EXTERNAL TABLE `myproject-364517`.mydataset.mytablename (	
	Date_Time	TIMESTAMP				
	,Computer	STRING				
	,Primary_Domain	STRING				
	,IP_Address	STRING				
	,Public_IP_Address	STRING				
	,Logon_Domain	STRING				
	,User	STRING				
	,Session	INTEGER				
	,Duration	INTEGER				
	,Duration__h_mm_ss_	TIME				
	,Titlebar	STRING				
	,Executable	STRING				
	,Description	STRING				
	,Url	STRING				
	,Productivity	STRING				
	,Video	INTEGER		
)
OPTIONS (
format = 'CSV',
Field_delimiter = '\t',
uris = ['gs://my-gcp-bucket/mytablename_*.csv'],
skip_leading_rows = 1
);

/*
SELECT _FILE_NAME as csv_filename,
A.* 
FROM `myproject-364517`.mydataset.mytablename  A TABLESAMPLE SYSTEM (1 PERCENT)
LIMIT 100
*/