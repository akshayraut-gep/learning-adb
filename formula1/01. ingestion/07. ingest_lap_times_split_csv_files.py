# Databricks notebook source
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

lap_time_schema = StructType(fields = [StructField('race_id', IntegerType(), False),
                                      StructField('driver_id', IntegerType(), True),
                                      StructField('lap', IntegerType(), True),
                                      StructField('position', IntegerType(), True),
                                      StructField('time', StringType(), True),
                                      StructField('milliseconds', IntegerType(), True)])

# COMMAND ----------

# MAGIC %md
# MAGIC #### There are two ways to read split files
# MAGIC ##### 1) Mention the path of the folder where files are kept.
# MAGIC spark.read.schema(lap_time_schema) \
# MAGIC     .csv('/mnt/formula1dl10/raw/lap_times').show()
# MAGIC ##### 2) Use wildcard pattern for matching file names, in case a folder contains different types of split files.
# MAGIC spark.read.schema(lap_time_schema) \
# MAGIC     .csv('/mnt/formula1dl10/raw/lap_times/lap_times*.csv').show()

# COMMAND ----------

lap_time_df = spark.read.schema(lap_time_schema) \
    .csv('/mnt/formula1dl10/raw/lap_times/')

# COMMAND ----------

from pyspark.sql.functions import current_timestamp

lap_time_df.withColumn('ingestion_date', current_timestamp()) \
    .write.mode('overwrite') \
    .parquet('/mnt/formula1dl10/processed/lap_times')

# COMMAND ----------

spark.read.parquet('/mnt/formula1dl10/processed/lap_times').show()
