"""
  Dave Skura
  
  File Description:
"""
from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account
import os

print (" Starting ") # 

class iam:
	def __init__(self,project_id=''):
		if project_id != '':
			self.get_policy(project_id)

	def get_policy(self,project_id, version=1):
		credentials = GoogleCredentials.get_application_default()
		service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
		request = service.projects().list()
		response = request.execute()

		policy = (
				service.projects()
				.getIamPolicy(
						resource=project_id,
						body={"options": {"requestedPolicyVersion": version}},
				)
				.execute()
		)
		self.printthing(policy,'version')
		self.printthing(policy,'etag')
		for binding in policy['bindings']:
			print('')
			self.printthing(binding,'role')
			self.printthing(binding,'members')
			self.printthing(binding,'role')

		return policy
	def printthing(self,jsoner,tag):
		print(tag + ': ' + str(jsoner[tag]))

if __name__ == '__main__':
	iam('watchful-lotus-364517')

