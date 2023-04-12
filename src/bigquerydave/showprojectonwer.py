"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
import sys
import bqd
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

class gcpowners:
	def __init__(self): 
		self.updated='April 10/2023'
		self.admin_filename = 'bigquery_admin.tsv'
		self.tablename = 'bqadmins'

	def get_bqadmins(self,project_id, version=1):
		content = ''
		try:
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
			
			#content = 'project_id \t role \t members\n'
			for binding in policy['bindings']:
				for mbr in binding['members']:
					if binding['role'].find('bigquery')>-1:
						if str(mbr).find('serviceAccount') == -1:
							content += project_id + '\t' + str(binding['role']) + '\t' + str(mbr) + '\n'
		except Exception as e:
			print(str(e))
			content = project_id + '\t The caller does not have permission \t\n'
		return content

	def loadbqadmins(self):
		schwiz = schemawiz()
		f = open(self.admin_filename,'w')
		f.write('project_id \t role \t members\n')
		sql = """
		 SELECT distinct project
		 FROM bqdatasets
		 WHERE project not like 'sys-%' and dataset not like 'has not enabled BigQuery.'
		 ORDER BY project """
		data = schwiz.dbthings.sqlite_db.query(sql)
		if data != None:
			for row in data:
				projectid = row[0]
				print(projectid)
				result = self.get_bqadmins(projectid)
				print(result)
				f.write(result)

		f.close()


if __name__ == '__main__':
	print('')
	gcpowners().loadbqadmins()


