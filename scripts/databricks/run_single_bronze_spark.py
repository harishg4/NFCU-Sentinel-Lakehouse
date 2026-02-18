from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_REF = globals().get("__file__") or (sys.argv[0] if sys.argv else "")
_SCRIPT_PATH = Path(_SCRIPT_REF).resolve() if _SCRIPT_REF else Path.cwd() / "scripts/databricks/run_single_bronze_spark.py"
REPO_SRC = (_SCRIPT_PATH.parents[2] / "src").as_posix()
if REPO_SRC not in sys.path:
    sys.path.insert(0, REPO_SRC)

from nfcu_sentinel.pipelines.bronze.spark_jobs import (  # noqa: E402
    run_b001_with_spark,
    run_b002_with_spark,
    run_b003_with_spark,
)
from nfcu_sentinel.utils.spark_io import get_spark  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a single Sprint 1 Bronze pipeline using Spark/Delta.")
    parser.add_argument("--pipeline", choices=["b001", "b002", "b003"], required=True)
    parser.add_argument("--catalog", default="workspace")
    parser.add_argument("--input-root", default="dbfs:/Volumes/workspace/default/nfcu_raw")
    parser.add_argument("--batch-id", default=datetime.now(timezone.utc).strftime("batch-%Y%m%d%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spark = get_spark(f"nfcu-sprint1-{args.pipeline}")

    if args.pipeline == "b001":
        run_b001_with_spark(
            spark=spark,
            input_csv_path=f"{args.input_root}/fiserv_dna/transaction_detail.csv",
            output_table=f"{args.catalog}.bronze_banking.txn_core_raw",
            batch_id=args.batch_id,
        )
    elif args.pipeline == "b002":
        run_b002_with_spark(
            spark=spark,
            auth_json_path=f"{args.input_root}/tsys_fis/card_auth_stream.jsonl",
            clearing_csv_path=f"{args.input_root}/tsys_fis/card_clearing.csv",
            output_table=f"{args.catalog}.bronze_cards.card_auth_raw",
            batch_id=args.batch_id,
        )
    else:
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
