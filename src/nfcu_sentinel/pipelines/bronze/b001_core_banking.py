from __future__ import annotations

from nfcu_sentinel.pipelines.bronze.common import append_metadata_row

PIPELINE_ID = "B-001"


def build_jdbc_query(watermark: str) -> str:
    return (
        "SELECT * FROM DNA_TXN.TRANSACTION_DETAIL "
        f"WHERE LAST_MODIFIED_TS > TO_TIMESTAMP('{watermark}')"
    )


def transform_record(record: dict, batch_id: str) -> dict:
    return append_metadata_row(record, source_system="fiserv_dna", batch_id=batch_id)
