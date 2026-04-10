from __future__ import annotations

import logging

from executor.registry import TOOLS

logger = logging.getLogger("chad.executor.dispatcher")


def dispatch(intent: str, params: dict | None = None) -> str:
    """
    Dispatch an intent to its registered tool function.

    Returns the tool's string output, or an error message.
    """
    if not intent:
        return "No hay accion para ejecutar."

    tool = TOOLS.get(intent)

    if not tool:
        logger.warning(f"Intent desconocido: {intent}")
        return "No reconozco esa accion."

    try:
        return tool(params or {})
    except Exception as exc:
        logger.error(f"Error ejecutando {intent}: {exc}")
        return "Error ejecutando accion."