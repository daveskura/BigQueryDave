"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

import sys

class bqtables:
	def __init__(self): 
		self.updated='April 6/2023'

	def get_bq_tables(self,project_id,dataset_id):
		client = bigquery.Client(project=project_id)

		tables = client.list_tables(dataset_id)  
		content = ''
		#project \t dataset_id \t table \t location \t partitioning_type \t range_partitioning \t require_partition_filter \t time_partitioning \t clustering_fields \t num_rows \t num_bytes \t expires \t description
		for onetable in tables:
			tableref = client.get_table(onetable)  # Make an API request.
			content += onetable.project + '\t' + onetable.dataset_id + '\t' + onetable.table_id + '\t' 
			content += str(tableref.location).replace('\t','') + '\t'

			content += str(tableref.partitioning_type).replace('\t','') + '\t' 
			content += str(tableref.range_partitioning).replace('\t','') + '\t' 
			content += str(tableref.require_partition_filter).replace('\t','') + '\t' 
			content += str(tableref.time_partitioning).replace('\t','') + '\t' 
			content += str(tableref.clustering_fields).replace('\t','') + '\t' 

			content += str(tableref.num_rows).replace('\t','') + '\t' 
			content += str(tableref.num_bytes).replace('\t','') + '\t' 
			content += str(tableref.expires).replace('\t','') + '\t'
			content += str(tableref.description).replace('\t','') + '\n'



			print(content)
			sys.exit(0)

		return content


if __name__ == '__main__':
	project_id = input('projectid : ') or 'ld-ds-rmp-sandbox'
	dataset_id = input('dataset_id : ') or 'ad_details'
	print(bqtables().get_bq_tables(project_id,dataset_id))

	




