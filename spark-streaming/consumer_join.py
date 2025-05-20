# spark-streaming/consumer_join.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StringType, IntegerType

# 1. Inisialisasi SparkSession
spark = SparkSession.builder \
    .appName("JoinSensorGudang") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Definisikan skema JSON untuk kedua stream
schema_suhu = StructType() \
    .add("gudang_id", StringType()) \
    .add("suhu", IntegerType())

schema_humi = StructType() \
    .add("gudang_id", StringType()) \
    .add("kelembaban", IntegerType())

# 3. Baca stream suhu dengan timestamp Kafka
suhu_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-suhu-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING) AS json", "timestamp") \
    .select(from_json(col("json"), schema_suhu).alias("data"), "timestamp") \
    .select("data.gudang_id", "data.suhu", "timestamp")

# 4. Baca stream kelembaban dengan timestamp Kafka
humi_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-kelembaban-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING) AS json", "timestamp") \
    .select(from_json(col("json"), schema_humi).alias("data"), "timestamp") \
    .select("data.gudang_id", "data.kelembaban", "timestamp")

# 5. Tambahkan watermark untuk menangani data terlambat
s = suhu_df.withWatermark("timestamp", "20 seconds").alias("s")
h = humi_df.withWatermark("timestamp", "20 seconds").alias("h")

# 6. Lakukan join pada gudang_id dan window ±10 detik
joined = s.join(
    h,
    on=(
        (col("s.gudang_id") == col("h.gudang_id")) &
        (col("h.timestamp") >= col("s.timestamp") - expr("INTERVAL 10 seconds")) &
        (col("h.timestamp") <= col("s.timestamp") + expr("INTERVAL 10 seconds"))
    ),
    how="inner"
)

# 7. Tambahkan kolom status sesuai kondisi kritis
result = joined.withColumn(
    "status",
    expr("""
      CASE
        WHEN s.suhu > 80 AND h.kelembaban > 70 THEN 'Bahaya tinggi! Barang berisiko rusak'
        WHEN s.suhu > 80 THEN 'Suhu tinggi, kelembaban normal'
        WHEN h.kelembaban > 70 THEN 'Kelembaban tinggi, suhu aman'
        ELSE 'Aman'
      END
    """)
).select(
    col("s.gudang_id").alias("gudang_id"),
    col("s.suhu").alias("suhu"),
    col("h.kelembaban").alias("kelembaban"),
    col("status")
)

# 8. Tulis hasil join & peringatan ke console dalam append mode
query = result.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .option("checkpointLocation", "/tmp/spark-checkpoints/consumer_join") \
    .start()

query.awaitTermination()
