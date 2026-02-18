from __future__ import annotations

from nfcu_sentinel.pipelines.bronze.common import append_metadata_row

PIPELINE_ID = "B-002"


def normalize_card_record(record: dict, batch_id: str) -> dict:
    out = dict(record)
    if "card_number" in out and out["card_number"]:
        out["card_number_last4"] = str(out["card_number"])[-4:]
    return append_metadata_row(out, source_system="tsys_fis", batch_id=batch_id)
