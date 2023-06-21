@echo off

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
SET TARGET_DIR=.
SET FILE_PREFIX=logsV2

SET TARGETFILE=%TARGET_DIR%\%FILE_PREFIX%_%FILE_SUFFIX%.csv

echo extracting from us-activtrak-ac-prod.661198.logsV2

echo %TARGETFILE%

bq query --nouse_legacy_sql --format=csv "SELECT * FROM us-activtrak-ac-prod.661198.logsV2" > %TARGETFILE%

