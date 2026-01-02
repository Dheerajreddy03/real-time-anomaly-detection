from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, lit
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    FloatType,
    TimestampType
)

# -------------------------------
# 1. Create Spark Session
# -------------------------------
spark = (
    SparkSession.builder
    .appName("RealTimeAnomalyDetection")
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# -------------------------------
# 2. Kafka message schema
# -------------------------------
schema = StructType([
    StructField("sensor_id", IntegerType(), True),
    StructField("temperature", FloatType(), True),
    StructField("pressure", FloatType(), True),
    StructField("timestamp", TimestampType(), True)
])

# -------------------------------
# 3. Read from Kafka
# -------------------------------
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "sensor-data")
    .option("startingOffsets", "latest")
    .load()
)

# -------------------------------
# 4. Parse JSON from Kafka
# -------------------------------
parsed_df = (
    kafka_df
    .select(from_json(col("value").cast("string"), schema).alias("data"))
    .select("data.*")
)

# -------------------------------
# 5. Simple anomaly detection logic
# -------------------------------
anomalies_df = (
    parsed_df
    .withColumn(
        "anomaly_score",
        when(
            (col("temperature") > 40) | (col("pressure") > 120),
            lit(1.0)
        ).otherwise(lit(0.0))
    )
)

# -------------------------------
# 6. Write to Elasticsearch (CORRECT & SAFE)
# -------------------------------
query = (
    anomalies_df
    .writeStream
    .format("org.elasticsearch.spark.sql")
    .option("es.nodes", "elasticsearch")
    .option("es.port", "9200")
    .option("es.nodes.wan.only", "true")
    .option("es.resource", "anomalies")          # 🔑 index name (MANDATORY)
    .option("checkpointLocation", "/tmp/spark-checkpoints/anomalies")
    .outputMode("append")
    .start()
)

# -------------------------------
# 7. Keep the stream alive
# -------------------------------
query.awaitTermination()

