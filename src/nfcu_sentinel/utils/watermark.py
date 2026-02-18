from __future__ import annotations

from pathlib import Path
import sqlite3


class WatermarkStore:
    def __init__(self, db_path: str | Path = "./.watermark.db") -> None:
        self.db_path = str(db_path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS watermarks (
                    pipeline_id TEXT PRIMARY KEY,
                    watermark_value TEXT NOT NULL
                )
                """
            )

    def get(self, pipeline_id: str, default: str = "1970-01-01T00:00:00Z") -> str:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT watermark_value FROM watermarks WHERE pipeline_id = ?",
                (pipeline_id,),
            ).fetchone()
        return row[0] if row else default

    def set(self, pipeline_id: str, watermark_value: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO watermarks (pipeline_id, watermark_value)
                VALUES (?, ?)
                ON CONFLICT(pipeline_id)
                DO UPDATE SET watermark_value=excluded.watermark_value
                """,
                (pipeline_id, watermark_value),
            )
