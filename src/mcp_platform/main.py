from __future__ import annotations

import importlib
import pkgutil
from fastapi import FastAPI

from .servers.base import ToolServerBase


def create_app() -> FastAPI:
    """Create FastAPI app with dynamically discovered tool servers."""
    app = FastAPI()
    package = importlib.import_module("mcp_platform.servers")
    for mod_info in pkgutil.iter_modules(package.__path__):
        if mod_info.name == "base":
            continue
        module = importlib.import_module(f"mcp_platform.servers.{mod_info.name}")
        for attr in dir(module):
            obj = getattr(module, attr)
            if (
                isinstance(obj, type)
                and issubclass(obj, ToolServerBase)
                and obj is not ToolServerBase
            ):
                server = obj()
                mount_path = "/" + mod_info.name.replace("_tool", "")
                app.include_router(server.router(), prefix=mount_path)

    return app
