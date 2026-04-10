from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field

logger = logging.getLogger("chad.config")


def _env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _env_int(key: str, default: int = 0) -> int:
    try:
        return int(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


def _env_float(key: str, default: float = 0.0) -> float:
    try:
        return float(os.environ.get(key, default))
    except (ValueError, TypeError):
        return default


def _env_list(key: str, default: str = "*") -> list[str]:
    raw = os.environ.get(key, default)
    return [o.strip() for o in raw.split(",") if o.strip()]


@dataclass
class Config:
    api_key: str = field(default_factory=lambda: _env("JARVIS_API_KEY"))
    allowed_origins: list[str] = field(default_factory=lambda: _env_list("ALLOWED_ORIGINS", "*"))
    llm_provider: str = field(default_factory=lambda: _env("LLM_PROVIDER", "auto"))
    anthropic_api_key: str = field(default_factory=lambda: _env("ANTHROPIC_API_KEY"))
    openai_api_key: str = field(default_factory=lambda: _env("OPENAI_API_KEY"))
    gemini_api_key: str = field(default_factory=lambda: _env("GEMINI_API_KEY"))
    claude_model: str = field(default_factory=lambda: _env("CLAUDE_MODEL", "claude-sonnet-4-5"))
    openai_model: str = field(default_factory=lambda: _env("OPENAI_MODEL", "gpt-4o-mini"))
    gemma_model: str = field(default_factory=lambda: _env("GEMMA_MODEL", "gemma2:9b"))
    ollama_base_url: str = field(default_factory=lambda: _env("OLLAMA_BASE_URL", "http://localhost:11434"))
    ollama_model: str = field(default_factory=lambda: _env("OLLAMA_MODEL", "llama3"))
    max_tokens: int = field(default_factory=lambda: _env_int("MAX_TOKENS", 512))
    temperature: float = field(default_factory=lambda: _env_float("TEMPERATURE", 0.7))
    wake_word: str = field(default_factory=lambda: _env("WAKE_WORD", "hey jarvis"))
    ha_url: str = field(default_factory=lambda: _env("HA_URL"))
    ha_token: str = field(default_factory=lambda: _env("HA_TOKEN"))
    telegram_token: str = field(default_factory=lambda: _env("TELEGRAM_TOKEN"))
    telegram_chat_id: str = field(default_factory=lambda: _env("TELEGRAM_CHAT_ID"))

    @classmethod
    def load(cls) -> "Config":
        config = cls()
        config._validate()
        return config

    def _validate(self):
        if not self.api_key:
            logger.warning("JARVIS_API_KEY no configurada — API sin proteccion")
        if self.llm_provider in ("claude", "auto") and not self.anthropic_api_key:
            logger.warning("ANTHROPIC_API_KEY no configurada")
        if self.llm_provider in ("openai", "auto") and not self.openai_api_key:
            logger.warning("OPENAI_API_KEY no configurada")
        if self.ha_url and not self.ha_token:
            logger.warning("HA_URL definido pero falta HA_TOKEN")
        logger.info(
            f"Config cargada | LLM={self.llm_provider} | "
            f"HA={'on' if self.ha_url else 'off'} | "
            f"Telegram={'on' if self.telegram_token else 'off'}"
        )