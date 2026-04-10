from __future__ import annotations

import logging
import time
from typing import Any, Optional

logger = logging.getLogger("chad.store.cache")


class TTLCache:
    """
    In-memory cache with per-entry time-to-live (TTL) expiry.

    Entries are lazily expired on access — no background thread needed.
    """

    def __init__(self, default_ttl: float = 300.0) -> None:
        self._default_ttl = default_ttl
        self._store: dict[str, tuple[Any, float]] = {}

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        expires_at = time.monotonic() + (ttl if ttl is not None else self._default_ttl)
        self._store[key] = (value, expires_at)

    def get(self, key: str, default: Any = None) -> Any:
        entry = self._store.get(key)
        if entry is None:
            return default
        value, expires_at = entry
        if time.monotonic() > expires_at:
            del self._store[key]
            return default
        return value

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def purge_expired(self) -> int:
        now = time.monotonic()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)

    def clear(self) -> None:
        self._store.clear()
        logger.debug("TTLCache cleared")