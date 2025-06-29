"""Redis-backed job queue implementation."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Optional

from redis.asyncio import Redis


@dataclass
class Job:
    """Representation of a queued job."""

    type: str
    data: dict[str, Any]


class RedisJobQueue:
    """A minimal Redis-backed FIFO queue."""

    def __init__(self, redis: Redis, name: str = "jobs") -> None:
        self._redis = redis
        self._name = name

    async def enqueue(self, job: Job) -> int:
        """Add a job to the queue."""
        return await self._redis.rpush(self._name, json.dumps(asdict(job)))

    async def dequeue(self) -> Optional[Job]:
        """Pop the next job from the queue if available."""
        data = await self._redis.lpop(self._name)
        if data is None:
            return None
        return Job(**json.loads(data))
