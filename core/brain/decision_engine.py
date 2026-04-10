from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from core.contracts.intents import PC_INTENTS

logger = logging.getLogger("chad.decision_engine")


@dataclass
class Decision:
    response: str
    action: Optional[str] = None
    requires_pc: bool = False
    params: dict = field(default_factory=dict)
    source: str = "llm"


def parse_llm_response(raw: str) -> Decision:
    """
    Parse the raw LLM output.

    If the model included an action directive such as:
        ACCION:OPEN_YOUTUBE PARAMS:{"key": "value"}
    it is extracted and stripped from the displayed response.
    """
    raw = raw.strip()

    match = re.search(
        r"ACCION:(\w+)\s+PARAMS:(\{.*?\})",
        raw,
        re.IGNORECASE | re.DOTALL,
    )

    if match:
        action = match.group(1).upper()
        try:
            params = json.loads(match.group(2))
        except Exception:
            params = {}

        clean = re.sub(
            r"ACCION:\w+\s+PARAMS:\{.*?\}",
            "",
            raw,
            flags=re.DOTALL,
        ).strip()

        requires_pc = action in PC_INTENTS

        return Decision(
            response=clean or f"Ejecutando {action.lower()}...",
            action=action,
            requires_pc=requires_pc,
            params=params,
            source="llm",
        )

    return Decision(response=raw, source="llm")