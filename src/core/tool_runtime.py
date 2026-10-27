"""Tool Runtime - centralized execution boundary for registered tools."""

import logging
from typing import Any, Dict

from .tool_security import is_tool_authorized

logger = logging.getLogger("ToolRuntime")


class ToolRuntime:
    """Resolve, authorize, validate and execute registered tools."""

    def __init__(self, registry: Dict[str, Any]):
        self.registry = registry

    def get_tool(self, tool_name: str):
        """Return a registered tool, or None when it does not exist."""
        tool = self.registry.get(tool_name)
        if tool is None:
            logger.warning("Tool not found: %s", tool_name)
        return tool

    def execute(self, tool_name: str, args: dict, state: dict) -> dict:
        """Authorize, validate and execute a tool through one boundary."""
        tool = self.get_tool(tool_name)
        if tool is None:
            return {
                "success": False,
                "result": f"Tool {tool_name} not found",
                "state_updates": None,
                "log": f"Unknown tool: {tool_name}",
            }

        if not is_tool_authorized(tool_name):
            logger.warning("Authorization denied for tool: %s", tool_name)
            return {
                "success": False,
                "result": f"Tool '{tool_name}' is not authorized by the security policy",
                "state_updates": None,
                "log": f"Authorization denied for tool: {tool_name}",
            }

        is_valid, error_msg = tool.validate_args(args)
        if not is_valid:
            return {
                "success": False,
                "result": error_msg,
                "state_updates": None,
                "log": f"Invalid args for {tool_name}: {error_msg}",
            }

        try:
            result = tool.execute(args, state)
            logger.info("Tool %s: %s", tool_name, result.get("log", ""))
            return result
        except Exception as exc:
            logger.error("Tool execution error for %s: %s", tool_name, exc)
            return {
                "success": False,
                "result": str(exc),
                "state_updates": None,
                "log": f"Execution error: {exc}",
            }
