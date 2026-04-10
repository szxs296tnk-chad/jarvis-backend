from __future__ import annotations

import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger("chad.tasks.queue")


class QueueManager:
    """
    Simple async task queue backed by asyncio.Queue.

    Workers are spawned once via `start()` and
    shut down gracefully via `stop()`.
    """

    def __init__(self, num_workers: int = 2, maxsize: int = 100) -> None:
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self._num_workers = num_workers
        self._workers: list[asyncio.Task] = []
        self._running = False

    async def start(self) -> None:
        self._running = True
        for i in range(self._num_workers):
            task = asyncio.create_task(self._worker(i), name=f"worker-{i}")
            self._workers.append(task)
        logger.info(f"QueueManager started with {self._num_workers} worker(s)")

    async def stop(self) -> None:
        self._running = False
        for _ in self._workers:
            await self._queue.put(None)
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("QueueManager stopped")

    async def enqueue(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        await self._queue.put((func, args, kwargs))

    async def _worker(self, worker_id: int) -> None:
        logger.debug(f"Worker-{worker_id} started")
        while True:
            item = await self._queue.get()
            if item is None:
                self._queue.task_done()
                break
            func, args, kwargs = item
            try:
                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
            except Exception as exc:
                logger.error(f"Worker-{worker_id} job error: {exc}")
            finally:
                self._queue.task_done()
        logger.debug(f"Worker-{worker_id} stopped")