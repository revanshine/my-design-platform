import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import pytest
from mcp_platform import server
from mcp_platform.jobs.queue import Job

# disable request context checks for unit testing
server.server.__class__.request_context = property(lambda self: None)

@pytest.mark.asyncio
async def test_list_resources_and_read():
    server.notes.clear()
    server.notes['one'] = 'hello'
    resources = await server.handle_list_resources()
    assert resources[0].name == 'Note: one'
    uri = resources[0].uri
    assert await server.handle_read_resource(uri) == 'hello'

@pytest.mark.asyncio
async def test_get_prompt_detailed():
    server.notes.clear()
    server.notes['a'] = 'alpha'
    result = await server.handle_get_prompt('summarize-notes', {'style': 'detailed'})
    text = result.messages[0].content.text
    assert 'Give extensive details' in text
    assert '- a: alpha' in text

@pytest.mark.asyncio
async def test_call_tool_add_and_delete():
    server.notes.clear()
    await server.handle_call_tool('add-note', {'name': 'n1', 'content': 'c1'})
    assert server.notes['n1'] == 'c1'
    await server.handle_call_tool('delete-note', {'name': 'n1'})
    assert 'n1' not in server.notes

@pytest.mark.asyncio
async def test_call_tool_add_async():
    class DummyQueue:
        def __init__(self):
            self.jobs = []
        async def enqueue(self, job):
            self.jobs.append(job)
    dq = DummyQueue()
    server.job_queue = dq
    await server.handle_call_tool('add-note-async', {'name': 'n2', 'content': 'c2'})
    assert dq.jobs and dq.jobs[0].data['name'] == 'n2'

@pytest.mark.asyncio
async def test_read_resource_invalid_scheme():
    from pydantic import AnyUrl
    with pytest.raises(ValueError):
        await server.handle_read_resource(AnyUrl('http://example.com'))

@pytest.mark.asyncio
async def test_call_tool_unknown():
    with pytest.raises(ValueError):
        await server.handle_call_tool('unknown', {'x': 'y'})
