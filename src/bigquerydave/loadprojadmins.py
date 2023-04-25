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
					if binding['role'].find('bigquery')>-1 or binding['role'].find('admin')>-1:
						if str(mbr).find('serviceAccount') == -1:
							content += project_id + '\t' + str(binding['role']) + '\t' + str(mbr) + '\n'
		except Exception as e:
			print(str(e))
			content = project_id + '\t The caller does not have permission \t\n'
		return content

	def loadprojadmins(self,missingonly=False):
		schwiz = schemawiz()
		if missingonly:
			f = open(self.admin_filename,'a')
		else:
			f = open(self.admin_filename,'w')
			f.write('project_id \t role \t members\n')
		
		sql = """
		 SELECT project_id
		 FROM ourprojects
		 """
		if missingonly:
			sql += ' AND project_id NOT IN (SELECT DISTINCT project_id from bqadmins) '
		sql += " ORDER BY project_id"
		data = schwiz.dbthings.postgres_db.query(sql)
		if data != None:
			for row in data:
				projectid = row[0]
				print(projectid)
				result = self.get_bqadmins(projectid)
				print(result)
				f.write(result)

		f.close()

	def loadtable(self):
		schwiz = schemawiz()

		if schwiz.dbthings.postgres_db.does_table_exist(self.tablename):
			schwiz.justload_postgres_from_csv(self.admin_filename,self.tablename,True)
		else:
			r = schwiz.createload_postgres_from_csv(self.admin_filename,self.tablename)

		print(self.tablename,' loaded')

if __name__ == '__main__':
	print('1. Create file bigquery_admin.tsv from all projects in bqdatasets with datasets')
	print('2. Append to bigquery_admin.tsv with projects in bqdatasets with datasets not in bqadmins.')
	print('3. Load file bigquery_admin.tsv to table bqadmins.')
	print('4. Cancel.')

	selectchar = input('select (1,2,3): ') or '3'
	print('')
	if selectchar.upper() == '1':
		print('Create file bigquery_admin.tsv from all projects in bqdatasets with datasets.')
		gcpowners().loadprojadmins(False)
	elif selectchar.upper() == '2':
		print('Append to bigquery_admin.tsv with projects in bqdatasets with datasets not in bqadmins.')
		gcpowners().loadprojadmins(True)
	elif selectchar.upper() == '3':
		print('Load file bigquery_admin.tsv to table bqadmins.')
		gcpowners().loadtable()
	else:
		print('do nothing')
