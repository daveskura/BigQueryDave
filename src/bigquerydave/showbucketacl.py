"""
  Dave Skura
  
  File Description:
"""
import bqd

from google.cloud import storage

class bucketaclshow:
	def __init__(self,action=''):
		self.storage_client = None
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
		self.storage_client = storage.Client(projectid)
		buckets = []
		for buck in self.storage_client.list_buckets():
			buckets.append(buck.name)
		
		return buckets

	def print_bucket_acl(self,bucket_name):
		bucket = self.storage_client.bucket(bucket_name)

		for entry in bucket.acl:
			print(f"{entry['role']}: {entry['entity']}")

	def bucket_has_acl(self,bucket_name):
		bucket = self.storage_client.get_bucket(bucket_name)
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
			return False
		else:
			print(
					f"Uniform bucket-level access is disabled for {bucket.name}."
			)
			return True

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
			buckets = self.get_buckets(projectids[selectnbr-1])

			atleastone = False
			itemnbr = 0
			for bucket in buckets:
				itemnbr += 1
				if not atleastone:
					print('You have access to these buckets:')
				atleastone = True
				print(str(itemnbr) + ') ' + 'gs://' + bucket)

			if atleastone:
				print('')
				selectnbr = int(input('select bucket: '))
				print('')
				if self.bucket_has_acl(buckets[selectnbr-1]):
					self.print_bucket_acl(buckets[selectnbr-1])
			else:
				print('There are no buckets you can access in project ' + str(projectid))

			print('')


if __name__ == '__main__':
	bucketaclshow('doit') #buckets('watchful-lotus-364517')

