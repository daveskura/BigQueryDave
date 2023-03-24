"""
  Dave Skura
  
  gcloud auth application-default login
	pip install --upgrade google-cloud-storage

"""
import bqd

from google.cloud import storage

class bucketshow:
	def __init__(self,action=''):
		if action != '':
			self.show()

	def get_projectids(self):
		projectids = []
		service = bqd.get_service()
		request = service.projects().list()
		response = request.execute()
		for project in response.get('projects', []):
			projectid = project['projectId']
			projectname = project['name']
			projectids.append(projectid)
			#print(projectname + ': ' + projectid)

		return projectids

	def get_buckets(self,projectid):
		storage_client = storage.Client(projectid)
		buckets = storage_client.list_buckets()
		atleastone = False
		for bucket in buckets:
			if not atleastone:
				print('You have access to these buckets:')
			atleastone = True
			print('gs://' + bucket.name)
		
		if not atleastone:
			print('There are no buckets you can access in project ' + str(projectid))

		print('')
			
		return buckets

	def show(self):
		projectids = self.get_projectids()
		itemnbr = 0
		for projectid in projectids:
			itemnbr += 1
			print(str(itemnbr) + ') ' + projectid)

		print('')
		selectnbr = int(input('select projectid: '))
		print('')

		if selectnbr <= len(projectids):
			self.get_buckets(projectids[selectnbr-1])


if __name__ == '__main__':
	bucketshow('doit') #buckets('watchful-lotus-364517')

