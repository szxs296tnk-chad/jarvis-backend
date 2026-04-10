from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger("chad.store.memory")


class MemoryStore:
    """
    Simple in-memory key-value store.

    Suitable for short-lived data that does not need
    to survive a process restart.
    """

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def exists(self, key: str) -> bool:
        return key in self._data

    def keys(self) -> list[str]:
        return list(self._data.keys())

    def clear(self) -> None:
        self._data.clear()
        logger.debug("MemoryStore cleared")

    def __len__(self) -> int:
        return len(self._data)