import sys
import pathlib
from fastapi.testclient import TestClient

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))

from mcp_platform.main import create_app


def test_scaffold_tool_discovery_and_call():
    app = create_app()
    with TestClient(app) as client:
        resp = client.get("/scaffold/tools/list")
        assert resp.status_code == 200
        tools = [t["name"] for t in resp.json()]
        assert "hello_world" in tools
        assert "echo" in tools

        call_resp = client.post(
            "/scaffold/tool/call",
            json={"name": "hello_world", "arguments": {}}
        )
        assert call_resp.status_code == 200
