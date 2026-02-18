from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from nfcu_sentinel.utils.spark_io import read_csv, read_json, write_delta


def _attach_metadata(df: DataFrame, source_system: str, batch_id: str) -> DataFrame:
    return (
        df.withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_system", F.lit(source_system))
        .withColumn("_batch_id", F.lit(batch_id))
    )


def run_b001_with_spark(
    spark,
    input_csv_path: str,
    output_table: str,
    batch_id: str,
) -> None:
    df = read_csv(spark, input_csv_path, header=True, infer_schema=True)
    out = _attach_metadata(df, source_system="fiserv_dna", batch_id=batch_id)
    write_delta(out, target=output_table, mode="append")


def run_b002_with_spark(
    spark,
    auth_json_path: str,
    clearing_csv_path: str,
    output_table: str,
    batch_id: str,
) -> None:
    auth = read_json(spark, auth_json_path).withColumn(
        "card_number_last4",
        F.expr("substring(cast(card_number as string), length(cast(card_number as string)) - 3, 4)"),
    )
    clearing = read_csv(spark, clearing_csv_path, header=True, infer_schema=True).withColumn(
        "card_number_last4", F.lit(None).cast("string")
    )
    merged = auth.unionByName(clearing, allowMissingColumns=True)
    out = _attach_metadata(merged, source_system="tsys_fis", batch_id=batch_id)
    write_delta(out, target=output_table, mode="append")


def run_b003_with_spark(
    spark,
    ofac_csv_path: str,
    blocked_csv_path: str,
    fincen_json_path: str,
    output_table: str,
    batch_id: str,
) -> None:
    ofac = read_csv(spark, ofac_csv_path, header=True, infer_schema=True).withColumn(
        "name_normalized", F.upper(F.trim(F.col("name")))
    )
    blocked = read_csv(spark, blocked_csv_path, header=True, infer_schema=True).withColumn(
        "name_normalized", F.upper(F.trim(F.col("entity_name")))
    )
    fincen_raw = read_json(spark, fincen_json_path, multiline=True)
    advisories = fincen_raw.select(F.explode(F.col("advisories")).alias("advisory")).select("advisory.*")
    advisories = advisories.withColumn("name_normalized", F.upper(F.trim(F.col("title"))))

    merged = ofac.unionByName(blocked, allowMissingColumns=True).unionByName(
        advisories, allowMissingColumns=True
    )
    out = _attach_metadata(merged, source_system="ofac_fincen", batch_id=batch_id)
    write_delta(out, target=output_table, mode="append")

