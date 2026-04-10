from __future__ import annotations

import logging

from core.config import Config
from ai.providers.ollama import OllamaProvider
from ai.providers.openai import OpenAIProvider
from ai.providers.gemma import GemmaProvider

logger = logging.getLogger("chad.ai.selector")


def select_provider(config: Config):
    """
    Return the correct AI provider instance based on config.

    Resolution order for 'auto':
        1. Claude  (Anthropic SDK, treated as OpenAI-compatible wrapper)
        2. OpenAI
        3. Ollama  (local fallback)
    """
    provider = config.llm_provider

    if provider == "auto":
        provider = _auto_select(config)

    if provider == "claude":
        return _make_claude_provider(config)

    if provider == "openai":
        return OpenAIProvider(
            api_key=config.openai_api_key,
            model=config.openai_model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
        )

    if provider == "gemma":
        return GemmaProvider(
            base_url=config.ollama_base_url,
            model=config.gemma_model,
            max_tokens=config.max_tokens,
        )

    # Default: Ollama
    return OllamaProvider(
        base_url=config.ollama_base_url,
        model=config.ollama_model,
        max_tokens=config.max_tokens,
    )


def _auto_select(config: Config) -> str:
    if config.anthropic_api_key:
        return "claude"
    if config.openai_api_key:
        return "openai"
    return "ollama"


def _make_claude_provider(config: Config):
    """Return a thin wrapper that speaks Claude via the Anthropic SDK."""
    return _ClaudeProvider(
        api_key=config.anthropic_api_key,
        model=config.claude_model,
        max_tokens=config.max_tokens,
    )


class _ClaudeProvider:
    def __init__(self, api_key: str, model: str, max_tokens: int):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens

    async def ping(self) -> None:
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")

    async def complete(self, messages: list[dict], lang: str | None = None) -> str:
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=self.api_key)

        system_content = ""
        turns: list[dict] = []

        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            else:
                turns.append(msg)

        response = await client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_content,
            messages=turns,
        )
        return response.content[0].text.strip()