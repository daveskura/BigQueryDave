"""
  Dave Skura
  
  File Description:
"""
from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from google.cloud import storage

class buckets:
	def __init__(self,action=''):
		if action != '':
			self.list_buckets()

	def gcpconnect(self):
		credentials = GoogleCredentials.get_application_default()
		service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
		request = service.projects().list()
		response = request.execute()

	def list_buckets(self):
		self.gcpconnect()
		storage_client = storage.Client()
		buckets = storage_client.list_buckets()
		for bucket in buckets:
			print(bucket.name)

if __name__ == '__main__':
	buckets('show')

