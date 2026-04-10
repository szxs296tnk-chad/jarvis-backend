from __future__ import annotations

from infrastructure.monitor import SystemMonitor
from utils.utils import timestamp_now


def get_health(monitor: SystemMonitor, agents: int = 0) -> dict:
    """Return a structured health-check payload."""
    return {
        "status": "online",
        "uptime_seconds": monitor.uptime_seconds(),
        "requests": monitor.requests,
        "active_agents": agents,
        "timestamp": timestamp_now(),
    }