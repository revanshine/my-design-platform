"""Background job processing utilities."""

from __future__ import annotations

import asyncio
from typing import Optional

from redis.asyncio import Redis

from .queue import Job, RedisJobQueue
from .. import server


async def process_job(job: Job) -> None:
    """Execute a single job."""
    if job.type == "add-note":
        note_name = job.data["name"]
        content = job.data["content"]
        server.notes[note_name] = content
        if server.redis_conn is not None:
            await server.redis_conn.hset("notes", note_name, content)
        if getattr(server, "request_context", None):
            await server.request_context.session.send_resource_list_changed()


async def worker(redis: Redis, poll_interval: float = 1.0) -> None:
    """Continuously process jobs from the queue."""
    queue = RedisJobQueue(redis)
    while True:
        job = await queue.dequeue()
        if job:
            await process_job(job)
        else:
            await asyncio.sleep(poll_interval)
