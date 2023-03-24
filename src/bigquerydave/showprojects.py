"""
  Dave Skura, 2023

	gcloud auth application-default login

"""
import bqd
from google.cloud import bigquery

class gcp_projects:
	def __init__(self): 
		self.updated='Mar 16/2023'
		self.list_gcp_projects()

	def list_gcp_projects(self):
		service = bqd.get_service()
		request = service.projects().list()
		response = request.execute()
		for project in response.get('projects', []):
			projectid = project['projectId']
			projectname = project['name']
			print(projectname + ': ' + projectid)
	
if __name__ == '__main__':
	print('You have access to these projects')
	gcp_projects()
