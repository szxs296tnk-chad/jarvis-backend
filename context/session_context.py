from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("chad.context.session")


@dataclass
class SessionContext:
    """
    Holds data scoped to a single conversation session.

    A new instance is created per WebSocket connection or
    reused across HTTP calls that share the same session_id.
    """
    session_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    messages: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > 40:
            self.messages = self.messages[-40:]

    def get_history(self) -> list[dict]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages = []
        logger.debug(f"Session {self.session_id} cleared")