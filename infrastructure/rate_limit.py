from __future__ import annotations

import time

_LAST_CALL: dict[str, float] = {}


def is_allowed(user: str = "default", cooldown: float = 1.0) -> bool:
    """
    Return True if the user is not within the cooldown window.

    Uses a simple last-call timestamp per user key.
    """
    now = time.monotonic()
    last = _LAST_CALL.get(user, 0.0)

    if now - last < cooldown:
        return False

    _LAST_CALL[user] = now
    return True