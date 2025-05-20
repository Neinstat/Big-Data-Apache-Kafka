# spark-streaming/consumer_filter.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType

spark = SparkSession.builder \
    .appName("FilterSensorGudang") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Skema JSON untuk suhu & kelembaban
schema_suhu = StructType().add("gudang_id", StringType()).add("suhu", IntegerType())
schema_humi = StructType().add("gudang_id", StringType()).add("kelembaban", IntegerType())

# Stream suhu
suhu_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-suhu-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema_suhu).alias("data")) \
    .select("data.*") \
    .filter(col("suhu") > 80)

# Stream kelembaban
humi_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor-kelembaban-gudang") \
    .load() \
    .selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema_humi).alias("data")) \
    .select("data.*") \
    .filter(col("kelembaban") > 70)

# Fungsi untuk menampilkan peringatan suhu
def display_suhu(batch_df, batch_id):
    if not batch_df.isEmpty():
        print("\n[Peringatan Suhu Tinggi]")
        for row in batch_df.collect():
            print(f"Gudang {row['gudang_id']}: Suhu {row['suhu']}°C")

# Fungsi untuk menampilkan peringatan kelembaban
def display_humi(batch_df, batch_id):
    if not batch_df.isEmpty():
        print("\n[Peringatan Kelembaban Tinggi]")
        for row in batch_df.collect():
            print(f"Gudang {row['gudang_id']}: Kelembaban {row['kelembaban']}%")

# Tampilkan peringatan suhu
suhu_df.writeStream \
    .foreachBatch(display_suhu) \
    .outputMode("append") \
    .start()

# Tampilkan peringatan kelembaban
humi_df.writeStream \
    .foreachBatch(display_humi) \
    .outputMode("append") \
    .start()

# Keep alive
spark.streams.awaitAnyTermination()
