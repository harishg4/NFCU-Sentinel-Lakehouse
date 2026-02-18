from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Any


@dataclass(frozen=True)
class DQResult:
    check_name: str
    passed: bool
    details: str


def null_check(values: Iterable[Any], field_name: str) -> DQResult:
    values_list = list(values)
    nulls = sum(v is None for v in values_list)
    passed = nulls == 0
    details = f"{field_name}: {nulls} null(s)"
    return DQResult("null_check", passed, details)


def uniqueness_check(values: Iterable[Any], field_name: str) -> DQResult:
    values_list = list(values)
    distinct = len(set(values_list))
    passed = distinct == len(values_list)
    details = f"{field_name}: {len(values_list) - distinct} duplicate(s)"
    return DQResult("uniqueness_check", passed, details)


def range_check(values: Iterable[float], field_name: str, min_value: float, max_value: float) -> DQResult:
    bad = [v for v in values if v < min_value or v > max_value]
    passed = len(bad) == 0
    details = f"{field_name}: {len(bad)} out-of-range value(s)"
    return DQResult("range_check", passed, details)
