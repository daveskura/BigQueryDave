# BigQueryDave

A wrapper on the bigquery libraries for simple access

### Install with pip

pip install bigquerydave_package

### import to your python script

from bigquerydave_package.bigquerydave import gcp
from bigquerydave_package.bigquerydave import bq

### try methods

#### gcp().list_gcp_projects()
#### bq().list_bq_datasets()
#### bq().list_bq_tables('watchful-lotus-364517.dave')
#### bq().estimate_query('SELECT CURRENT_TIMESTAMP')
