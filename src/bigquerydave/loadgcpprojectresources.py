"""
  Dave Skura, 2023

	gcloud auth application-default login
	py -m bigquerydave_package.loadgcpprojects
"""
import sys
import bqd
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

class gcp_projectresources:
	def __init__(self): 
		self.updated='Apr 3/2023'

	def get_project_ancestry(self,service,project_id):

		dets = (
				service.projects()
				.getAncestry(
						projectId=project_id
				)
				.execute()
		)
		ancestor = dets['ancestor']
		content = '' #'project_id\tresourcetype\tresourceid\n'
		for resource in ancestor:
			type = resource['resourceId']['type']
			id = resource['resourceId']['id']
			content += project_id + '\t' + type + '\t' + id + '\n'
		
		return content


	def load_gcp_project_resources(self,missingonly=False):
		schwiz = schemawiz()
		service = bqd.get_service()
		resource_filename = 'project_resource.tsv'
		if missingonly:
			f = open(resource_filename,'a')
		else:
			f = open(resource_filename,'w')

		f.write('project_id\tresourcetype\tresourceid\n')
		sql = """
		SELECT DISTINCT P.projectid
		FROM gcp_projects P """
		if missingonly:
			sql += """
					LEFT JOIN project_resource R ON (P.projectid = R.project_id)
				WHERE R.project_id is null
			"""
		
		data = schwiz.dbthings.postgres_db.query(sql)
		for row in data:
			print(row[0])
			project_id = row[0] # '596240788706'
			content = self.get_project_ancestry(service,project_id)	
			f.write(content) 
		f.close()
		print(resource_filename, ' loaded')

	def load_table(self):
		schwiz = schemawiz()
		tablename = 'project_resource'
		resource_filename = 'project_resource.tsv'
		if schwiz.dbthings.postgres_db.does_table_exist(tablename):
			schwiz.justload_postgres_from_csv(resource_filename,tablename,True)
		else:
			r = schwiz.createload_postgres_from_csv(resource_filename,tablename)

		print(tablename,' loaded')


if __name__ == '__main__':
	print('1. Create/Load resources into project_resource.tsv')
	print('2. Create/Load table project_resource from project_resource.tsv')
	print('3. Cancel.')

	selectchar = input('select (1,2,3): ') or '3'
	print('')
	if selectchar.upper() == '1':
		print('Create/Load resources into project_resource.tsv')
		gcp_projectresources().load_gcp_project_resources(False)
	elif selectchar.upper() == '2':
		print('Create/Load table project_resource from project_resource.tsv')
		gcp_projectresources().load_table()
	else:
		print('do nothing')

