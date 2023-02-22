"""
  Dave Skura
  
  File Description:
"""

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

datasets = list(client.list_datasets())  # Make an API request.
project = client.project

if datasets:
    print('project: ' + project)
    for dataset in datasets:
        print('\tdataset: ' + dataset.dataset_id)
