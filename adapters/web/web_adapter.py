from __future__ import annotations

import logging
import webbrowser
from urllib.parse import urlencode, quote_plus

import httpx

logger = logging.getLogger("chad.adapters.web")


def search_google(params: dict | None = None) -> str:
    query = (params or {}).get("query", "")
    if not query:
        return "No se especifico que buscar."
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    webbrowser.open(url)
    return f"Buscando: {query}"


def get_request(params: dict | None = None) -> str:
    url = (params or {}).get("url", "")
    if not url:
        return "URL no especificada."
    try:
        resp = httpx.get(url, timeout=10.0)
        return f"GET {url} → {resp.status_code}"
    except Exception as exc:
        logger.error(f"HTTP GET error: {exc}")
        return f"Error al hacer GET a {url}"


def post_request(params: dict | None = None) -> str:
    p = params or {}
    url = p.get("url", "")
    body = p.get("body", {})
    if not url:
        return "URL no especificada."
    try:
        resp = httpx.post(url, json=body, timeout=10.0)
        return f"POST {url} → {resp.status_code}"
    except Exception as exc:
        logger.error(f"HTTP POST error: {exc}")
        return f"Error al hacer POST a {url}"


def trigger_n8n(params: dict | None = None) -> str:
    webhook_url = (params or {}).get("webhook_url", "")
    payload = (params or {}).get("payload", {})
    if not webhook_url:
        return "webhook_url no especificado."
    try:
        resp = httpx.post(webhook_url, json=payload, timeout=10.0)
        return f"n8n trigger → {resp.status_code}"
    except Exception as exc:
        logger.error(f"n8n trigger error: {exc}")
        return "Error al disparar n8n."