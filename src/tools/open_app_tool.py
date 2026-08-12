#!/usr/bin/env python3
"""Open App Tool - Launch applications."""

import logging
import subprocess
from typing import Dict, Any
from .base_tool import BaseTool

logger = logging.getLogger("OpenAppTool")

class OpenAppTool(BaseTool):
    """Tool for opening applications."""
    
    def __init__(self):
        super().__init__("open_app", "Open applications by name")
        
        self.app_aliases = {
            "chrome": ["google-chrome", "chrome"],
            "firefox": ["firefox"],
            "vscode": ["code"],
            "terminal": ["gnome-terminal", "xterm"],
        }
    
    def execute(self, args: str, **kwargs) -> Dict[str, Any]:
        """Open application."""
        
        if not self.validate_input(args):
            return {"success": False, "error": "Invalid input"}
        
        app_name = args.strip().lower()
        
        if not app_name:
            return {"success": False, "error": "No app specified"}
        
        try:
            self._launch_app(app_name)
            self.log_execution({})
            return {"success": True, "app": app_name, "message": f"Opened {app_name}"}
        
        except Exception as e:
            logger.error(f"Error opening app: {e}")
            return {"success": False, "error": str(e)[:100]}
    
    def _launch_app(self, app_name: str):
        """Launch application."""
        
        cmd = self.app_aliases.get(app_name, [app_name])
        subprocess.Popen(cmd)
