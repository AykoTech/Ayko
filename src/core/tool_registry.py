"""Tool Registry - STATIC mapping only. NO logic."""

import logging
from .tools import (
    OpenAppTool, CloseAppTool, SystemInfoTool,
    VolumeControlTool, WebSearchTool, OpenUrlTool,
    MemoryTool, SuggesterTool, ContextAwarnessTool
)

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


class ToolExecutor:
    @staticmethod
    def get_tool(tool_name: str):
        if tool_name not in TOOL_REGISTRY:
            logger.warning(f"Tool not found: {tool_name}")
            return None
        return TOOL_REGISTRY[tool_name]

    @staticmethod
    def execute(tool_name: str, args: dict, state: dict) -> dict:
        tool = ToolExecutor.get_tool(tool_name)
        if not tool:
            return {"success": False, "result": f"Tool {tool_name} not found",
                    "state_updates": None, "log": f"Unknown tool: {tool_name}"}
        is_valid, error_msg = tool.validate_args(args)
        if not is_valid:
            return {"success": False, "result": error_msg,
                    "state_updates": None, "log": f"Invalid args for {tool_name}: {error_msg}"}
        try:
            result = tool.execute(args, state)
            logger.info(f"Tool {tool_name}: {result.get('log','')}")
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {"success": False, "result": str(e),
                    "state_updates": None, "log": f"Execution error: {e}"}
