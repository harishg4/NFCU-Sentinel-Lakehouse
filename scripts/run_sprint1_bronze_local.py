from __future__ import annotations

from nfcu_sentinel.pipelines.bronze.sprint1_runner import run_sprint1_bronze


if __name__ == "__main__":
    results = run_sprint1_bronze()
    for r in results:
        print(f"{r.pipeline_id}: {r.records_processed} -> {r.output_path}")
