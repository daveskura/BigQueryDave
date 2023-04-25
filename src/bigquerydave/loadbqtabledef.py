"""
  Dave Skura, 2023

	you need to run gcloud init to setup your default connection credentials for this

"""
from google.cloud import bigquery
from schemawizard_package.schemawizard import schemawiz

import sys

class bqtabledefs:
	def __init__(self): 
		self.updated='April 6/2023'

	def get_bq_tabledef(self,project_id='',dataset_id='',tablename='',appendtofile=False):
		schwiz = schemawiz()
		bq_filename = 'bqcolumns.csv'
		hdr = 'project_id\tdataset_id\ttablename\tfieldname\tfieldtype\tsampledata_text\n'
		if appendtofile:
			f = open(bq_filename,'a')
		else:
			f = open(bq_filename,'w')
			f.write(hdr)
		
		sql = """
			SELECT project_id,dataset_id,table_id
			FROM bqtables 
			WHERE project_id = '""" + project_id + "' "
		if dataset_id != '':
			sql += " AND dataset_id ='" + dataset_id + "' "

		if tablename != '':
			sql += " AND table_id ='" + tablename + "' "
		
		if appendtofile:
			sql += ' AND concat(project_id,dataset_id,table_id) not in (SELECT concat(project_id,dataset_id,tablename) FROM bqcolumns) '

		sql += ' ORDER BY project_id,dataset_id,table_id '
		#print(sql)
		data = schwiz.dbthings.postgres_db.query(sql)
		irow = 0
		for row in data:
			project = row[0]
			dataset = row[1]
			thistablename = row[2]

			client = bigquery.Client(project=project)
			thistable_id = project + '.' + dataset + '.' + thistablename
	
			sampledata = []
			table = None
			try:
				table = client.get_table(thistable_id)  # Make an API request.
				datarows = list(client.list_rows(thistable_id, max_results=1))
				line = ''
				for onerow in datarows:
					for cols in range(0,len(onerow)):
						sampledata.append(onerow[cols]) 
					break

				#project\tdataset_id\ttablename\tfieldname\tfieldtype\tsampledata_text\n
				i = 0
				for Schemafield in table.schema:
					irow += 1
					if len(sampledata) <= i:
						sampledata.append('')

					f.write(project + '\t' + dataset + '\t' + thistablename + '\t' + Schemafield.name + '\t' + Schemafield.field_type +'\t' + str(sampledata[i]) + '\n')
					i += 1
			except Exception as e:
				f.write(project + '\t' + dataset + '\t' + thistablename + '\tNone\tNone\tNone\n')
				continue


		f.close()
		print(bq_filename + ' loaded with ' + str(irow) + ' rows')

	def load_table(self):
		schwiz = schemawiz()
		bq_filename = 'bqcolumns.csv'
		tablename = 'bqcolumns'

		if schwiz.dbthings.postgres_db.does_table_exist(tablename):
			schwiz.justload_postgres_from_csv(bq_filename,tablename,True)
		else:
			r = schwiz.createload_postgres_from_csv(bq_filename,tablename)

		print(tablename,' loaded')

if __name__ == '__main__':
	print('1. Create/Load table columns in bqcolumns.tsv for selected project/dataset/table.')
	print('2. Append columns in bqcolumns.tsv for selected project/dataset/table.')
	print('3. Create/Load table bqcolumns from bqcolumns.csv')
	print('4. Cancel.')

	selectchar = input('select (1,2,3,4): ') or '4'
	print('')
	if selectchar.upper() == '1':
		print('Create/Load table columns in bqcolumns.tsv for selected project/dataset/table.')
		project_id = input('project_id : ') or 'lt-dia-lake-prd-consume'
		dataset_id = input('dataset_id : ') or ''
		tablename = input('tablename : ') or ''
		bqtabledefs().get_bq_tabledef(project_id,dataset_id,tablename,False)

	elif selectchar.upper() == '2':
		print('Append columns in bqcolumns.tsv for selected project/dataset/table.')
		project_id = input('project_id : ') or 'lt-dia-lake-prd-consume'
		dataset_id = input('dataset_id : ') or ''
		tablename = input('tablename : ') or ''
		bqtabledefs().get_bq_tabledef(project_id,dataset_id,tablename,True)

	elif selectchar.upper() == '3':
		print('Create/Load table bqcolumnes from bqcolumns.csv')
		bqtabledefs().load_table()

	else:
		print('do nothing')



	