from __future__ import annotations

"""
LLM Adapter
-----------
Thin facade over ai.selector so the rest of the application
can call a single interface without knowing which provider is active.
"""

import logging
from typing import Optional

from core.config import Config
from ai.selector import select_provider

logger = logging.getLogger("chad.adapters.llm")


class LLMAdapter:
    def __init__(self, config: Config):
        self._config = config

    async def complete(self, messages: list[dict], lang: Optional[str] = None) -> str:
        provider = select_provider(self._config)
        return await provider.complete(messages, lang=lang)

    async def ping(self) -> None:
        provider = select_provider(self._config)
        await provider.ping()