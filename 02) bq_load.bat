@echo off
REM
REM  Dave Skura, 2021
REM
REM Determine TMS for unique naming.
REM

FOR /f "tokens=2 delims==" %%G in ('wmic os get localdatetime /value') do set datetime=%%G
for /f "tokens=1,2,3 delims=: " %%a in ("%time%") do set hr=%%a&set min=%%b&set secs=%%c

REM Building a timestamp from variables
SET "dd=%datetime:~6,2%"
SET "mth=%datetime:~4,2%"
SET "yyyy=%datetime:~0,4%"
SET "Date=%yyyy%%mth%%dd%"
SET TMS=%hr%-%min%

REM ----- TARGET
SET FILE_SUFFIX=%DATE%-%TMS%
SET TARGET_DIR=C:\work\data
SET FILE_PREFIX=ossn_users
SET BUCKET_FILE=ossn_users.csv

SET TARGETFILE=%TARGET_DIR%\%FILE_PREFIX%_%FILE_SUFFIX%.csv

echo  extracting from MySQL

call C:\work\MySQL\mysql_export.bat %TARGETFILE%

DIR %TARGETFILE%

REM ------- can optionally store this in a GCP bucket --------
REM echo  Load file to GCP Bucket gs://dskura-mysql-bucket
REM call gcloud storage cp %TARGETFILE% gs://dskura-mysql-bucket/%BUCKET_FILE%

REM ------------ this would cost money to run the bq sql each time ----------
REM bq --project_id=mysql-work --dataset_id=mysql-work.ossn query --nouse_legacy_sql < update_current_ossn_user.sql

echo emptying ossn.current_ossn_user and loading ossn.current_ossn_user 

REM ----------- this load statement should be free ------------------------
@echo on

bq load --autodetect --replace --source_format=CSV ossn.current_ossn_user %TARGETFILE%


