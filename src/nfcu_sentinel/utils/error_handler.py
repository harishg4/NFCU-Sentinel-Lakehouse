from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any


def with_error_capture(fallback: Any = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001
                if fallback is not None:
                    return fallback
                raise RuntimeError(f"Pipeline error in {func.__name__}: {exc}") from exc

        return wrapper

    return decorator
