"""
  Dave Skura
  
  gcloud auth application-default login
	pip install --upgrade google-cloud-storage

"""
import bqd
from google.cloud import storage
from schemawizard_package.schemawizard import schemawiz

class gcsbuckets:
	def __init__(self):
		self.updated = 'April 11,2023'

	def get_bucket_details(self,projectid,bucketname=''):
		try:
			storage_client = storage.Client(projectid)
			buckets = storage_client.list_buckets()
			content = ''
			atleastone = False
			for bucket in buckets:
				#'project\tbucket\tstorageclass\tfilenanme\tsize\n'
				if bucketname == '' or (bucketname != '' and bucketname == bucket.name):
					atleastone = True
					blobs = bucket.list_blobs()
					size_multi_regional = size_regional = size_nearline = size_coldline = 0
					for blob in blobs:
						content += projectid+'\t'+bucket.name+'\t'+blob.storage_class+'\t'+blob.name + '\t' + str(blob.size) + '\n'

			if not atleastone:
				content = projectid+'\tno buckets\t\t\t\n'

		except Exception as e:
			#print(str(e))
			content = projectid+'\tno bucket access\t\t\t\n'

		return content
	
	def load_table(self):
		schwiz = schemawiz()
		bucketfilename = 'gcsbuckets.tsv'
		tablename = 'gcsbuckets'

		if schwiz.dbthings.sqlite_db.does_table_exist(tablename):
			schwiz.justload_sqlite_from_csv(bucketfilename,tablename,True)
		else:
			r = schwiz.createload_sqlite_from_csv(bucketfilename,tablename)

		print(tablename,' loaded')

	def loadbuckets(self,project_id='',bucketname='',missingonly=True):
		schwiz = schemawiz()
		sql = """
			SELECT P.projectid
			FROM gcp_projects P
			WHERE P.projectid not like 'sys%' AND P.projectid like '%lake%'
		"""

		bucketfilename = 'gcsbuckets.tsv'
		if missingonly:
			sql += 	" AND P.projectid not in (SELECT DISTINCT project FROM gcsbuckets) "
			f = open(bucketfilename,'a')
		else:
			f = open(bucketfilename,'w')
			f.write('project\tbucket\tstorageclass\tfilenanme\tsize\n')

		data = schwiz.dbthings.sqlite_db.query(sql)
		for row in data:
			f.write(self.get_bucket_details(row[0],bucketname))

		f.close()

		self.loadtable()		

	def showmissingprojects(self):
		schwiz = schemawiz()
		sql = """
			SELECT P.projectid
			FROM gcp_projects P
			WHERE P.projectid not like 'sys%' 
					AND P.projectid not in (SELECT DISTINCT project FROM gcsbuckets)
		"""
		sql2 = """
			SELECT count(distinct P.projectid)
			FROM gcp_projects P
			WHERE P.projectid not like 'sys%' 
					AND P.projectid not in (SELECT DISTINCT project FROM gcsbuckets)
		"""

		print(schwiz.dbthings.sqlite_db.export_query_to_str(sql))
		print('projects to do:' + str(schwiz.dbthings.sqlite_db.queryone(sql2)))

if __name__ == '__main__':
	print('1. Create/Overwrite buckets into gcsbuckets.tsv for all projects in gcp_projects.')
	print('2. Append buckets for projects missing from gcsbuckets only.')
	print('3. Show projects in gcp_projects, missing from gcsbuckets.')
	print('4. Create/Overwrite table gcsbuckets from gcsbuckets.tsv.')
	print('5. Cancel.')

	selectchar = input('select (1,2,3,4): ') or '4'
	print('')
	if selectchar.upper() == '1':
		print('Create/Overwrite file gcsbuckets.tsv for all projects in gcp_projects.')
		gcsbuckets().loadbuckets('','',False) 

	elif selectchar.upper() == '2':
		print('Append buckets for projects missing from gcsbuckets only.')
		gcsbuckets().loadbuckets('','',True) 

	elif selectchar.upper() == '3':
		print('Show projects in gcp_projects, missing from gcsbuckets.')
		gcsbuckets().showmissingprojects()

	elif selectchar.upper() == '4':
		print('Create/Load table gcsbuckets from gcsbuckets.tsv.')
		gcsbuckets().load_table()

	else:
		print('Do Nothing')
