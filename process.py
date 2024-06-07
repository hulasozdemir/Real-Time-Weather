from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, from_unixtime
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, ArrayType, TimestampType

# Define schema for weather data
weather_schema = StructType([
    StructField("coord", StructType([
        StructField("lon", FloatType(), True),
        StructField("lat", FloatType(), True)
    ]), True),
    StructField("weather", ArrayType(StructType([
        StructField("id", IntegerType(), True),
        StructField("main", StringType(), True),
        StructField("description", StringType(), True),
        StructField("icon", StringType(), True)
    ])), True),
    StructField("base", StringType(), True),
    StructField("main", StructType([
        StructField("temp", FloatType(), True),
        StructField("feels_like", FloatType(), True),
        StructField("temp_min", FloatType(), True),
        StructField("temp_max", FloatType(), True),
        StructField("pressure", IntegerType(), True),
        StructField("humidity", IntegerType(), True)
    ]), True),
    StructField("visibility", IntegerType(), True),
    StructField("wind", StructType([
        StructField("speed", FloatType(), True),
        StructField("deg", IntegerType(), True),
        StructField("gust", FloatType(), True)
    ]), True),
    StructField("clouds", StructType([
        StructField("all", IntegerType(), True)
    ]), True),
    StructField("dt", IntegerType(), True),
    StructField("sys", StructType([
        StructField("type", IntegerType(), True),
        StructField("id", IntegerType(), True),
        StructField("country", StringType(), True),
        StructField("sunrise", IntegerType(), True),
        StructField("sunset", IntegerType(), True)
    ]), True),
    StructField("timezone", IntegerType(), True),
    StructField("id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("cod", IntegerType(), True)
])

# Initialize the Spark session
spark = SparkSession.builder \
    .appName("WeatherDataProcessing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.3,org.elasticsearch:elasticsearch-spark-30_2.12:8.14.0") \
    .getOrCreate()

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather") \
    .load()

# Process data
weather_df = df.selectExpr("CAST(value AS STRING) as value") \
    .select(from_json(col("value"), weather_schema).alias("weather_data"))

weather_df = weather_df.withColumn("weather_data.dt", from_unixtime(col("weather_data.dt")).cast(TimestampType()))
# Extract weather_data fields
weather_data_df = weather_df.select("weather_data.*")

# Write data to Elasticsearch
query = weather_data_df.writeStream \
    .outputMode("append") \
    .format("es") \
    .option("checkpointLocation", "/Users/uozdemir/realtime_weather/spark-checkpoint") \
    .option("es.nodes", "localhost:9200") \
    .option("es.index.auto.create", "true") \
    .option("es.resource", "weather_index/") \
    .start()

query.awaitTermination()
