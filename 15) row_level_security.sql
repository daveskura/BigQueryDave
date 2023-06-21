-- https://cloud.google.com/bigquery/docs/managing-row-level-security

/*
CREATE ROW ACCESS POLICY my_row_filter
ON dataset.my_table
GRANT TO ('domain:example.com')
FILTER USING (email = SESSION_USER());

*/


DROP TABLE `watchful-lotus-364517.dave.rando_table`;
CREATE TABLE `watchful-lotus-364517.dave.rando_table` (
  user STRING,
  year INT64,			
  month INT64,			
  sent_to STRING,		
  email_count INT64,	
  avg_email_length INT64, 
  min_email_length INT64, 
  max_email_length INT64 
)
PARTITION BY
  RANGE_BUCKET(Year, GENERATE_ARRAY(2000, 2030, 30)) -- 30 partitions, from 2000-2030
CLUSTER BY
	Month
	,sent_to
OPTIONS (
	require_partition_filter = False
	,description = 'Data comes from ....'
) ;

INSERT INTO `watchful-lotus-364517.dave.rando_table` (user,year,month,sent_to,email_count,avg_email_length,min_email_length,max_email_length)
VALUES (SESSION_USER(),2023,1,'thisguy@email.com',123,333,444,2000);

INSERT INTO `watchful-lotus-364517.dave.rando_table` (user,year,month,sent_to,email_count,avg_email_length,min_email_length,max_email_length)
VALUES (SESSION_USER(),2022,1,'thatguy@email.com',122,222,212,2003);

INSERT INTO `watchful-lotus-364517.dave.rando_table` (user,year,month,sent_to,email_count,avg_email_length,min_email_length,max_email_length)
VALUES (SESSION_USER(),2021,1,'guy@email.com',133,155,166,2050);


CREATE ROW ACCESS POLICY thisuser_filter
ON `watchful-lotus-364517.dave.rando_table`
GRANT TO ('user:sqlmaster7@gmail.com')
FILTER USING (year=2021);
