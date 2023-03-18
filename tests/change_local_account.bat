@echo off
REM
REM  Dave Skura, 2023
REM 
REM  run gcloud init to setup configuration

set configuration=sqlmaster7
set gcpemail=sqlmaster7@gmail.com
set gcpproject=cosmic-ascent-364921

call gcloud config configurations activate %configuration%
call gcloud config set account %gcpemail%
call gcloud config set project %gcpproject%


