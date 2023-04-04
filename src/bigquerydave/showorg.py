"""
  Dave Skura, 2023

	gcloud auth application-default login

"""
import bqd

class gcp_project_ancestry:
	def __init__(self): 
		self.updated='Apr 3/2023'

	#'resourcetype\tresourceid\n'
	def get_project_ancestry(self,project_id):
		service = bqd.get_service()

		dets = (
				service.projects()
				.getAncestry(
						projectId=project_id
				)
				.execute()
		)
		ancestor = dets['ancestor']
		content = '' #'resourcetype\tresourceid\n'
		for resource in ancestor:
			type = resource['resourceId']['type']
			id = resource['resourceId']['id']
			content += type + '\t' + id + '\n'
		
		return content

		"""
		{
			'ancestor': [	{'resourceId': {'type': 'project', 'id': 'sys-17129398924880695740455381'}}, 
										{'resourceId': {'type': 'folder', 'id': '30263264461'}}, 
										{'resourceId': {'type': 'folder', 'id': '337401936763'}}, 
										{'resourceId': {'type': 'organization', 'id': '494667196037'}}
									]
		}
		"""


if __name__ == '__main__':
	project_id = '596240788706'
	print('Project ancestry for ', project_id)
	
	a = gcp_project_ancestry()
	print(a.get_project_ancestry(project_id))

