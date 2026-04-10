from __future__ import annotations

from typing import Optional

from core.context.context_manager import ContextManager


def build_system_prompt(
    context_manager: ContextManager,
    lang: Optional[str] = None,
) -> str:
    """Build the system prompt injected into every LLM call."""
    ctx = context_manager.get_context()
    lang_str = f"Responde en: {lang}. " if lang else ""
    ctx_str = f"\nContexto reciente: {ctx}" if ctx else ""

    return (
        "Eres CHAD, un asistente personal inteligente. "
        "Se util y conciso. "
        f"{lang_str}{ctx_str}"
        "\n\nSi necesitas ejecutar una accion responde con este formato exacto:"
        '\nACCION:<NOMBRE_EN_MAYUSCULAS> PARAMS:{"clave": "valor"}'
    )


def build_messages(
    history: list[dict],
    text: str,
    system_prompt: str,
) -> list[dict]:
    """Assemble the full message list for an LLM call."""
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": text})
    return messages