from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import DoubleType, IntegerType, LongType, StringType, StructField, StructType


schema = StructType(
    [
        StructField("timestamp_ms", LongType()),
        StructField("turbine_id", StringType()),
        StructField("rpm", DoubleType()),
        StructField("vibration", DoubleType()),
        StructField("temperature_c", DoubleType()),
        StructField("pressure_bar", DoubleType()),
        StructField("power_kw", DoubleType()),
        StructField("is_anomaly", IntegerType()),
    ]
)


def main() -> None:
    spark = SparkSession.builder.appName("turbine-anomaly-detection").getOrCreate()
    raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "turbine-telemetry")
        .load()
    )
    parsed = raw.select(from_json(col("value").cast("string"), schema).alias("event")).select("event.*")

    simple_alerts = parsed.where(
        (col("vibration") > 0.75) | (col("temperature_c") > 95) | (col("pressure_bar") > 27)
    )

    query = simple_alerts.writeStream.format("console").outputMode("append").start()
    query.awaitTermination()


if __name__ == "__main__":
    main()
