"""
  Dave Skura
  
  File Description:
"""

from google.cloud import bigquery

client = bigquery.Client()

dataset_id = 'cosmic-ascent-364921.dataset1234'

tables = client.list_tables(dataset_id)  

for table in tables:
    print(table.project, table.dataset_id, table.table_id)