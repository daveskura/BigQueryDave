@echo off

REM ----- SOURCE
SET SOURCE_DIR=./*.csv

REM ----- TARGET
SET TARGET_DIR=gs://dtc456/FileAudit

echo Load daily csv files
echo on
DIR *.csv

gsutil mv %SOURCE_DIR% %TARGET_DIR%
