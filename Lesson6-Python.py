"""
  Dave Skura
  
"""

print (" Starting ") # 
dataset_id = 'lt-dia-lake-sbx.daves_dataset'

from google.cloud import bigquery

client = bigquery.Client()
dataset = client.get_dataset(dataset_id)  # Make an API request.

print('\n\n--------------------','project',dataset.project)

print('full_dataset_id',dataset.full_dataset_id)
print('dataset_id: ',dataset.dataset_id)
print('friendly_name',dataset.friendly_name)
print("Description: ",dataset.description)
print("Labels:")
labels = dataset.labels
if labels:
	for label, value in labels.items():
		print("\t",label,": ",value)
else:
	print("\tDataset has no labels defined.")

print('default_table_expiration_ms: ',dataset.default_table_expiration_ms)
print('default_partition_expiration_ms:', dataset.default_partition_expiration_ms)
print('default_encryption_configuration:', dataset.default_encryption_configuration)

print('access_entries:', dataset.access_entries)
print('created:', dataset.created)
print('etag:', dataset.etag)

print('location',dataset.location)
print('modified',dataset.modified)

print('path',dataset.path)
print('reference',dataset.reference)
print('self_link',dataset.self_link)
print('modified',dataset.modified)

# View tables in dataset.
print("Tables/Views:")
tables = list(client.list_tables(dataset))  # Make an API request(s).
if tables:
	for table in tables:
		print("\t",table.table_id)
else:
	print("\tThis dataset does not contain any tables.")