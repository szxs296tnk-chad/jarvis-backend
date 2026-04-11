from __future__ import annotations

import logging

logger = logging.getLogger("chad.tasks.process_doc")


async def process_doc(content: str, task: str = "summarize", lang: str = "es") -> str:
    """
    Process a text document with the LLM.

    Parameters
    ----------
    content : str
        Raw text of the document to process.
    task : str
        What to do with it — e.g. "summarize", "translate", "extract_keywords".
    lang : str
        Language for the response.

    Returns
    -------
    str
        The LLM's processed output.
    """
    logger.info(f"Processing document | task={task} | chars={len(content)}")

    from core.config import Config
    from ia.selector import select_provider
    from core.brain.response_builder import build_messages

    config = Config.load()
    provider = select_provider(config)

    task_instructions = {
        "summarize": "Resume el siguiente documento de forma clara y concisa.",
        "translate": f"Traduce el siguiente documento al {lang}.",
        "extract_keywords": "Extrae las palabras clave mas importantes del siguiente documento. Devuelve una lista separada por comas.",
    }

    instruction = task_instructions.get(task, f"Realiza la siguiente tarea sobre el documento: {task}.")

    system = f"Eres un asistente experto en procesamiento de documentos. {instruction} Idioma de respuesta: {lang}."

    messages = build_messages([], content, system)

    return await provider.complete(messages)
