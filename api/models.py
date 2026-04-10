from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class CommandRequest(BaseModel):
    text: str
    source: str = "shortcut"
    lang: Optional[str] = None
    agent_id: Optional[str] = None


class CommandResponse(BaseModel):
    response: str
    action: Optional[str] = None
    forwarded_to_agent: bool = False
    timestamp: str