from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger("chad.tasks.generate_exam")


async def generate_exam(
    topic: str,
    num_questions: int = 5,
    difficulty: str = "medium",
    lang: str = "es",
) -> dict:
    """
    Generate an exam for the given topic using the LLM.

    Returns a dict with keys:
        topic       - original topic
        questions   - list of question dicts with 'question' and 'answer'
        difficulty  - requested difficulty
    """
    logger.info(f"Generating exam | topic={topic} | questions={num_questions} | difficulty={difficulty}")

    # Lazy import to avoid circular dependencies
    from core.config import Config
    from ia.selector import select_provider
    from core.brain.response_builder import build_messages

    config = Config.load()
    provider = select_provider(config)

    system = (
        "Eres un experto generador de examenes. "
        f"Genera exactamente {num_questions} preguntas sobre el tema indicado. "
        f"Dificultad: {difficulty}. Idioma: {lang}. "
        "Responde SOLO con un JSON valido con este esquema: "
        '{"questions": [{"question": "...", "answer": "..."}]}'
    )

    messages = build_messages([], topic, system)

    raw = await provider.complete(messages)

    import json
    import re

    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`")

    try:
        data = json.loads(raw)
    except Exception:
        logger.warning("Could not parse LLM JSON output for exam; returning raw text")
        data = {"questions": [{"question": raw, "answer": ""}]}

    return {
        "topic": topic,
        "difficulty": difficulty,
        "questions": data.get("questions", []),
    }
