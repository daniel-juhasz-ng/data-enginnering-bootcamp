CREATE EXTERNAL TABLE `data-eng-bootcamp-375614.trips_data_all.yellow_tripdata`
OPTIONS (
  format = 'CSV',
  field_delimiter = ',',
  uris = ['gs://dtc_data_lake_data-eng-bootcamp-375614/yellow_tripdata_*.csv.gz']
);
