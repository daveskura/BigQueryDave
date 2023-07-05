/*
  -- Dave Skura, 2023

	BigQuery is a columnar database great for analytics, OLAP queries and data science.
	The read/query of large data is incredibly fast.
	max columns is 10,000
	(postgres max is 1600, MySQL is 4096, Redshift is 1664, Delta tables support over 4000 cols but have a row limit of 20MB
	
	updating/deleting is very slow, and limited by a hard transaction count/day.  Insert only is faster.
    
	Re: BigQuery...
	It is not a classic RDBMS.  Bigquery stores data in columns similar to Databricks Delta tables and AWS Redshift.
	It is not the best choice for reporting & dashboards
	It does not have referential integrity 
	It is not suitable for OLTP use cases.

*/
Classic design theory in RDBMS:
Model tables by entity with associated attributes uniquely attributed to the unique key in the same table.  The basis for this being the classic normalized datamodel.  This is also sometimes referred to as vertical modelling.  1st, 2nd & 3rd normal form present increasing abstraction from the contextual content of the data and increased type coding, requiring more and more intersect joins in your queries.  Popular relational databases like Teradata, DB2 and Oracle support at least 64 table joins in single query.

Classic design supports realtime/online applications for creating and maintaining data very well.
Classic design also supports reporting tools like Power BI, Plateau and Qlik very well, as these reporting tools and are designed to make it easy to build reports based on indexed/vertical tables.  It is very for the tools to automatically requery the source database on each user click to filter the data showing on a page.  

A word on primary/foreign keys:
Until recently, BigQuery didn`t even have primary/foreign keys so no referential integrity.  BigQuery has this now, but I`ve still never seen it used.  A primary key in Bigquery is not an index, it is only to ensure uniqueness of the row, which means if you add a primary key you will cause CRUD operations to fail if they violate the key.


My thoughts on the complex datatypes:

	complex datatypes such as STRUCT and ARRAY:
	pros:
	offer a way to bury/nest large amounts of data in a single field without duplicating any other fields.

	cons:
	these fields cannot be partitioned or clustered
	add complexity


My thoughts on adding columns:
remember this example
	-- ALL fields: 1.34 TB
	-- one field(ARTCL_ACCT_ASSN_GRP_CD): 17.25 GB
	SELECT ARTCL_ACCT_ASSN_GRP_CD
	FROM daves_dataset.lesson1_view;


Designing a table for columnar in BigQuery:
1) Tables should be lean and wide.  
	- Lean as in, don`t generat needless ids
	- wide as in, many columns.
	
	You should not be generating uneccessary surrogate id values for look up tables for data which is not multipurpose.  You don`t need to break everything down to it`s own entity and join it later with ids.  The number of supported columns is massive, and if people only select the fields they are interested in, there is little downside to making tables very wide.

2) Judicious use of complex struct and array field types.  Using struct fields means you have to understand how to unnest the data elements, and searching the struct fields is more expensive bytewise because BQ has to search the whole Struct to get your burried field.  For a case where the data will not be joined or qualified, simply stored and retrieved as is, the struct field can make sense.  Array fields I would caution against as they add complexity with little gain.

3) Partitioning and Cluster fields

	ALWAYS ALWAYS ALWAYS provide a partition and 3 cluster fields whenever your table is larger 
	than the minimum byte charge size for bigquery, which is 10MB

	Creating partitions using ranges of numbers / partition has massive impact.
	Google allows 4000 partitions.

	If you create a partition with 1000 buckets, and qualify it in the queries,
	The cost for running the query approaches almost 1000 times less !!

	Cluster fields work amazing with partitions, but even without, they should be used.  

	You should think of cluster fields like a single compound index on a table.








