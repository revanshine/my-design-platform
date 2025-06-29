import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
import pytest
import fakeredis.aioredis
from mcp_platform.jobs.queue import Job, RedisJobQueue

@pytest.mark.asyncio
async def test_enqueue_and_dequeue():
    redis = fakeredis.aioredis.FakeRedis()
    queue = RedisJobQueue(redis)
    job = Job(type="echo", data={"message": "hi"})
    await queue.enqueue(job)
    result = await queue.dequeue()
    assert result == job
