from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, get_json_object


project_id = 'data-eng-bootcamp-project'
raw_dataset_name = 'museum_objects_raw'
processed_dataset_name = 'museum_objects_processed'

spark = SparkSession \
    .builder \
    .appName('spark-bigquery-tate') \
    .getOrCreate()

raw = spark.read.format('bigquery') \
    .load(f'{project_id}.{raw_dataset_name}.tate_objects_table')

summary_details = raw.select(
    get_json_object(raw.json_column, "$.title").alias("title"),
    get_json_object(raw.json_column, "$.classification").alias("type"),
    get_json_object(get_json_object(raw.json_column, "$.dateRange"), "$.startYear").alias("date")
).withColumn('museum', lit('Tate Collection'))

# TODO add partition overwrite based on museum value OR just create a dedicated table and replace all values there
summary_details.format('bigquery') \
    .option('writeMethod', 'direct') \
    .save(f'{project_id}.{processed_dataset_name}.summary')



