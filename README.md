# A wrapper on the bigquery libraries for simple access

### Google install

'''
pip install google
pip install google-api-python-client
pip install --upgrade google-api-python-client
pip3 install --upgrade oauth2client 

pip install --upgrade google-cloud
pip install --upgrade google-cloud-bigquery

gcloud auth application-default login

gcloud init 
'''

### Install with pip

pip install bigquerydave

### import to your python script

from bigquerydave_package.bigquerydave import gcp

from bigquerydave_package.bigquerydave import bq

### try methods

  gcp().list_gcp_projects()
  
  bq().list_bq_datasets()
  
  bq().list_bq_tables('watchful-lotus-364517.dave')
  
  bq().estimate_query('SELECT CURRENT_TIMESTAMP')
