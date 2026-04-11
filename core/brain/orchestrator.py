from __future__ import annotations

import logging
from typing import Optional

from core.config import Config
from core.context.context_manager import ContextManager
from core.contracts.intents import PC_INTENTS, detect_intent, extract_data
from core.brain.decision_engine import Decision, parse_llm_response
from core.brain.response_builder import build_system_prompt, build_messages
from ia.selector import select_provider

logger = logging.getLogger("chad.orchestrator")


class Orchestrator:
    """
    Central brain of CHAD.

    Responsibilities
    ----------------
    1. Run rule-based intent detection first.
    2. Fall back to LLM when no rule matches.
    3. Maintain short-term history and context.
    """

    def __init__(self, config: Config):
        self.config = config
        self.context = ContextManager()
        self._history: list[dict] = []
        self._max_pairs = 10

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def initialize(self) -> None:
        logger.info(f"Orchestrator | provider={self.config.llm_provider}")
        provider = select_provider(self.config)
        try:
            await provider.ping()
            logger.info(f"{provider.__class__.__name__} ready")
        except Exception as exc:
            logger.warning(f"LLM ping failed: {exc}")
        logger.info("Orchestrator ready")

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    async def process(
        self,
        text: str,
        source: str = "unknown",
        lang: Optional[str] = None,
    ) -> Decision:
        logger.info(f"[Orchestrator:{source}] {text}")

        # 1. Rule-based detection
        intent = detect_intent(text)
        data = extract_data(text)

        if intent != "UNKNOWN":
            self.context.add(f"[{intent}] {text}")
            return Decision(
                response=f"Ejecutando {intent.lower().replace('_', ' ')}...",
                action=intent,
                requires_pc=intent in PC_INTENTS,
                params=data,
                source="rules",
            )

        # 2. LLM fallback
        try:
            system_prompt = build_system_prompt(self.context, lang)
            messages = build_messages(self._history, text, system_prompt)
            provider = select_provider(self.config)
            raw = await provider.complete(messages)
        except Exception as exc:
            logger.error(f"LLM error: {exc}")
            return Decision(response="Error procesando tu solicitud.")

        decision = parse_llm_response(raw)

        self.context.add(text)
        self._push_history(text, decision.response)

        if decision.action:
            decision.requires_pc = decision.action in PC_INTENTS

        return decision

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _push_history(self, user_text: str, assistant_text: str) -> None:
        self._history.append({"role": "user", "content": user_text})
        self._history.append({"role": "assistant", "content": assistant_text})
        max_msgs = self._max_pairs * 2
        if len(self._history) > max_msgs:
            self._history = self._history[-max_msgs:]
