from __future__ import annotations

from datetime import datetime, timezone


def append_metadata_row(record: dict, source_system: str, batch_id: str) -> dict:
    return {
        **record,
        "_ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
        "_source_system": source_system,
        "_batch_id": batch_id,
    }
