from __future__ import annotations

from pathlib import Path
from typing import Any
import json

import yaml


class ConfigError(Exception):
    """Raised when configuration loading fails."""


class ConfigLoader:
    def __init__(self, root: str | Path = "config") -> None:
        self.root = Path(root)

    def load(self, name: str, env: str = "dev") -> dict[str, Any]:
        base = self._load_file(self.root / f"{name}.yaml")
        env_overrides = self._load_file(self.root / "env" / f"{env}.yaml", optional=True)
        merged = self._deep_merge(base, env_overrides)
        return merged

    @staticmethod
    def load_json(path: str | Path) -> dict[str, Any]:
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)

    def _load_file(self, path: Path, optional: bool = False) -> dict[str, Any]:
        if not path.exists():
            if optional:
                return {}
            raise ConfigError(f"Missing config file: {path}")
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ConfigError(f"Config must be a mapping: {path}")
        return data

    def _deep_merge(self, left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
        out = dict(left)
        for key, value in right.items():
            if key in out and isinstance(out[key], dict) and isinstance(value, dict):
                out[key] = self._deep_merge(out[key], value)
            else:
                out[key] = value
        return out
