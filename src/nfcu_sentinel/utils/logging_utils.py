from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any


class PipelineLogger:
    def __init__(self, pipeline_id: str, run_id: str) -> None:
        self.pipeline_id = pipeline_id
        self.run_id = run_id
        self._logger = logging.getLogger(f"nfcu.{pipeline_id}")
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def info(self, message: str, **extra: Any) -> None:
        self._emit("INFO", message, **extra)

    def error(self, message: str, **extra: Any) -> None:
        self._emit("ERROR", message, **extra)

    def _emit(self, level: str, message: str, **extra: Any) -> None:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "pipeline_id": self.pipeline_id,
            "run_id": self.run_id,
            "message": message,
            **extra,
        }
        self._logger.info(json.dumps(payload, sort_keys=True))
