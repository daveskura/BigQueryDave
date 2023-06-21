/*
  -- Dave Skura, 2022

  partition_expiration_days = 3 -- only for time partitions
*/


CREATE TABLE `mysql-work`.ossn.current_ossn_user (
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
  RANGE_BUCKET(guid, GENERATE_ARRAY(0, 100, 2)) -- 51 partitions, from 0-100, [0,1][2,3][4,5][6,7]
  CLUSTER BY
    type
    ,username
    ,email
  OPTIONS (
    require_partition_filter = False
    ,description = 'a user table partitioned by guid, clustered by type,username,email '
    ) ;



