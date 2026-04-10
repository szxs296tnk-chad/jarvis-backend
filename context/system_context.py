from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("chad.context.system")


@dataclass
class SystemContext:
    """
    Global runtime state shared across all requests.

    Tracks startup time, active agents, and feature flags.
    """
    started_at: datetime = field(default_factory=datetime.utcnow)
    active_agents: set[str] = field(default_factory=set)
    feature_flags: dict[str, bool] = field(default_factory=dict)

    def register_agent(self, agent_id: str) -> None:
        self.active_agents.add(agent_id)
        logger.info(f"SystemContext: agent registered — {agent_id}")

    def unregister_agent(self, agent_id: str) -> None:
        self.active_agents.discard(agent_id)
        logger.info(f"SystemContext: agent unregistered — {agent_id}")

    def uptime_seconds(self) -> float:
        return (datetime.utcnow() - self.started_at).total_seconds()

    def is_enabled(self, flag: str) -> bool:
        return self.feature_flags.get(flag, False)