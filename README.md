# NFCU Sentinel Lakehouse

Sprint-1 implementation baseline for a Databricks-native fraud detection and regulatory reporting platform.

## What's Included

- Reusable engineering utilities (`src/nfcu_sentinel/utils`)
- Bronze pipeline starter modules (`src/nfcu_sentinel/pipelines/bronze`)
- Databricks orchestration bundle (`orchestration/databricks.yml`)
- CI workflow for lint/tests + Databricks bundle validate/deploy (`.github/workflows/ci.yml`)
- Unit tests for core utility behavior (`tests/`)

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Run Sprint 1 Bronze Locally

```bash
python3 scripts/run_sprint1_bronze_local.py
```

Outputs:

- `data/bronze/b001_txn_core_raw.jsonl`
- `data/bronze/b002_card_transactions_raw.jsonl`
- `data/bronze/b003_compliance_reference_raw.jsonl`
- `artifacts/audit-events.jsonl`

## Run Sprint 1 Bronze On Databricks (Spark + Delta)

Use this entrypoint in a Databricks job (or via bundle task):

```bash
python scripts/databricks/run_sprint1_bronze_spark.py \
  --catalog workspace \
  --input-root dbfs:/Volumes/workspace/default/nfcu_raw
```

This path uses real Spark DataFrame I/O and writes Delta tables:

- `workspace.bronze_banking.txn_core_raw`
- `workspace.bronze_cards.card_auth_raw`
- `workspace.bronze_compliance.ofac_watchlist_raw`

## Run Databricks Workflow Bundle

```bash
cd orchestration
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle run -t dev sprint1_bronze_orchestration
```

## Sprint 1 Mapping

- `DAT-7`: utility module foundation
- `DAT-4`, `DAT-2`, `DAT-3`: Bronze B-001/B-002/B-003 pipeline scaffolds
- `DAT-5`: Databricks Workflow orchestration (scheduled, retries, dependencies)
- `DAT-1`: CI/CD validation + bundle deployment flow
