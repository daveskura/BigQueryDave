"""
  Dave Skura
  
  File Description:
"""
from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from google.cloud import storage

class bucketula:
	def __init__(self,bucket_name=''): 
		self.updated='Feb 22/2023'
		if bucket_name != '':
			self.print_bucket_ula(bucket_name)

	def gcpconnect(self):
		credentials = GoogleCredentials.get_application_default()
		service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
		request = service.projects().list()
		response = request.execute()


	def print_bucket_ula(self,bucket_name):
		self.gcpconnect()

		storage_client = storage.Client()
		bucket = storage_client.get_bucket(bucket_name)
		iam_configuration = bucket.iam_configuration

		if iam_configuration.uniform_bucket_level_access_enabled:
			print(
					f"Uniform bucket-level access is enabled for {bucket.name}."
			)
			print(
				"Bucket will be locked on {}.".format(
						iam_configuration.uniform_bucket_level_access_locked_time
				)
			)
		else:
			print(
					f"Uniform bucket-level access is disabled for {bucket.name}."
			)


if __name__ == '__main__':
	bucketula('daves-gcp-bucket')




