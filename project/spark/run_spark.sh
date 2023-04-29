#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <py_file> <region> <bucket_name>"
  exit 1
fi

# Get the command line arguments
py_file="$1"
region="$2"
bucket_name="$3"

# Submit the PySpark job to Dataproc
gcloud dataproc batches submit pyspark "$py_file" \
--region="$region" \
--deps-bucket="$bucket_name" \
--properties spark.executor.instances=2,spark.driver.cores=4,spark.executor.cores=4 \
--version 2.1 \
--jars=gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-version.jar
