from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger("chad.ai.openai")


class OpenAIProvider:
    def __init__(self, api_key: str, model: str, max_tokens: int = 512, temperature: float = 0.7):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    async def ping(self) -> None:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

    async def complete(self, messages: list[dict], lang: Optional[str] = None) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content.strip()