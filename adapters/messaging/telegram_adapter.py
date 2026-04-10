from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger("chad.adapters.telegram")

_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
_BASE = f"https://api.telegram.org/bot{_TOKEN}"


async def send_message(text: str, chat_id: str | None = None) -> bool:
    """Send a text message via Telegram Bot API."""
    cid = chat_id or _CHAT_ID
    if not _TOKEN or not cid:
        logger.warning("Telegram no configurado (TOKEN o CHAT_ID falta).")
        return False
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{_BASE}/sendMessage",
                json={"chat_id": cid, "text": text},
            )
            resp.raise_for_status()
            return True
    except Exception as exc:
        logger.error(f"Telegram send error: {exc}")
        return False