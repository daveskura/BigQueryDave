
REM extract a file from BigQuery to csv
bq extract --destination_format CSV --field_delimiter , --print_header=true Professional.activtrak_all gs://dtc456/dave/activtrak_all_20221026.csv


dataset
logsV2

user
661198@activtrak.us

pwd
r26B!@Lb6


bq query --nouse_legacy_sql \
'SELECT
   COUNT(*)
 FROM
   `bigquery-public-data`.samples.shakespeare'