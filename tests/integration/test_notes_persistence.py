import shutil
import subprocess
import time

import pytest
from redis.asyncio import Redis

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from mcp_platform import server
from mcp_platform.jobs.queue import RedisJobQueue
from mcp_platform.jobs.worker import worker
import asyncio
import contextlib


async def wait_for_note_in_redis(redis: Redis, name: str, timeout: float = 3.0) -> None:
    """Poll Redis until the note exists or timeout."""
    start = time.monotonic()
    while time.monotonic() - start < timeout:
        if await redis.hexists("notes", name):
            return
        await asyncio.sleep(0.05)
    raise TimeoutError(f"Note {name} not found in Redis after {timeout}s")


@pytest.fixture(scope="module")
def redis_url():
    if shutil.which("redis-server") is None:
        pytest.skip("redis-server not available")
    proc = subprocess.Popen([
        "redis-server",
        "--port",
        "6380",
        "--save",
        "",
        "--appendonly",
        "no",
    ])
    time.sleep(0.5)
    url = "redis://localhost:6380/0"
    try:
        yield url
    finally:
        subprocess.run(["redis-cli", "-p", "6380", "shutdown"], stdout=subprocess.DEVNULL)
        proc.wait()
        server.redis_conn = None
        server.job_queue = None


@pytest.mark.asyncio
async def test_notes_persistence(redis_url):
    redis = Redis.from_url(redis_url, decode_responses=True)
    await redis.flushdb()
    server.notes.clear()
    server.redis_conn = redis
    server.job_queue = RedisJobQueue(redis)

    worker_task = asyncio.create_task(worker(redis, poll_interval=0.05))
    try:
        await server.handle_call_tool("add-note-async", {"name": "persist", "content": "c1"})
        await wait_for_note_in_redis(redis, "persist")
    finally:
        worker_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await worker_task

    server.notes.clear()
    server.job_queue = RedisJobQueue(redis)
    server.notes.update(await redis.hgetall("notes"))

    resources = await server.handle_list_resources()
    names = [r.name for r in resources]
    assert "Note: persist" in names

    await redis.flushdb()
    await redis.aclose()
