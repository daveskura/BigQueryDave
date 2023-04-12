"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

import sys

class bqtabledefs:
	def __init__(self): 
		self.updated='April 6/2023'

	def get_bq_tabledef(self,project_id,dataset_id,tablename):

		client = bigquery.Client(project=project_id)

		table_id = project_id + '.' + dataset_id + '.' + tablename
		table = client.get_table(table_id)  # Make an API request.
		
		content = ''
		#project\tdataset_id\ttablename\tfieldname\tfieldtype\n
		for Schemafield in table.schema:
			content += project_id + '\t' + dataset_id + '\t' + tablename + '\t' + Schemafield.name + '\t' + Schemafield.field_type +'\n'

		return content


if __name__ == '__main__':
	project_id = input('projectid : ') or 'ld-ds-rmp-sandbox'
	dataset_id = input('dataset_id : ') or 'ad_details'
	table = input('table : ') or 'ad_details'
	print(bqtabledefs().get_bq_tabledef(project_id,dataset_id,table))


	