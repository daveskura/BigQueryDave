"""
  Dave Skura, 2023

	pp install google
	pip install google-api-python-client
	pip install --upgrade google-api-python-client
	pip3 install --upgrade oauth2client 

	pip install --upgrade google-cloud
	pip install --upgrade google-cloud-bigquery

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery


class cost:
	def __init__(self,query=''): 
		self.query=''
		if query != '':
			self.query=query
			self.estimate_query()
		
		self.updated='Mar 16/2023'

	def estimate_query(self):
		client = bigquery.Client()

		job_config = bigquery.QueryJobConfig(default_dataset='watchful-lotus-364517.dave', dry_run=True, use_query_cache=False)

		query_job = client.query(
				(
						self.query
				),
				job_config=job_config
		)  

		# A dry run query completes immediately.
		print("This query will process {} bytes.".format(query_job.total_bytes_processed))

if __name__ == '__main__':
	cost('SELECT CURRENT_TIMESTAMP')
