@echo off
REM gcp commands from your laptop 

REM copy a file from laptop to bucket
REM gsutil cp test.txt gs://dtc456/dave/test.txt

REM extract a file from BigQuery to csv
bq extract --destination_format CSV --field_delimiter , --print_header=true Professional.activtrak_all gs://dtc456/dave/activtrak_all_20221026.csv

REM download a file from a bucket to your current directory
gsutil cp gs://dtc456/dave/activtrak_all_20221026.csv .

