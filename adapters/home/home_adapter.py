from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger("chad.adapters.home")

_HA_URL = os.environ.get("HA_URL", "")
_HA_TOKEN = os.environ.get("HA_TOKEN", "")


def _ha_headers() -> dict:
    return {
        "Authorization": f"Bearer {_HA_TOKEN}",
        "Content-Type": "application/json",
    }


def turn_on_light(params: dict | None = None) -> str:
    entity_id = (params or {}).get("entity_id", "light.all_lights")
    if not _HA_URL:
        return "Home Assistant no configurado."
    try:
        resp = httpx.post(
            f"{_HA_URL}/api/services/light/turn_on",
            json={"entity_id": entity_id},
            headers=_ha_headers(),
            timeout=10.0,
        )
        return f"Luz encendida: {entity_id} ({resp.status_code})"
    except Exception as exc:
        logger.error(f"turn_on_light error: {exc}")
        return "No pude encender la luz."


def turn_off_light(params: dict | None = None) -> str:
    entity_id = (params or {}).get("entity_id", "light.all_lights")
    if not _HA_URL:
        return "Home Assistant no configurado."
    try:
        resp = httpx.post(
            f"{_HA_URL}/api/services/light/turn_off",
            json={"entity_id": entity_id},
            headers=_ha_headers(),
            timeout=10.0,
        )
        return f"Luz apagada: {entity_id} ({resp.status_code})"
    except Exception as exc:
        logger.error(f"turn_off_light error: {exc}")
        return "No pude apagar la luz."


def set_temperature(params: dict | None = None) -> str:
    p = params or {}
    entity_id = p.get("entity_id", "climate.main")
    temperature = p.get("temperature", 22)
    if not _HA_URL:
        return "Home Assistant no configurado."
    try:
        resp = httpx.post(
            f"{_HA_URL}/api/services/climate/set_temperature",
            json={"entity_id": entity_id, "temperature": temperature},
            headers=_ha_headers(),
            timeout=10.0,
        )
        return f"Temperatura ajustada a {temperature}°C ({resp.status_code})"
    except Exception as exc:
        logger.error(f"set_temperature error: {exc}")
        return "No pude ajustar la temperatura."


def get_sensor_state(params: dict | None = None) -> str:
    entity_id = (params or {}).get("entity_id", "")
    if not entity_id:
        return "entity_id no especificado."
    if not _HA_URL:
        return "Home Assistant no configurado."
    try:
        resp = httpx.get(
            f"{_HA_URL}/api/states/{entity_id}",
            headers=_ha_headers(),
            timeout=10.0,
        )
        data = resp.json()
        return f"{entity_id}: {data.get('state', 'desconocido')}"
    except Exception as exc:
        logger.error(f"get_sensor_state error: {exc}")
        return "No pude obtener el estado del sensor."