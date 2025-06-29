import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
import pytest
from mcp_platform import server
from mcp_platform.jobs.queue import Job
from mcp_platform.jobs.worker import process_job

@pytest.mark.asyncio
async def test_process_job_add_note():
    server.notes.clear()
    job = Job(type="add-note", data={"name": "async", "content": "hello"})
    await process_job(job)
    assert server.notes["async"] == "hello"
