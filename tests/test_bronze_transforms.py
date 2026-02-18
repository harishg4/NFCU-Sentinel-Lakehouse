from nfcu_sentinel.pipelines.bronze.b001_core_banking import build_jdbc_query, transform_record
from nfcu_sentinel.pipelines.bronze.b002_card_transactions import normalize_card_record
from nfcu_sentinel.pipelines.bronze.b003_compliance_reference import normalize_watchlist_record


def test_b001_query_contains_watermark() -> None:
    query = build_jdbc_query("2026-02-17T00:00:00Z")
    assert "2026-02-17T00:00:00Z" in query


def test_transform_record_adds_metadata() -> None:
    out = transform_record({"transaction_id": "1"}, "batch-1")
    assert out["_batch_id"] == "batch-1"


def test_b002_masks_to_last4() -> None:
    out = normalize_card_record({"card_number": "1234567890123456"}, "batch-2")
    assert out["card_number_last4"] == "3456"


def test_b003_normalizes_name() -> None:
    out = normalize_watchlist_record({"name": "  john doe "}, "batch-3")
    assert out["name_normalized"] == "JOHN DOE"
