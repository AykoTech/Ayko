
"""Tool Registry - STATIC mapping only. NO logic."""

import logging
from .tools import (
    OpenAppTool, CloseAppTool, SystemInfoTool,
    VolumeControlTool, WebSearchTool, OpenUrlTool
)

logger = logging.getLogger("ToolRegistry")

# STATIC REGISTRY - NO CONDITIONS, NO LOGIC
TOOL_REGISTRY = {
    # System control
    "open_app": OpenAppTool(),
    "close_app": CloseAppTool(),
    "system_info": SystemInfoTool(),
    
    # Audio/Media
    "volume_control": VolumeControlTool(),
    
    # Web
    "web_search": WebSearchTool(),
    "open_url": OpenUrlTool(),
}

class ToolExecutor:
    """Execute tool from registry."""
    
    @staticmethod
    def get_tool(tool_name: str):
        """Get tool by name. Returns None if not found."""
        if tool_name not in TOOL_REGISTRY:
            logger.warning(f"Tool not found: {tool_name}")
            return None
        return TOOL_REGISTRY[tool_name]
    
    @staticmethod
    def execute(tool_name: str, args: dict, state: dict) -> dict:
        """Execute tool - NO routing logic here."""
        
        tool = ToolExecutor.get_tool(tool_name)
        if not tool:
            return {
                "success": False,
                "result": f"Tool {tool_name} not found",
                "state_updates": None,
                "log": f"Unknown tool: {tool_name}"
            }
        
        # Validate arguments
        is_valid, error_msg = tool.validate_args(args)
        if not is_valid:
            return {
                "success": False,
                "result": error_msg,
                "state_updates": None,
                "log": f"Invalid args for {tool_name}: {error_msg}"
            }
        
        # Execute
        try:
            result = tool.execute(args, state)
            logger.info(f"Tool {tool_name}: {result['log']}")
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"Execution error: {e}"
            }
