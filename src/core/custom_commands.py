#!/usr/bin/env python3
"""Custom Commands - Ultimate version with security fixes."""

import logging
import shlex
import re
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("CustomCommands")

class CustomCommandManager:
    """Ultimate custom command manager."""
    
    ALLOWED_ACTIONS = {"open", "search", "set_volume", "get_time"}
    
    FORBIDDEN_PATTERNS = [
        r"os\.system", r"subprocess", r"exec", r"eval",
        r"__import__", r"rm\s+-", r"del\s+", r"drop\s+",
        r"format\s+c:", r":[*]",
    ]
    
    def __init__(self):
        self.custom_commands = {}
        logger.info("✓ CustomCommandManager initialized")
    
    def create_custom_command(self, name: str, action: str, description: str = "") -> bool:
        """Create command safely."""
        
        if name is None or not isinstance(name, str):
            return False
        
        if action is None or not isinstance(action, str):
            return False
        
        name = name.strip()
        action = action.strip()
        
        if not self._validate_command_name(name):
            logger.warning(f"Invalid command name: {name}")
            return False
        
        if not self._validate_command_action(action):
            logger.warning(f"Forbidden action: {action[:50]}")
            return False
        
        if len(description) > 200:
            description = description[:200]
        
        self.custom_commands[name] = {
            "action": action,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "last_used": None,
        }
        
        logger.info(f"Command created: {name}")
        return True
    
    def _validate_command_name(self, name: str) -> bool:
        """Validate command name."""
        
        if not isinstance(name, str):
            return False
        
        if not (1 <= len(name) <= 50):
            return False
        
        if not re.match(r'^[a-zA-Z0-9_]+$', name):
            return False
        
        return name not in {"run", "exec", "system", "shell"}
    
    def _validate_command_action(self, action: str) -> bool:
        """Validate action safely."""
        
        if not isinstance(action, str):
            return False
        
        if not (1 <= len(action) <= 1000):
            return False
        
        for pattern in self.FORBIDDEN_PATTERNS:
            try:
                if re.search(pattern, action, re.IGNORECASE):
                    return False
            except re.error:
                continue
        
        return True
    
    def execute_custom_command(self, name: str) -> Optional[Dict]:
        """Execute command safely."""
        
        if name is None or not isinstance(name, str):
            return None
        
        name = name.strip()
        
        if name not in self.custom_commands:
            logger.warning(f"Command not found: {name}")
            return None
        
        try:
            cmd_config = self.custom_commands[name]
            action = cmd_config.get("action", "")
            
            result = self._safe_execute(action)
            
            cmd_config["usage_count"] += 1
            cmd_config["last_used"] = datetime.now().isoformat()
            
            return {
                "success": True,
                "result": result,
                "command": name,
            }
        
        except Exception as e:
            logger.error(f"Command execution error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)[:100],
                "command": name,
            }
    
    def _safe_execute(self, action: str) -> str:
        """Execute safely."""
        
        try:
            parts = shlex.split(action)
            if not parts:
                return "No action"
            
            cmd = parts[0]
            
            if cmd not in self.ALLOWED_ACTIONS:
                return f"Unknown command: {cmd}"
            
            return f"Executed: {cmd}"
        
        except (ValueError, IndexError) as e:
            logger.error(f"Execution error: {e}")
            return "Execution error"
    
    def get_all_custom_commands(self) -> Dict:
        """Get all commands."""
        return {k: {**v, "action_preview": v["action"][:50]} for k, v in self.custom_commands.items()}
    
    def delete_custom_command(self, name: str) -> bool:
        """Delete command."""
        
        if name is None or not isinstance(name, str):
            return False
        
        name = name.strip()
        
        if name in self.custom_commands:
            del self.custom_commands[name]
            logger.info(f"Command deleted: {name}")
            return True
        
        return False
