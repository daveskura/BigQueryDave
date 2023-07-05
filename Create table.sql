
CREATE TABLE `gcpproject`.mybigquerydataset.user (
  guid INTEGER
  ,type STRING
  ,username STRING
  ,email STRING
  ,password STRING
  ,salt STRING
  ,first_name STRING
  ,last_name STRING
  ,last_login INTEGER
  ,last_activity INTEGER
  ,activation  STRING
  ,time_created INTEGER
)
PARTITION BY
  /* 
    ALWAYS ALWAYS ALWAYS provide a partition and 3 cluster fields whenever your table is larger 
	than the minimum byte charge size for bigquery, which is 10MB
    
    Creating partitions using ranges of numbers / partition has massive impact.
    Google allows 4000 partitions.

	If you create a partition with 1000 buckets, and qualify it in the queries,
	The cost for running the query approaches almost 1000 times less !!

	Cluster fields work amazing with partitions, but even without, they should be used.  
  */
  RANGE_BUCKET(guid, GENERATE_ARRAY(0, 100, 2)) -- 51 partitions, from 0-100, [0,1][2,3][4,5][6,7]
  CLUSTER BY
    type
    ,username
    ,email
  OPTIONS (
    require_partition_filter = False
	,partition_expiration_days = 2555 -- 365*7
    ,description = 'a user table partitioned by guid, clustered by type,username,email '
    ) ;



