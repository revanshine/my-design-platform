from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from mcp.server import FastMCP


class ToolCall(BaseModel):
    """Schema for tool invocation payload."""

    name: str
    arguments: dict[str, Any] | None = None


class ToolServerBase(ABC):
    """Abstract base class for pluggable tool servers."""

    @property
    @abstractmethod
    def app(self) -> FastMCP:
        """Return the FastMCP instance exposed by this server."""
        raise NotImplementedError

    def router(self) -> APIRouter:
        """Return FastAPI routes exposing the server's tools."""

        router = APIRouter()

        @router.get("/tools/list")
        async def list_tools() -> Any:
            return await self.app.list_tools()

        @router.post("/tool/call")
        async def call_tool(payload: ToolCall) -> Any:
            return await self.app.call_tool(payload.name, payload.arguments or {})

        return router
