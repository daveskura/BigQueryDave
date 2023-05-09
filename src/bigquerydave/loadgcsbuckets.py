"""
  Dave Skura
  
  gcloud auth application-default login
	pip install --upgrade google-cloud-storage

"""
import bqd
from google.cloud import storage
from schemawizard_package.schemawizard import schemawiz

class projectbuckets:
	def __init__(self):
		self.updated = 'April 11,2023'

	def get_buckets(self,projectid):
		try:
			storage_client = storage.Client(projectid)
			buckets = storage_client.list_buckets()
			content = ''
			atleastone = False
			for bucket in buckets:
				#'project\tbucket\n'
				if bucketname == '' or (bucketname != '' and bucketname == bucket.name):
					atleastone = True
					print(bucket.name)
					content += projectid+'\t'+bucket.name + '\n'

			if not atleastone:
				content = projectid+'\tno buckets\n'

		except Exception as e:
			#print(str(e))
			content = projectid+'\tno bucket access\n'

		return content
	
	def load_table(self):
		schwiz = schemawiz()
		bucketfilename = 'projectbuckets.tsv'
		tablename = 'projectbuckets'

		if schwiz.dbthings.postgres_db.does_table_exist(tablename):
			schwiz.justload_postgres_from_csv(bucketfilename,tablename,True)
		else:
			r = schwiz.createload_postgres_from_csv(bucketfilename,tablename)

		print(tablename,' loaded')

	def loadbuckets(self,project_id='',missingonly=True):
		schwiz = schemawiz()
		sql = """
			
			SELECT P.projectid
			FROM gcp_projects P
				INNER JOIN (SELECT project_id as projectid FROM ourprojects)L USING (projectid)
			WHERE P.projectid not like 'sys%' AND P.projectid like '%lake%'
			 and (P.projectid like '%lake%')

		"""

		bucketfilename = 'projectbuckets.tsv'
		if missingonly:
			sql += 	" AND P.projectid not in (SELECT DISTINCT project FROM projectbuckets) "
			f = open(bucketfilename,'a')
		else:
			f = open(bucketfilename,'w')
			f.write('project\tbucket\n')

		data = schwiz.dbthings.postgres_db.query(sql)
		for row in data:
			f.write(self.get_buckets(row[0]))

		f.close()

		self.load_table()		

	def showmissingprojects(self):
		schwiz = schemawiz()
		sqlbase = """
			FROM gcp_projects P
				INNER JOIN (SELECT project_id as projectid FROM ourprojects)L USING (projectid)

			WHERE P.projectid not like 'sys%' 
				  AND  (P.projectid like '%lake%')
					AND P.projectid not in (SELECT DISTINCT project FROM projectbuckets)
		"""
		sql = 'SELECT P.projectid ' + sqlbase
		sql2 = 'SELECT count(distinct P.projectid) ' + sqlbase

		print(schwiz.dbthings.postgres_db.export_query_to_str(sql))
		print('projects to do:' + str(schwiz.dbthings.postgres_db.queryone(sql2)))

if __name__ == '__main__':
	print('1. Create/Overwrite buckets into projectbuckets.tsv for all projects in gcp_projects.')
	print('2. Append buckets for projects missing from projectbuckets only.')
	print('3. Show projects in gcp_projects, missing from projectbuckets.')
	print('4. Create/Overwrite table projectbuckets from projectbuckets.tsv.')
	print('5. Cancel.')

	selectchar = input('select (1,2,3,4): ') or '4'
	print('')
	if selectchar.upper() == '1':
		print('Create/Overwrite file projectbuckets.tsv for all projects in gcp_projects.')
		projectbuckets().loadbuckets('',False) 

	elif selectchar.upper() == '2':
		print('Append buckets for projects missing from projectbuckets only.')
		projectbuckets().loadbuckets('',True) 

	elif selectchar.upper() == '3':
		print('Show projects in gcp_projects, missing from projectbuckets.')
		projectbuckets().showmissingprojects()

	elif selectchar.upper() == '4':
		print('Create/Load table projectbuckets from projectbuckets.tsv.')
		projectbuckets().load_table()

	else:
		print('Do Nothing')
