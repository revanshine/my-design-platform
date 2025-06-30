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

    await server.handle_call_tool("add-note", {"name": "persist", "content": "c1"})

    server.notes.clear()
    server.job_queue = RedisJobQueue(redis)
    server.notes.update(await redis.hgetall("notes"))

    resources = await server.handle_list_resources()
    names = [r.name for r in resources]
    assert "Note: persist" in names

    await redis.flushdb()
    await redis.aclose()
