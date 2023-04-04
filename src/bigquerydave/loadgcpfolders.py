"""
  Dave Skura, 2023

	gcloud auth application-default login

"""
import sys
import bqd
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz
from google.cloud import resourcemanager_v3

class gcp_folders:
	def __init__(self): 
		self.updated='Apr 4/2023'

	# "name\tparent\tdisplay_name\tstate\tcreate_time\tupdate_time\n"
	def get_folder_details(self,client,folder_id):
		folder_name = 'folders/' + str(folder_id)
		request = resourcemanager_v3.GetFolderRequest(name=folder_name)

		# Make the request
		response = client.get_folder(request=request)

		"""
		name: "folders/30263264461"
		parent: "folders/337401936763"
		display_name: "apps-script"
		state: ACTIVE
		create_time {
			seconds: 1558617997
			nanos: 435000000
		}
		update_time {
			seconds: 1558617997
			nanos: 435000000
		}
		"""
		hdr = "id\tname\tparent\tdisplay_name\tstate\tcreate_time\tupdate_time\n"
		line = str(folder_id) + '\t'
		line += str(response.name) + '\t'
		line += str(response.parent) + '\t'
		line += str(response.display_name) + '\t'
		line += str(response.state) + '\t'
		line += str(response.create_time) + '\t'
		line += str(response.update_time) + '\n'
		return line


	def load_gcp_folder_resources(self):
		schwiz = schemawiz()
		client = resourcemanager_v3.FoldersClient()

		folder_filename = 'folder_details.tsv'
		f = open(folder_filename,'a')
		#f.write('id\tname\tparent\tdisplay_name\tstate\tcreate_time\tupdate_time\n')
		sql = """
			SELECT distinct resourceid
			FROM project_resource pr
							LEFT JOIN folder_details fd ON (pr.resourceid = fd.id)        
			WHERE resourcetype='folder'
							and fd.id is null
			limit 500
		"""
		
		data = schwiz.dbthings.sqlite_db.query(sql)
		for row in data:
			print(row[0])
			folder_id = row[0] # '30263264461'
			content = self.get_folder_details(client,folder_id)	
			f.write(content) 
		f.close()
		print(folder_filename, ' created')
		
		tablename = 'folder_details'
		if schwiz.dbthings.sqlite_db.does_table_exist(tablename):
			schwiz.justload_sqlite_from_csv(folder_filename,tablename,True)
		else:
			schwiz.createload_sqlite_from_csv(folder_filename,tablename)

		print(tablename,' loaded')


if __name__ == '__main__':
	print('Dont run this unless serious')
	gcp_folders().load_gcp_folder_resources()
