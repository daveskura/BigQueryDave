"""
  Dave Skura, 2023

	gcloud auth application-default login
	py -m bigquerydave_package.loadgcpprojects
"""
import sys
import bqd
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

class gcp_projects:
	def __init__(self): 
		self.updated='Apr 3/2023'

	def list_gcp_projects(self):
		project_list_filename='projects.tsv'
		service = bqd.get_service()
		request = service.projects().list()

		filecontents = 'projectNumber\tprojectId\tlifecycleState\tname\tcreateTime\tparent_type\tparent_id\n'
		while request is not None:
			response = request.execute()
			for project in response.get('projects', []):
				line = project['projectNumber'] + '\t'
				line += project['projectId'] + '\t'
				line += project['lifecycleState'] + '\t'
				line += project['name'] + '\t'
				line += project['createTime'] + '\t'
				line += project['parent']['type'] + '\t'
				line += project['parent']['id'] + '\n'
				filecontents += line
			request = service.projects().list_next(previous_request=request, previous_response=response)

		f = open(project_list_filename,'w')
		f.write(filecontents) 
		f.close()

	def load_table(self):
			schwiz = schemawiz()
			project_list_filename='projects.tsv'
			tablename = 'gcp_projects'
			if schwiz.dbthings.postgres_db.does_table_exist(tablename):
				schwiz.justload_postgres_from_csv(project_list_filename,tablename,True)
			else:
				r = schwiz.createload_postgres_from_csv(project_list_filename,tablename)

			print(tablename,' loaded')

if __name__ == '__main__':
	print('1. Create/Load projects into projects.tsv')
	print('2. Create/Load table gcp_projects from projects.tsv')
	print('3. Cancel.')

	selectchar = input('select (1,2,3): ') or '3'
	print('')
	if selectchar.upper() == '1':
		print('Create/Load projects into projects.tsv')
		gcp_projects().list_gcp_projects()
	elif selectchar.upper() == '2':
		print('Create/Load table gcp_projects from projects.tsv')
		gcp_projects().load_table()
	else:
		print('do nothing')
