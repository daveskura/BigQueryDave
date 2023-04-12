"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery
import sys
from schemawizard_package.schemawizard import schemawiz


class gcpdatasets:
	def __init__(self): 
		self.updated='April 5/2023'

	#project\tdataset
	def get_datasets(self,project_id):
		client = bigquery.Client(project=project_id)
		gotsomedata = False

		try:
			datasets = list(client.list_datasets())  # Make an API request.
			project = client.project
			content = ''
			if datasets:
				gotsomedata = True
				for dataset in datasets:
					content += dataset.project + '\t' + dataset.dataset_id + '\n'
		except Exception as e:
			print(str(e))

		if not gotsomedata:
			content = project_id + '\t' + ' has not enabled BigQuery.'+ '\n'

		return content

	def showmissingprojectss(self):
		schwiz = schemawiz()
		sql = """
			SELECT projectid
			FROM gcp_projects
			WHERE projectid not like 'sys%'
				AND projectid NOT IN (SELECT project FROM bqdatasets) """
		sql2 = """
			SELECT count(distinct projectid)
			FROM gcp_projects
			WHERE projectid not like 'sys%'
				AND projectid NOT IN (SELECT project FROM bqdatasets) """
		print(schwiz.dbthings.postgres_db.export_query_to_str(sql))
		print('projects to do:' + str(schwiz.dbthings.postgres_db.queryone(sql2)))

	def load_bq_datasets(self,missingonly=False):
		schwiz = schemawiz()
		dataset_filename = 'bqdatasets.csv'
		if not missingonly:
			f = open(dataset_filename,'w')
			f.write('project\tdataset\n')
		else:
			f = open(dataset_filename,'a')

		sql = """
			SELECT projectid
			FROM gcp_projects
			WHERE projectid not like 'sys%'
		"""
		if missingonly:
			sql += ' 			AND projectid NOT IN (SELECT project FROM bqdatasets) '

		data = schwiz.dbthings.postgres_db.query(sql)
		if data != None:
			for row in data:
				projectid = row[0]
				datasets = self.get_datasets(projectid)
		
				if datasets != '':
					f.write(datasets)

		f.close()
		print(dataset_filename, ' loaded')

	def load_table(self):
		schwiz = schemawiz()
		dataset_filename = 'bqdatasets.csv'
		tablename = 'bqdatasets'

		if schwiz.dbthings.postgres_db.does_table_exist(tablename):
			schwiz.justload_postgres_from_csv(dataset_filename,tablename,True)
		else:
			r = schwiz.createload_postgres_from_csv(dataset_filename,tablename)

		print(tablename,' loaded')


if __name__ == '__main__':
	print('Dont run this dataset load unless serious.')
	print('')
	print('1. Create/Load datasets into bqdatasets.csv for all projects in gcp_projects.')
	print('2. Append bqdatasets in bqdatasets.csv for projects missing from bqdatasets only.')
	print('3. Show projects in gcp_projects, missing from bqdatasets table.')
	print('4. Create/Load table bqdatasets from bqdatasets.csv')
	print('5. Cancel.')

	selectchar = input('select (1,2,3,4): ') or '4'
	print('')
	if selectchar.upper() == '1':
		print('Load datasets into bqdatasets for all projects in gcp_projects.')
		gcpdatasets().load_bq_datasets(False)
	elif selectchar.upper() == '2':
		print('Append bqdatasets for projects missing from bqdatasets only.')
		gcpdatasets().load_bq_datasets(True)
	elif selectchar.upper() == '3':
		print('Show projects in gcp_projects, missing from bqdatasets.')
		gcpdatasets().showmissingprojectss()	
	elif selectchar.upper() == '4':
		print('Create/Load table bqdatasets from bqdatasets.csv')
		gcpdatasets().load_table()
	else:
		print('do nothing')


	


