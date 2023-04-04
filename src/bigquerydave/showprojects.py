"""
  Dave Skura, 2023

	gcloud auth application-default login

"""
import sys
import bqd
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

class gcp_projects:
	def __init__(self,project_list_filename=''): 
		self.updated='Apr 3/2023'
		self.list_gcp_projects(project_list_filename)

	def list_gcp_projects(self,project_list_filename=''):
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

		if project_list_filename != '':
			f = open(project_list_filename,'w')
			f.write(filecontents) 
			f.close()

			schwiz = schemawiz()
			tablename = 'gcp_projects'
			if schwiz.dbthings.sqlite_db.does_table_exist(tablename):
				schwiz.justload_sqlite_from_csv(project_list_filename,tablename,WithTruncate)
			else:
				r = schwiz.createload_sqlite_from_csv(project_list_filename,tablename)

			print(tablename,' loaded')

		else:
			print(filecontents)


if __name__ == '__main__':
	print('You have access to these projects')
	gcp_projects('projects.tsv')
