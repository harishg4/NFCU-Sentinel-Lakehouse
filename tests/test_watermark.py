from pathlib import Path

from nfcu_sentinel.utils.watermark import WatermarkStore


def test_watermark_set_get(tmp_path: Path) -> None:
    db = tmp_path / "wm.db"
    store = WatermarkStore(db)
    assert store.get("B-001") == "1970-01-01T00:00:00Z"
    store.set("B-001", "2026-02-18T00:00:00Z")
    assert store.get("B-001") == "2026-02-18T00:00:00Z"
