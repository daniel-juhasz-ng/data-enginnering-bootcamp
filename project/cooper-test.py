from pyspark.sql import SparkSession
from pyspark.sql.functions import input_file_name
from pyspark.sql.functions import regexp_replace
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, MapType

# Create a SparkSession
spark = SparkSession.builder.appName("ReadJSONFiles").getOrCreate()

# Set the path to the root directory containing the nested folders of JSON files
path = "path/to/root/directory"

# Define the schema for the JSON files (if necessary)

schema = StructType([
    StructField("id", StringType(), True),
    StructField("tms:id", StringType(), True),
    StructField("accession_number", StringType(), True),
    StructField("title", StringType(), True),
    StructField("title_raw", StringType(), True),
    StructField("url", StringType(), True),
    StructField("department_id", StringType(), True),
    StructField("period_id", StringType(), True),
    StructField("media_id", StringType(), True),
    StructField("type_id", StringType(), True),
    StructField("date", StringType(), True),
    StructField("year_start", IntegerType(), True),
    StructField("year_end", IntegerType(), True),
    StructField("year_acquired", StringType(), True),
    StructField("decade", StringType(), True),
    StructField("woe:country_id", StringType(), True),
    StructField("medium", StringType(), True),
    StructField("markings", StringType(), True),
    StructField("signed", StringType(), True),
    StructField("inscribed", StringType(), True),
    StructField("provenance", StringType(), True),
    StructField("dimensions", StringType(), True),
    StructField("dimensions_raw", StringType(), True),
    StructField("creditline", StringType(), True),
    StructField("description", StringType(), True),
    StructField("justification", StringType(), True),
    StructField("woe:country", StringType(), True),
    StructField("type", StringType(), True),
    StructField("images", ArrayType(StringType()), True),
    StructField("participants", ArrayType(
        StructType([
            StructField("person_id", StringType(), True),
            StructField("role_id", StringType(), True),
            StructField("person_name", StringType(), True),
            StructField("person_date", StringType(), True),
            StructField("role_name", StringType(), True),
            StructField("role_display_name", StringType(), True),
            StructField("person_url", StringType(), True),
            StructField("role_url", StringType(), True),
        ])
    ), True),
    StructField("tombstone", StructType([
        StructField("epitaph", StringType(), True),
    ]), True),
    StructField("colors", ArrayType(MapType(StringType(), StringType())), True),
])


# Read the JSON files into a dataframe
df = spark.read.schema(schema).option("multiline", "true").json("/Users/danieljuhasz/Documents/data-eng-bootcamp/project/cooper-hevit-collection-master/merged/*.json")

summary_details = df.select(regexp_replace(col('title'), "\"", ""),col('classification').alias('type'),convert_date_range(col('dated')).alias('date')).withColumn('museum', lit('Minneapolis Institute of Art'))
summary_details = df.select(col('title'),col('type'),convert_date_range(col('date')).alias('date')).withColumn('museum', lit('Cooper Hewitt, Smithsonian Design Museum'))
# Add a column to the dataframe indicating the file name
df = df.withColumn("file_name", input_file_name())

summary_details.write.mode("overwrite").option("header", "true").option("delimiter", ";").csv("/Users/danieljuhasz/Documents/data-eng-bootcamp/project/file1.csv")

# Show the resulting dataframe
df.show()
