import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

import pytest
from mcp_platform import server
from mcp_platform.jobs.queue import Job
import asyncio
import fakeredis.aioredis

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

@pytest.mark.asyncio
async def test_get_prompt_unknown():
    with pytest.raises(ValueError):
        await server.handle_get_prompt('bad', None)

@pytest.mark.asyncio
async def test_handle_list_tools():
    tools = await server.handle_list_tools()
    names = [t.name for t in tools]
    assert set(names) >= {'add-note', 'add-note-async', 'delete-note'}

@pytest.mark.asyncio
async def test_call_tool_missing_arguments():
    with pytest.raises(ValueError):
        await server.handle_call_tool('add-note', None)

@pytest.mark.asyncio
async def test_call_tool_add_missing_fields():
    with pytest.raises(ValueError):
        await server.handle_call_tool('add-note', {'name': 'x'})

@pytest.mark.asyncio
async def test_call_tool_add_triggers_notification(monkeypatch):
    server.notes.clear()
    class Session:
        def __init__(self):
            self.called = False
        async def send_resource_list_changed(self):
            self.called = True
    session = Session()
    server.server.__class__.request_context = property(lambda self: type('Ctx',(object,),{'session':session})())
    await server.handle_call_tool('add-note', {'name':'n3','content':'c3'})
    assert session.called
    server.server.__class__.request_context = property(lambda self: None)

@pytest.mark.asyncio
async def test_call_tool_add_async_no_queue():
    server.notes.clear()
    server.job_queue = None
    with pytest.raises(ValueError):
        await server.handle_call_tool('add-note-async', {'name': 'n4', 'content': 'c4'})

@pytest.mark.asyncio
async def test_call_tool_add_async_missing_fields():
    server.notes.clear()
    class DummyQueue:
        async def enqueue(self, job):
            pass
    server.job_queue = DummyQueue()
    with pytest.raises(ValueError):
        await server.handle_call_tool('add-note-async', {'name': 'n4'})

@pytest.mark.asyncio
async def test_call_tool_delete_missing_name():
    server.notes.clear()
    with pytest.raises(ValueError):
        await server.handle_call_tool('delete-note', {'content': 'c'})

@pytest.mark.asyncio
async def test_call_tool_delete_not_found():
    server.notes.clear()
    with pytest.raises(ValueError):
        await server.handle_call_tool('delete-note', {'name': 'none'})

@pytest.mark.asyncio
async def test_call_tool_delete_triggers_notification(monkeypatch):
    server.notes.clear()
    server.notes['del'] = 'x'
    class Session:
        def __init__(self):
            self.called = False
        async def send_resource_list_changed(self):
            self.called = True
    session = Session()
    server.server.__class__.request_context = property(lambda self: type('Ctx',(object,),{'session':session})())
    await server.handle_call_tool('delete-note', {'name': 'del'})
    assert session.called
    server.server.__class__.request_context = property(lambda self: None)

@pytest.mark.asyncio
async def test_main_runs(monkeypatch):
    server.notes.clear()
    called = {}
    async def fake_worker(redis, poll_interval=0.01):
        called['worker'] = True
    async def fake_run(read, write, opts):
        called['run'] = True
        await asyncio.sleep(0)
    class FakeCM:
        async def __aenter__(self):
            return object(), object()
        async def __aexit__(self, exc_type, exc, tb):
            return False
    monkeypatch.setattr(server, 'worker', fake_worker)
    monkeypatch.setattr(server.mcp.server.stdio, 'stdio_server', lambda: FakeCM())
    monkeypatch.setattr(server.server, 'run', fake_run)
    monkeypatch.setattr(server.Redis, 'from_url', lambda *a, **k: fakeredis.aioredis.FakeRedis())
    await server.main()
    assert 'run' in called and 'worker' in called
