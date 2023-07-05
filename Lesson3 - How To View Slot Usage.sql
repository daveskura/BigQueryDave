/*
  -- Dave Skura, 2023

   BigQuery slot usage

	https://console.cloud.google.com/bigquery/admin/monitoring;region=northamerica-northeast1/resource-utilization?project=digital-billing-cad&region=northamerica-northeast1

*/

-- find queries and the cost.  good pratice to qualify partition and project.
BEGIN
	SELECT
	  TIMESTAMP_TRUNC(creation_time, DAY) AS usage_date,
	  reservation_id,
	  project_id,
	  job_type,
	  user_email,

	  -- Aggregate total_slots_ms /number of milliseconds in a day
	  SAFE_DIVIDE(SUM(total_slot_ms), (1000 * 60 * 60 * 24)) AS average_daily_slot_usage

	FROM `region-northamerica-northeast1`.INFORMATION_SCHEMA.JOBS -- or JOBS_BY_ORGANIZATION 
	WHERE date(creation_time) = current_date -- partition field
		AND project_id = 'lt-dia-lake-sbx' -- cluster field

	GROUP BY
	  usage_date,
	  project_id,
	  job_type,
	  user_email,
	  reservation_id
	ORDER BY
	  usage_date ASC;

END;