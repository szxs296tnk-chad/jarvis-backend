from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger("chad.context.user")


@dataclass
class UserContext:
    """
    Holds persistent preferences and history for a specific user.

    In production this would be backed by a database;
    here it lives in memory for simplicity.
    """
    user_id: str
    preferred_lang: str = "es"
    preferences: dict = field(default_factory=dict)
    interaction_count: int = 0

    def record_interaction(self) -> None:
        self.interaction_count += 1

    def set_preference(self, key: str, value: object) -> None:
        self.preferences[key] = value
        logger.debug(f"User {self.user_id} preference set: {key}={value}")

    def get_preference(self, key: str, default: object = None) -> object:
        return self.preferences.get(key, default)
