"""Tool Registry - registered tools and compatibility executor."""

import logging

from .tools import (
    OpenAppTool, CloseAppTool, SystemInfoTool,
    VolumeControlTool, WebSearchTool, OpenUrlTool,
    MemoryTool, SuggesterTool, ContextAwarnessTool
)
from .tool_runtime import ToolRuntime

logger = logging.getLogger("ToolRegistry")

TOOL_REGISTRY = {
    "open_app": OpenAppTool(),
    "close_app": CloseAppTool(),
    "system_info": SystemInfoTool(),
    "volume_control": VolumeControlTool(),
    "web_search": WebSearchTool(),
    "open_url": OpenUrlTool(),
    "memory": MemoryTool(),
    "suggest": SuggesterTool(),
    "context_awareness": ContextAwarnessTool(),
}

TOOL_RUNTIME = ToolRuntime(TOOL_REGISTRY)


class ToolExecutor:
    """Backward-compatible facade delegating execution to ToolRuntime."""

    @staticmethod
    def get_tool(tool_name: str):
        return TOOL_RUNTIME.get_tool(tool_name)

    @staticmethod
    def execute(tool_name: str, args: dict, state: dict) -> dict:
        return TOOL_RUNTIME.execute(tool_name, args, state)
