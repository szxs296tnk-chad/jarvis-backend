from __future__ import annotations

import logging

logger = logging.getLogger("chad.context_manager")


class ContextManager:
    """Manages short-term conversational context."""

    def __init__(self, max_items: int = 20):
        self._items: list[str] = []
        self._max = max_items

    def add(self, text: str) -> None:
        if not text:
            return
        self._items.append(text)
        if len(self._items) > self._max:
            self._items.pop(0)

    def get_context(self) -> str:
        return " | ".join(self._items)

    def clear(self) -> None:
        self._items = []