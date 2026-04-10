from __future__ import annotations

import re
from datetime import datetime, timezone


def clean_text(text: str) -> str:
    """Normalize and strip input text."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def timestamp_now() -> str:
    """Return a UTC ISO-8601 timestamp string."""
    return datetime.now(tz=timezone.utc).isoformat()