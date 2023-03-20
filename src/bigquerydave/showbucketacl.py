"""
  Dave Skura
  
  File Description:
"""
from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from google.cloud import storage

class bucketacl:
	def __init__(self,bucket_name=''): 
		self.updated='Feb 22/2023'
		if bucket_name != '':
			self.print_bucket_acl(bucket_name)

	def gcpconnect(self):
		credentials = GoogleCredentials.get_application_default()
		service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
		request = service.projects().list()
		response = request.execute()


	def print_bucket_acl(self,bucket_name):
			self.gcpconnect()

			storage_client = storage.Client()
			bucket = storage_client.bucket(bucket_name)

			for entry in bucket.acl:
					print(f"{entry['role']}: {entry['entity']}")

if __name__ == '__main__':
	bucketacl('daves-gcp-bucket')
