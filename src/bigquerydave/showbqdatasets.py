"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery
import sys
from schemawizard_package.schemawizard import schemawiz


class gcpdatasets:
	def __init__(self): 
		self.updated='April 5/2023'

	def showds(Self,project_id,dataset_id):
		client = bigquery.Client(project=project_id)
		dataset = client.get_dataset(dataset_id)  # Make an API request.

		full_dataset_id = "{}.{}".format(dataset.project, dataset.dataset_id)
		friendly_name = dataset.friendly_name
		print(
			"Got dataset '{}' with friendly_name '{}'.".format(
				full_dataset_id, friendly_name
			)
		)

		# View dataset properties.
		print("Description: {}".format(dataset.description))
		print("Labels:")
		labels = dataset.labels
		if labels:
			for label, value in labels.items():
				print("\t{}: {}".format(label, value))
		else:
			print("\tDataset has no labels defined.")

		# View tables in dataset.
		print("Tables:")
		tables = list(client.list_tables(dataset))  # Make an API request(s).
		if tables:
			for table in tables:
				print("\t{}".format(table.table_id))
		else:
			print("\tThis dataset does not contain any tables.")
if __name__ == '__main__':
	gcpdatasets().showds('lt-dia-lake-sbx','daves_dataset')


	


