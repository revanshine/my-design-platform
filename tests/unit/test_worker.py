import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
import pytest
from mcp_platform import server
from mcp_platform.jobs.queue import Job
import contextlib
import asyncio
import fakeredis.aioredis
from mcp_platform.jobs.queue import RedisJobQueue
from mcp_platform.jobs.worker import process_job, worker

@pytest.mark.asyncio
async def test_process_job_add_note():
    server.notes.clear()
    job = Job(type="add-note", data={"name": "async", "content": "hello"})
    await process_job(job)
    assert server.notes["async"] == "hello"


@pytest.mark.asyncio
async def test_process_job_unknown_type():
    server.notes.clear()
    job = Job(type="noop", data={})
    await process_job(job)
    assert server.notes == {}


@pytest.mark.asyncio
async def test_worker_processes_queue():
    server.notes.clear()
    redis = fakeredis.aioredis.FakeRedis()
    queue = RedisJobQueue(redis)
    await queue.enqueue(Job(type="add-note", data={"name": "w", "content": "c"}))
    task = asyncio.create_task(worker(redis, poll_interval=0.01))
    try:
        for _ in range(10):
            await asyncio.sleep(0.01)
            if server.notes.get("w") == "c":
                break
        assert server.notes["w"] == "c"
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
