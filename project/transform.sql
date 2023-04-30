INSERT INTO `data-eng-bootcamp-project.crime_processed.crime_processed_table` (year, month, reported_by, crime_type)
SELECT CAST(SPLIT(month, '-')[SAFE_OFFSET(0)] AS INT64) AS year, CAST(SPLIT(month, '-')[SAFE_OFFSET(1)] AS INT64) AS month, reported_by, crime_type FROM `data-eng-bootcamp-project.crime_raw.crime_raw_table`
