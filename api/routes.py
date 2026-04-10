from __future__ import annotations

import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException

from api.models import CommandRequest, CommandResponse
from core.brain.orchestrator import Orchestrator
from core.contracts.validator import validate_intent
from executor.dispatcher import dispatch
from infrastructure.monitor import SystemMonitor
from infrastructure.rate_limit import is_allowed
from utils.utils import clean_text, timestamp_now

logger = logging.getLogger("chad.api.routes")

router = APIRouter()

# These are injected by main.py after startup
_orchestrator: Optional[Orchestrator] = None
_monitor: Optional[SystemMonitor] = None
_api_key: str = ""
_history: list[dict] = []


def init_routes(orchestrator: Orchestrator, monitor: SystemMonitor, api_key: str, history: list[dict]) -> None:
    global _orchestrator, _monitor, _api_key, _history
    _orchestrator = orchestrator
    _monitor = monitor
    _api_key = api_key
    _history = history


def _verify_token(x_api_key: str = Header(None)) -> bool:
    if _api_key and x_api_key != _api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@router.get("/health")
async def health():
    return {
        "status": "online",
        "requests": _monitor.requests if _monitor else 0,
        "timestamp": timestamp_now(),
    }


@router.get("/")
async def root():
    return {"status": "online", "version": "3.0.0"}


@router.post("/command", response_model=CommandResponse)
async def command(req: CommandRequest, _auth: bool = Depends(_verify_token)):
    if not is_allowed(req.agent_id or req.source or "global"):
        return CommandResponse(
            response="Espera un momento...",
            timestamp=timestamp_now(),
        )

    if _monitor:
        _monitor.log_request()

    text = clean_text(req.text)
    if not text:
        raise HTTPException(status_code=400, detail="Empty command")

    logger.info(f"[{req.source}] {text}")

    decision = await _orchestrator.process(text, source=req.source, lang=req.lang)

    if decision.action and not validate_intent(decision.action):
        logger.warning(f"Invalid action blocked: {decision.action}")
        decision.action = None

    entry = {
        "id": str(uuid.uuid4())[:8],
        "input": text,
        "response": decision.response,
        "action": decision.action,
        "timestamp": timestamp_now(),
    }
    _history.append(entry)
    if len(_history) > 200:
        _history.pop(0)

    forwarded = False

    if decision.action:
        if not decision.requires_pc:
            decision.response = dispatch(decision.action, decision.params)

    return CommandResponse(
        response=decision.response,
        action=decision.action,
        forwarded_to_agent=forwarded,
        timestamp=timestamp_now(),
    )