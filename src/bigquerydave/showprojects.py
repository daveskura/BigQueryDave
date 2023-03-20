"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account
from google.cloud import bigquery
import sys


class gcp_projects:
	def __init__(self): 
		self.updated='Mar 16/2023'
		self.get_service()
		self.list_gcp_projects()

	def get_service(self):
		credentials = GoogleCredentials.get_application_default()
		if credentials.create_scoped_required():
			credentials = credentials.create_scoped('https://www.googleapis.com/auth/bigquery')
		return build('bigquery','v2', credentials=GoogleCredentials.get_application_default())

	def list_gcp_projects(self):
		credentials = GoogleCredentials.get_application_default()
		service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
		request = service.projects().list()
		response = request.execute()
		for project in response.get('projects', []):
			projectid = project['projectId']
			projectname = project['name']
			print(projectname + ': ' + projectid)
	
if __name__ == '__main__':
	print('You have access to these projects')
	gcp_projects()
