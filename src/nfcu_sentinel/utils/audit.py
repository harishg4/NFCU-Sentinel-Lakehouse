from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json


@dataclass
class AuditEvent:
    pipeline_id: str
    run_id: str
    status: str
    records_processed: int


class AuditTrail:
    def __init__(self, path: str | Path = "./artifacts/audit-events.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: AuditEvent) -> None:
        payload = asdict(event)
        payload["ts"] = datetime.now(timezone.utc).isoformat()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
