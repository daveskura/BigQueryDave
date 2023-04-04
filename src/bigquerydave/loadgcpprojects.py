"""
  Dave Skura, 2023

	gcloud auth application-default login

"""
import sys
import bqd
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

class gcp_projects:
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


	def load_gcp_project_resources(self):
		schwiz = schemawiz()
		service = bqd.get_service()
		resource_filename = 'project_resource.tsv'
		f = open(resource_filename,'w')
		f.write('project_id\tresourcetype\tresourceid\n')
		sql = """
		SELECT DISTINCT projectid
		FROM gcp_projects P
						LEFT JOIN project_resource R ON (P.projectid = R.project_id)
		WHERE R.project_id is null
		"""
		
		data = schwiz.dbthings.sqlite_db.query(sql)
		for row in data:
			print(row[0])
			project_id = row[0] # '596240788706'
			content = self.get_project_ancestry(service,project_id)	
			f.write(content) 
		f.close()
		print(resource_filename, ' loaded')
		
		tablename = 'project_resource'
		if schwiz.dbthings.sqlite_db.does_table_exist(tablename):
			schwiz.justload_sqlite_from_csv(resource_filename,tablename,True)
		else:
			r = schwiz.createload_sqlite_from_csv(resource_filename,tablename)

		print(tablename,' loaded')


if __name__ == '__main__':
	print('Dont run this unless serious')
	#gcp_projects().load_gcp_project_resources()
