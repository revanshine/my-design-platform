from __future__ import annotations

from mcp.server import FastMCP

from .base import ToolServerBase


class ScaffoldToolServer(ToolServerBase):
    """Minimal tool server used for plugin architecture tests."""

    def __init__(self) -> None:
        self._app = FastMCP(name="scaffold")
        self._app.settings.streamable_http_path = "/"

        @self._app.tool()
        def hello_world() -> str:
            return "scaffold hello"

        @self._app.tool()
        def echo(message: str) -> str:
            return message

    @property
    def app(self) -> FastMCP:
        return self._app
