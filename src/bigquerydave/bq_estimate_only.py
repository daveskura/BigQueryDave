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
import sys
from google.cloud import bigquery

# costo('SELECT CURRENT_TIMESTAMP')
def main():
	if len(sys.argv) != 2:
		print('This script calls BigQuery to ask for the byte cost of a query stored in the file BigQuery.sql \n')
		print('Usage: bq_estimate_only.py BigQuery.sql\n')
		print('---------------------------------------')
	else: # len(sys.argv) == 2:
		queryfilename = sys.argv[1]
		print('opening ' + queryfilename )
		#try:
		f = open(queryfilename,'r')
		sql = f.read()
		f.close()
		print('read contents.\n\n' +sql)
		print('\n-------------------------\nEstimating.\n')
		bytescan = costo().estimate_query(sql)
		print('BigQuery bytescan estimate is ' + str(bytescan))
		#except:
		#	print('parameter must be a file with a SQL inside')


class costo:
	def __init__(self): 
		self.query=''
		self.updated='June 6/2023'

	def estimate_query(self,query=''):
		self.query=query
		
		client = bigquery.Client()

		job_config = bigquery.QueryJobConfig(default_dataset='lt-dia-lake-sbx.daves_dataset', dry_run=True, use_query_cache=False)

		query_job = client.query(
				(
						self.query
				),
				job_config=job_config
		)  

		# A dry run query completes immediately.
		return query_job.total_bytes_processed
		#print("This query will process {} bytes.".format(query_job.total_bytes_processed))



if __name__ == '__main__':
	
	main()