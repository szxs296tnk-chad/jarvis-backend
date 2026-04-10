from __future__ import annotations

import re
from typing import Optional

# ---------------------------------------------------------------------------
# Intent catalogue
# ---------------------------------------------------------------------------

PC_INTENTS = {
    "OPEN_YOUTUBE",
    "OPEN_NETFLIX",
    "OPEN_BROWSER",
    "OPEN_SPOTIFY",
    "OPEN_NOTES",
    "OPEN_CALCULATOR",
    "SCREENSHOT",
    "SHUTDOWN_PC",
    "RESTART_PC",
    "SET_VOLUME",
}

ALL_INTENTS = PC_INTENTS | {
    "SEARCH_GOOGLE",
    "HTTP_GET",
    "HTTP_POST",
    "N8N_TRIGGER",
    "TURN_ON_LIGHT",
    "TURN_OFF_LIGHT",
    "SET_TEMPERATURE",
    "GET_SENSOR",
    "UNKNOWN",
}

# ---------------------------------------------------------------------------
# Simple keyword-based intent detection
# ---------------------------------------------------------------------------

_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\byoutube\b", re.I), "OPEN_YOUTUBE"),
    (re.compile(r"\bnetflix\b", re.I), "OPEN_NETFLIX"),
    (re.compile(r"\bspotify\b", re.I), "OPEN_SPOTIFY"),
    (re.compile(r"\b(navegador|browser|chrome|firefox)\b", re.I), "OPEN_BROWSER"),
    (re.compile(r"\b(calculadora|calculator)\b", re.I), "OPEN_CALCULATOR"),
    (re.compile(r"\b(notas|notepad|bloc)\b", re.I), "OPEN_NOTES"),
    (re.compile(r"\b(captura|screenshot|pantalla)\b", re.I), "SCREENSHOT"),
    (re.compile(r"\b(apagar|shutdown)\b", re.I), "SHUTDOWN_PC"),
    (re.compile(r"\b(reiniciar|restart|reboot)\b", re.I), "RESTART_PC"),
    (re.compile(r"\b(volumen|volume)\b", re.I), "SET_VOLUME"),
    (re.compile(r"\b(busca|buscar|search|google)\b", re.I), "SEARCH_GOOGLE"),
    (re.compile(r"\b(luz|light|enciende|prende)\b", re.I), "TURN_ON_LIGHT"),
    (re.compile(r"\b(apaga la luz|turn off light)\b", re.I), "TURN_OFF_LIGHT"),
    (re.compile(r"\b(temperatura|temperature|termostato)\b", re.I), "SET_TEMPERATURE"),
    (re.compile(r"\b(sensor|sensores)\b", re.I), "GET_SENSOR"),
]


def detect_intent(text: str) -> str:
    for pattern, intent in _RULES:
        if pattern.search(text):
            return intent
    return "UNKNOWN"


def extract_data(text: str) -> dict:
    data: dict = {}

    vol_match = re.search(r"\b(\d{1,3})\s*%?\s*(volumen|volume)?", text, re.I)
    if vol_match:
        data["level"] = int(vol_match.group(1))

    query_match = re.search(
        r"(?:busca|buscar|search|google)\s+(.+)", text, re.I
    )
    if query_match:
        data["query"] = query_match.group(1).strip()

    return data