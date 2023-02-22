"""
  Dave Skura
  
  File Description:
"""

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account

credentials = GoogleCredentials.get_application_default()
service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
request = service.projects().list()
response = request.execute()
for project in response.get('projects', []):
	print(project['projectId'])

