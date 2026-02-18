from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyspark.sql import DataFrame, SparkSession


def get_spark(app_name: str) -> "SparkSession":
    from pyspark.sql import SparkSession

    return SparkSession.builder.appName(app_name).getOrCreate()


def read_csv(spark: "SparkSession", path: str, header: bool = True, infer_schema: bool = True) -> "DataFrame":
    return (
        spark.read.format("csv")
        .option("header", str(header).lower())
        .option("inferSchema", str(infer_schema).lower())
        .load(path)
    )


def read_json(spark: "SparkSession", path: str, multiline: bool = False) -> "DataFrame":
    return spark.read.format("json").option("multiline", str(multiline).lower()).load(path)


def read_jdbc_incremental(
    spark: "SparkSession",
    jdbc_url: str,
    table: str,
    user: str,
    password: str,
    watermark_column: str,
    watermark_value: str,
) -> "DataFrame":
    query = f"(SELECT * FROM {table} WHERE {watermark_column} > '{watermark_value}') src"
    return (
        spark.read.format("jdbc")
        .option("url", jdbc_url)
        .option("dbtable", query)
        .option("user", user)
        .option("password", password)
        .load()
    )


def write_delta(df: "DataFrame", target: str, mode: str = "append", partition_by: str | None = None) -> None:
    writer = df.write.format("delta").mode(mode)
    if partition_by:
        writer = writer.partitionBy(partition_by)
    writer.saveAsTable(target)

