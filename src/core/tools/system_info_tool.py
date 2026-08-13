#!/usr/bin/env python3
"""System Info Tool - Get system information."""

import logging
import platform
import psutil
from typing import Dict, Any
from .base_tool import BaseTool

logger = logging.getLogger("SystemInfoTool")

class SystemInfoTool(BaseTool):
    """Tool for getting system information."""
    
    def __init__(self):
        super().__init__("system_info", "Get system information")
    
    def execute(self, args: str, **kwargs) -> Dict[str, Any]:
        """Get system info."""
        
        try:
            info = {
                "os": platform.system(),
                "platform": platform.platform(),
                "processor": platform.processor(),
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory": {
                    "total": psutil.virtual_memory().total / (1024**3),
                    "available": psutil.virtual_memory().available / (1024**3),
                    "percent": psutil.virtual_memory().percent,
                },
                "disk": {
                    "total": psutil.disk_usage("/").total / (1024**3),
                    "free": psutil.disk_usage("/").free / (1024**3),
                    "percent": psutil.disk_usage("/").percent,
                }
            }
            
            self.log_execution(info)
            return {"success": True, "data": info}
        
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {"success": False, "error": str(e)[:100]}
