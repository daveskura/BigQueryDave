"""
  Dave Skura

"""
from bigquerydave.cost

query = """
	   SELECT name, COUNT(*) as name_count 
		 FROM `bigquery-public-data.usa_names.usa_1910_2013` 
     WHERE state = 'WA' 
     GROUP BY name
"""

bq().estimate_query(query)
