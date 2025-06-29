import sys
import pathlib
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from mcp_platform.servers.scaffold_tool import ScaffoldToolServer
from mcp_platform.servers.base import ToolServerBase
from mcp_platform.main import create_app


def test_scaffold_router_endpoints():
    server = ScaffoldToolServer()
    router = server.router()
    app = TestClient(router).app  # Create FastAPI app from router
    client = TestClient(app)
    resp = client.get("/tools/list")
    names = [t["name"] for t in resp.json()]
    assert "hello_world" in names and "echo" in names
    call_resp = client.post("/tool/call", json={"name": "echo", "arguments": {"message": "hi"}})
    assert call_resp.json()[1]["result"] == "hi"


def test_base_class_not_implemented():
    class Dummy(ToolServerBase):
        @property
        def app(self):
            return super().app

    dummy = Dummy()
    with pytest.raises(NotImplementedError):
        dummy.app


def test_create_app_discovers_scaffold():
    app = create_app()
    client = TestClient(app)
    resp = client.get("/scaffold/tools/list")
    assert resp.status_code == 200
