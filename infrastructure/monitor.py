from __future__ import annotations

from datetime import datetime


class SystemMonitor:
    """Tracks basic runtime metrics."""

    def __init__(self) -> None:
        self.start_time: datetime = datetime.utcnow()
        self.requests: int = 0

    def log_request(self) -> None:
        self.requests += 1

    def uptime_seconds(self) -> float:
        return (datetime.utcnow() - self.start_time).total_seconds()

    def status(self) -> dict:
        return {
            "uptime_seconds": self.uptime_seconds(),
            "requests": self.requests,
        }