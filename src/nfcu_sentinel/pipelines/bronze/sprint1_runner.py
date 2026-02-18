from __future__ import annotations

import csv
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from nfcu_sentinel.pipelines.bronze.b001_core_banking import PIPELINE_ID as B001_ID
from nfcu_sentinel.pipelines.bronze.b001_core_banking import transform_record as transform_b001
from nfcu_sentinel.pipelines.bronze.b002_card_transactions import PIPELINE_ID as B002_ID
from nfcu_sentinel.pipelines.bronze.b002_card_transactions import normalize_card_record
from nfcu_sentinel.pipelines.bronze.b003_compliance_reference import PIPELINE_ID as B003_ID
from nfcu_sentinel.pipelines.bronze.b003_compliance_reference import normalize_watchlist_record
from nfcu_sentinel.utils.audit import AuditEvent, AuditTrail
from nfcu_sentinel.utils.dq_checks import null_check, uniqueness_check
from nfcu_sentinel.utils.logging_utils import PipelineLogger
from nfcu_sentinel.utils.watermark import WatermarkStore


@dataclass
class PipelineRunResult:
    pipeline_id: str
    run_id: str
    records_processed: int
    output_path: str


def _now_batch_id() -> str:
    return datetime.now(timezone.utc).strftime("batch-%Y%m%d%H%M%S")


def _write_jsonl(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def run_b001(
    input_csv: Path,
    output_jsonl: Path,
    watermark_store: WatermarkStore,
    audit_trail: AuditTrail,
) -> PipelineRunResult:
    run_id = str(uuid.uuid4())
    logger = PipelineLogger(B001_ID, run_id)
    batch_id = _now_batch_id()

    watermark = watermark_store.get(B001_ID)
    watermark_dt = datetime.fromisoformat(watermark.replace("Z", "+00:00"))

    rows: list[dict] = []
    max_last_modified = watermark
    with input_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lm = row.get("last_modified_ts")
            if not lm:
                continue
            lm_dt = datetime.fromisoformat(lm.replace("Z", "+00:00"))
            if lm_dt <= watermark_dt:
                continue
            rows.append(transform_b001(row, batch_id))
            if lm > max_last_modified:
                max_last_modified = lm

    _write_jsonl(rows, output_jsonl)

    dq_nulls = null_check((r.get("transaction_id") for r in rows), "transaction_id")
    dq_unique = uniqueness_check((r.get("transaction_id") for r in rows), "transaction_id")
    logger.info(
        "B-001 completed",
        records_processed=len(rows),
        dq_null_check_passed=dq_nulls.passed,
        dq_uniqueness_passed=dq_unique.passed,
    )

    if rows:
        watermark_store.set(B001_ID, max_last_modified)

    audit_trail.write(
        AuditEvent(
            pipeline_id=B001_ID,
            run_id=run_id,
            status="SUCCESS",
            records_processed=len(rows),
        )
    )

    return PipelineRunResult(B001_ID, run_id, len(rows), str(output_jsonl))


def run_b002(auth_jsonl: Path, clearing_csv: Path, output_jsonl: Path, audit_trail: AuditTrail) -> PipelineRunResult:
    run_id = str(uuid.uuid4())
    logger = PipelineLogger(B002_ID, run_id)
    batch_id = _now_batch_id()

    rows: list[dict] = []

    with auth_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(normalize_card_record(json.loads(line), batch_id))

    with clearing_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(normalize_card_record(row, batch_id))

    _write_jsonl(rows, output_jsonl)

    dq_nulls = null_check((r.get("member_id") for r in rows), "member_id")
    logger.info(
        "B-002 completed",
        records_processed=len(rows),
        dq_null_check_passed=dq_nulls.passed,
    )

    audit_trail.write(
        AuditEvent(
            pipeline_id=B002_ID,
            run_id=run_id,
            status="SUCCESS",
            records_processed=len(rows),
        )
    )

    return PipelineRunResult(B002_ID, run_id, len(rows), str(output_jsonl))


def run_b003(
    ofac_csv: Path,
    fincen_json: Path,
    blocked_csv: Path,
    output_jsonl: Path,
    audit_trail: AuditTrail,
) -> PipelineRunResult:
    run_id = str(uuid.uuid4())
    logger = PipelineLogger(B003_ID, run_id)
    batch_id = _now_batch_id()

    rows: list[dict] = []

    with ofac_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(normalize_watchlist_record(row, batch_id))

    with blocked_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(normalize_watchlist_record(row, batch_id))

    with fincen_json.open("r", encoding="utf-8") as f:
        advisories = json.load(f)
    for advisory in advisories.get("advisories", []):
        rows.append(normalize_watchlist_record(advisory, batch_id))

    _write_jsonl(rows, output_jsonl)

    dq_nulls = null_check((r.get("name_normalized") for r in rows), "name_normalized")
    logger.info(
        "B-003 completed",
        records_processed=len(rows),
        dq_null_check_passed=dq_nulls.passed,
    )

    audit_trail.write(
        AuditEvent(
            pipeline_id=B003_ID,
            run_id=run_id,
            status="SUCCESS",
            records_processed=len(rows),
        )
    )

    return PipelineRunResult(B003_ID, run_id, len(rows), str(output_jsonl))


def run_sprint1_bronze(root: Path | None = None) -> list[PipelineRunResult]:
    repo_root = root or Path(__file__).resolve().parents[4]
    raw = repo_root / "data" / "raw"
    bronze = repo_root / "data" / "bronze"

    watermark_store = WatermarkStore(repo_root / ".watermark.db")
    audit_trail = AuditTrail(repo_root / "artifacts" / "audit-events.jsonl")

    results = [
        run_b001(
            raw / "fiserv_dna" / "transaction_detail.csv",
            bronze / "b001_txn_core_raw.jsonl",
            watermark_store,
            audit_trail,
        ),
        run_b002(
            raw / "tsys_fis" / "card_auth_stream.jsonl",
            raw / "tsys_fis" / "card_clearing.csv",
            bronze / "b002_card_transactions_raw.jsonl",
            audit_trail,
        ),
        run_b003(
            raw / "compliance" / "ofac_watchlist.csv",
            raw / "compliance" / "fincen_advisories.json",
            raw / "compliance" / "blocked_entities.csv",
            bronze / "b003_compliance_reference_raw.jsonl",
            audit_trail,
        ),
    ]

    return results
