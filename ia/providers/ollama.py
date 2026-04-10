from __future__ import annotations

import logging
from typing import Optional

import httpx

logger = logging.getLogger("chad.ai.ollama")


class OllamaProvider:
    def __init__(self, base_url: str, model: str, max_tokens: int = 512):
        self.base_url = base_url
        self.model = model
        self.max_tokens = max_tokens

    async def ping(self) -> None:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{self.base_url}/api/tags")
            r.raise_for_status()

    async def complete(self, messages: list[dict], lang: Optional[str] = None) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            return resp.json()["message"]["content"].strip()