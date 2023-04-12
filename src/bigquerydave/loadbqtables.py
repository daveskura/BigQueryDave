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
		print(project_id,'.',dataset_id)
		client = bigquery.Client(project=project_id)
		try:
			tables = client.list_tables(dataset_id)  

			content = ''
			#project_id \t dataset_id \t table_id \t location \t partitioning_type \t range_partitioning \t require_partition_filter \t time_partitioning \t clustering_fields \t num_rows \t num_bytes \t expires \t description

			atleastone = False
			for onetable in tables:
				atleastone = True
				tableref = client.get_table(onetable)  # Make an API request.
				content += onetable.project + '\t' + onetable.dataset_id + '\t' + onetable.table_id + '\t' 
				content += str(tableref.location).replace('\t','').replace('\n',' ') + '\t'

				content += str(tableref.partitioning_type).replace('\t','').replace('\n',' ') + '\t' 
				content += str(tableref.range_partitioning).replace('\t','').replace('\n',' ') + '\t' 
				content += str(tableref.require_partition_filter).replace('\t','').replace('\n',' ') + '\t' 
				content += str(tableref.time_partitioning).replace('\t','').replace('\n',' ') + '\t' 
				content += str(tableref.clustering_fields).replace('\t','').replace('\n',' ') + '\t' 

				content += str(tableref.num_rows).replace('\t','').replace('\n',' ') + '\t' 
				content += str(tableref.num_bytes).replace('\t','').replace('\n',' ') + '\t' 
				content += str(tableref.expires).replace('\t','').replace('\n',' ') + '\t'
				content += str(tableref.description).replace('\t','').replace('\n',' ') + '\n'

			if not atleastone:
				content = project_id + '\t' + dataset_id + '\t none \t \t \t\t\t\t\t \t\t\t\n'

		except:
			content = project_id + '\t' + dataset_id + '\t none \t \t \t\t\t\t\t \t\t\t\n'

		return content

	def showmissingdatasets(self):
		schwiz = schemawiz()
		sql = """
		SELECT project,dataset
		FROM bqdatasets D
		WHERE dataset not like '%not enabled%' and dataset not like '%temp_dataset_beam%'
				AND project||'.'||dataset NOT IN (SELECT DISTINCT project_id||'.'||dataset_id FROM bqtables) """
		sql2 = """
		SELECT count(*)
		FROM bqdatasets D
		WHERE dataset not like '%not enabled%' and dataset not like '%temp_dataset_beam%'
				AND project||'.'||dataset NOT IN (SELECT DISTINCT project_id||'.'||dataset_id FROM bqtables) """
		print(schwiz.dbthings.postgres_db.export_query_to_str(sql))
		print('projects to do:' + str(schwiz.dbthings.postgres_db.queryone(sql2)))


	def load_bq_tables(self,missingonly=False):
		schwiz = schemawiz()
		bqtable_filename = 'bqtables.csv'
		if not missingonly:
			f = open(bqtable_filename,'w')
			hdr = "project_id\tdataset_id\ttable_id\tlocation\tpartitioning_type\trange_partitioning\trequire_partition_filter\ttime_partitioning\tclustering_fields\tnum_rows\tnum_bytes\texpires\tdescription\n"
			f.write(hdr)
		else:
			f = open(bqtable_filename,'a')

		sql = """
		SELECT DISTINCT project,dataset
		FROM bqdatasets D
		WHERE dataset not like '%not enabled%' AND project like '%d%' and dataset not like '%temp_dataset_beam%' 
		"""
		if missingonly:
			sql += " 			AND project||'.'||dataset NOT IN (SELECT DISTINCT project_id||'.'||dataset_id FROM bqtables) "

		#sql += ' limit 10'
		data = schwiz.dbthings.postgres_db.query(sql)
		if data != None:
			for row in data:
				projectid = row[0]
				datasetid = row[1]
				bqtables = self.get_bq_tables(projectid,datasetid)
		
				if bqtables != '':
					f.write(bqtables)

		f.close()

		print(bqtable_filename, ' loaded')
	def load_table(self):
		schwiz = schemawiz()
		bqtable_filename = 'bqtables.csv'
		tablename = 'bqtables'

		if schwiz.dbthings.postgres_db.does_table_exist(tablename):
			schwiz.justload_postgres_from_csv(bqtable_filename,tablename,True)
		else:
			r = schwiz.createload_postgres_from_csv(bqtable_filename,tablename)

		print(tablename,' loaded')

if __name__ == '__main__':
	print('1. Create/Load tables in bqtables.csv for all datasets in bqdatasets.')
	print('2. Append tables in bqtables.csv for the datasets missing from table bqtables only.')
	print('3. Show datasets in bqdatasets, missing from bqtables.')
	print('4. Create/Load table bqtables from bqtables.csv')

	print('5. Cancel.')

	selectchar = input('select (1,2,3,4,5): ') or '5'
	print('')
	if selectchar.upper() == '1':
		print('Create/Load tables in bqtables.csv for all datasets in bqdatasets.')
		bqtables().load_bq_tables(False)
	elif selectchar.upper() == '2':
		print('Append tables in bqtables.csv for the datasets missing from table bqtables only.')
		bqtables().load_bq_tables(True)
	elif selectchar.upper() == '3':
		print('Show datasets in bqdatasets, missing from bqtables.')
		bqtables().showmissingdatasets()
	elif selectchar.upper() == '4':
		print('Create/Load table bqtables from bqtables.csv.')
		bqtables().load_table()
	else:
		print('do nothing')



