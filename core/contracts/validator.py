from __future__ import annotations

from executor.registry import TOOLS


def validate_intent(intent: str) -> bool:
    """Return True if the intent is registered in the executor registry."""
    return intent in TOOLS