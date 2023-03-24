"""
  Dave Skura
  
  gcloud auth application-default login
"""
import bqd

class iamshow:
	def __init__(self,action=''):
		self.policy = ''
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

	def get_policy(self,project_id, version=1):
		service = bqd.get_service()

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
		self.policy = 'role \t members\n'
		for binding in policy['bindings']:
			for mbr in binding['members']:
				self.policy += str(binding['role']) + '\t' + str(mbr) + '\n'

		return self.policy

	def savepolicyfile(self,projectid='',csvfilename='',delimiter='\t'):
		with open(csvfilename,'w') as f:
			f.write(self.get_policy(projectid))
	
	def show(self):
		projectids = self.get_projectids()
		itemnbr = 0
		for projectid in projectids:
			itemnbr += 1
			print(str(itemnbr) + ') ' + projectid)

		print('')
		selectnbr = int(input('select projectid: '))

		if selectnbr <= len(projectids):
			print('')
			selectyn = input('Save to file y/n ? ')
			print('')
			if selectyn.upper() == 'Y':
				csvfilename = input('filename ? (' + projectids[selectnbr-1] + '_iam.csv' + '): ')
				if csvfilename == '':
					csvfilename = projectids[selectnbr-1] + '_iam.csv'
				print('')
				self.savepolicyfile(projectids[selectnbr-1],csvfilename)

			else:
				print(self.get_policy(projectids[selectnbr-1]))

if __name__ == '__main__':
	x = iamshow('doit')
	#print(x.get_policy('watchful-lotus-364517'))
	#x.savepolicyfile('watchful-lotus-364517','out.csv')
	

