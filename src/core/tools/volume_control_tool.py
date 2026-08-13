#!/usr/bin/env python3
"""Volume Control Tool - Control system volume."""

import logging
from typing import Dict, Any
from .base_tool import BaseTool

logger = logging.getLogger("VolumeControlTool")

class VolumeControlTool(BaseTool):
    """Tool for controlling system volume."""
    
    def __init__(self):
        super().__init__("volume_control", "Control system volume")
        self.current_volume = 50
    
    def execute(self, args: str, **kwargs) -> Dict[str, Any]:
        """Control volume."""
        
        if not self.validate_input(args):
            return {"success": False, "error": "Invalid input"}
        
        action = args.strip().lower()
        
        if action == "up":
            self.current_volume = min(100, self.current_volume + 10)
        elif action == "down":
            self.current_volume = max(0, self.current_volume - 10)
        elif action == "mute":
            self.current_volume = 0
        elif action == "unmute":
            self.current_volume = 50
        else:
            try:
                self.current_volume = max(0, min(100, int(action)))
            except ValueError:
                return {"success": False, "error": "Invalid volume value"}
        
        self.log_execution({})
        return {"success": True, "volume": self.current_volume}
