from __future__ import annotations

import argparse
from datetime import datetime, timezone

from nfcu_sentinel.pipelines.bronze.spark_jobs import (
    run_b001_with_spark,
    run_b002_with_spark,
    run_b003_with_spark,
)
from nfcu_sentinel.utils.spark_io import get_spark


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Sprint 1 Bronze pipelines using Spark/Delta.")
    parser.add_argument("--catalog", default="nfcu_dev")
    parser.add_argument("--input-root", default="dbfs:/FileStore/nfcu/raw")
    parser.add_argument("--batch-id", default=datetime.now(timezone.utc).strftime("batch-%Y%m%d%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = get_spark("nfcu-sprint1-bronze")

    run_b001_with_spark(
        spark=spark,
        input_csv_path=f"{args.input_root}/fiserv_dna/transaction_detail.csv",
        output_table=f"{args.catalog}.bronze_banking.txn_core_raw",
        batch_id=args.batch_id,
    )
    run_b002_with_spark(
        spark=spark,
        auth_json_path=f"{args.input_root}/tsys_fis/card_auth_stream.jsonl",
        clearing_csv_path=f"{args.input_root}/tsys_fis/card_clearing.csv",
        output_table=f"{args.catalog}.bronze_cards.card_auth_raw",
        batch_id=args.batch_id,
    )
    run_b003_with_spark(
        spark=spark,
        ofac_csv_path=f"{args.input_root}/compliance/ofac_watchlist.csv",
        blocked_csv_path=f"{args.input_root}/compliance/blocked_entities.csv",
        fincen_json_path=f"{args.input_root}/compliance/fincen_advisories.json",
        output_table=f"{args.catalog}.bronze_compliance.ofac_watchlist_raw",
        batch_id=args.batch_id,
    )

    spark.stop()


if __name__ == "__main__":
    main()

