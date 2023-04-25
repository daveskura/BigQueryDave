"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

import sys

class bqsamples:
	def __init__(self): 
		self.updated='April 12/2023'

	def sample_table(self,project_id='',dataset_id='',tablename=''):
 
		table_id = project_id + '.' + dataset_id + '.' + tablename
		client = bigquery.Client()
		rows_iter = client.list_rows(table_id, max_results=1)
		rows = list(rows_iter)
		content = ''
		for r in rows:
			line = ''
			for cols in range(0,len(r)):
				line += str(r[cols]) + '\t'
			line = line[:-2] + '\n'
			content += line

		print(content)


if __name__ == '__main__':
	project = input('project : ') or 'lt-dia-lake-prd-consume'
	dataset = input('dataset : ') or 'merchandising_pricing'
	tablename = input('tablename : ') or 'inventory_value_store_snpsht_duplicate'

	bqsamples().sample_table(project,dataset,tablename)

	

