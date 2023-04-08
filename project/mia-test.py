from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, BooleanType, ArrayType
from pyspark.sql.functions import regexp_replace

# Create a SparkSession
spark = SparkSession.builder.appName("ReadJSONFiles").getOrCreate()

# Set the path to the root directory containing the nested folders of JSON files
path = "path/to/root/directory"

# Define the schema for the JSON files (if necessary)
schema = StructType([
    StructField("accession_number", StringType(), True),
    StructField("art_champions_text", StringType(), True),
    StructField("artist", StringType(), True),
    StructField("catalogue_raissonne", StringType(), True),
    StructField("classification", StringType(), True),
    StructField("continent", StringType(), True),
    StructField("country", StringType(), True),
    StructField("creditline", StringType(), True),
    StructField("culture", StringType(), True),
    StructField("curator_approved", IntegerType(), True),
    StructField("dated", StringType(), True),
    StructField("department", StringType(), True),
    StructField("description", StringType(), True),
    StructField("dimension", StringType(), True),
    StructField("id", StringType(), True),
    StructField("image", StringType(), True),
    StructField("image_copyright", StringType(), True),
    StructField("image_height", IntegerType(), True),
    StructField("image_width", IntegerType(), True),
    StructField("inscription", StringType(), True),
    StructField("life_date", StringType(), True),
    StructField("markings", StringType(), True),
    StructField("medium", StringType(), True),
    StructField("nationality", StringType(), True),
    StructField("object_name", StringType(), True),
    StructField("portfolio", StringType(), True),
    StructField("provenance", StringType(), True),
    StructField("restricted", IntegerType(), True),
    StructField("rights_type", StringType(), True),
    StructField("role", StringType(), True),
    StructField("room", StringType(), True),
    StructField("see_also", ArrayType(StringType()), True),
    StructField("signed", StringType(), True),
    StructField("style", StringType(), True),
    StructField("text", StringType(), True),
    StructField("title", StringType(), True)
])

# Read the JSON files into a dataframe
df = spark.read.schema(schema).option("multiline", "true").json("/Users/danieljuhasz/Documents/data-eng-bootcamp/project/mia-collection-main/objects/3/*.json")

summary_details = df.select(regexp_replace(col('title'), "\"", ""),col('classification').alias('type'),convert_date_range(col('dated')).alias('date')).withColumn('museum', lit('Minneapolis Institute of Art'))

# Add a column to the dataframe indicating the file name
df = df.withColumn("file_name", input_file_name())

# Show the resulting dataframe
df.show()
