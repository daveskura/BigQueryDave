"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account
from google.cloud import bigquery
import sys

class gcp:
	def __init__(self): 
		self.updated='Feb 22/2023'

	def list_bq_tables(self,dataset_id):
		client = bigquery.Client()

		tables = client.list_tables(dataset_id)  

		for table in tables:
			print(table.project, table.dataset_id, table.table_id)

	def list_bq_datasets(self):
		client = bigquery.Client()

		datasets = list(client.list_datasets())  # Make an API request.
		project = client.project

		if datasets:
			print('project: ' + project)
			for dataset in datasets:
				print('\tdataset: ' + dataset.dataset_id)
		
	def list_gcp_projects(self):
		credentials = GoogleCredentials.get_application_default()
		#print(credentials.to_json())
		#sys.exit(0)
		service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
		request = service.projects().list()
		response = request.execute()
		for project in response.get('projects', []):
			print(project['projectId'])
	
if __name__ == '__main__':
	print ("db command line") # 
	print('')
	mygcp = gcp()
	print(' projects:')
	mygcp.list_gcp_projects()

	print('\n datasets:')
	mygcp.list_bq_datasets()

	print('\n tables:')
	mygcp.list_bq_tables('watchful-lotus-364517.dave')



