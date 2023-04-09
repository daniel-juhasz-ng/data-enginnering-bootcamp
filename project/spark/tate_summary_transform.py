import re
from dateutil.parser import parse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, lit
from pyspark.sql.types import StringType


project_id = 'data-eng-bootcamp-project'
raw_dataset_name = 'museum_objects_raw'
processed_dataset_name = 'museum_objects_processed'

spark = SparkSession \
    .builder \
    .appName('spark-bigquery-tate') \
    .getOrCreate()

raw = spark.read.format('bigquery') \
    .load(f'{project_id}.{raw_dataset_name}.tate_objects_table')

# https://www.holistics.io/blog/how-to-extract-nested-or-array-json-in-bigquery/
summary_details = raw.select(
    col('title'),
    col('classification').alias('type'),
    col('dateRange.startYear').alias('date')) \
    .withColumn('museum', lit('Tate Collection'))

# TODO add partition overwrite based on museum value OR just create a dedicated table and replace all values there
summary_details.format('bigquery') \
    .option('writeMethod', 'direct') \
    .save(f'{project_id}.{processed_dataset_name}.summary')
