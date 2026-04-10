from __future__ import annotations

import json
import logging
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("chad.api.websocket")

ws_router = APIRouter()

# Shared registry of connected PC agents
connected_agents: dict[str, WebSocket] = {}


@ws_router.websocket("/ws/agent")
async def ws_agent(ws: WebSocket):
    await ws.accept()
    agent_id: str | None = None

    try:
        raw = await ws.receive_text()
        msg = json.loads(raw)

        if msg.get("type") != "register":
            await ws.close()
            return

        agent_id = msg.get("agent_id") or f"agent-{uuid.uuid4().hex[:6]}"
        connected_agents[agent_id] = ws
        logger.info(f"Agent connected: {agent_id}")

        while True:
            raw = await ws.receive_text()
            msg = json.loads(raw)

            if msg.get("type") == "result":
                logger.info(f"Agent [{agent_id}] result: {msg.get('output')}")

    except WebSocketDisconnect:
        logger.warning(f"Agent disconnected: {agent_id}")

    except Exception as exc:
        logger.error(f"WS error [{agent_id}]: {exc}")

    finally:
        if agent_id and agent_id in connected_agents:
            del connected_agents[agent_id]


async def forward_to_agent(
    action: str,
    params: dict,
    command_id: str,
    agent_id: str | None = None,
) -> bool:
    """
    Send an action to a connected PC agent via WebSocket.
    Returns True if the message was sent successfully.
    """
    if not connected_agents:
        return False

    target_id = agent_id or next(iter(connected_agents))
    ws = connected_agents.get(target_id)

    if not ws:
        return False

    try:
        await ws.send_text(json.dumps({
            "type": "execute",
            "action": action,
            "params": params,
            "command_id": command_id,
        }))
        return True
    except Exception as exc:
        logger.error(f"WS send error: {exc}")
        return False