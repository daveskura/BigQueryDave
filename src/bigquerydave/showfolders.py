"""
  Dave Skura, 2023

	gcloud auth application-default login

	pip install google-cloud-resource-manager

"""
from google.cloud import resourcemanager_v3

class gcp_folders:
	def __init__(self): 
		self.updated='Apr 3/2023'

	# "name\tparent\tdisplay_name\tstate\tcreate_time\tupdate_time\n"
	def get_folder_details(self,folder_id):
		client = resourcemanager_v3.FoldersClient()
		request = resourcemanager_v3.GetFolderRequest(name=folder_id)

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
		hdr = "name\tparent\tdisplay_name\tstate\tcreate_time\tupdate_time\n"
		line = response.name + '\t'
		line += str(response.parent) + '\t'
		line += str(response.display_name) + '\t'
		line += str(response.state) + '\t'
		line += str(response.create_time) + '\t'
		line += str(response.update_time) + '\t'
		return line


if __name__ == '__main__':
	folder_id = 'folders/30263264461'
	print('Folder ', folder_id)
	
	a = gcp_folders()
	print(a.get_folder_details(folder_id))

