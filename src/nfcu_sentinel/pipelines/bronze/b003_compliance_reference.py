from __future__ import annotations

from nfcu_sentinel.pipelines.bronze.common import append_metadata_row

PIPELINE_ID = "B-003"


def normalize_watchlist_record(record: dict, batch_id: str) -> dict:
    out = dict(record)
    name = out.get("name")
    out["name_normalized"] = str(name).strip().upper() if name is not None else None
    return append_metadata_row(out, source_system="ofac_fincen", batch_id=batch_id)
