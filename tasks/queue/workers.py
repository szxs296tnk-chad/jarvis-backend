from __future__ import annotations

import logging
from typing import Callable, Any

logger = logging.getLogger("chad.tasks.workers")


async def run_job(func: Callable, *args: Any, **kwargs: Any) -> Any:
    """
    Execute a single job function, catching and logging any exceptions.

    Can be used standalone (without the QueueManager) for fire-and-forget
    tasks spawned with asyncio.create_task().
    """
    try:
        import asyncio
        if asyncio.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)
        logger.info(f"Job {func.__name__} completed successfully")
        return result
    except Exception as exc:
        logger.error(f"Job {func.__name__} failed: {exc}")
        return None