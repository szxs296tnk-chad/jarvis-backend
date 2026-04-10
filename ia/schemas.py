from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMMessage:
    role: str
    content: str


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: Optional[str] = None