"""
  Dave Skura
"""

from googleapiclient.discovery import build
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

def get_service():
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
	return service