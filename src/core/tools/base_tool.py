#!/usr/bin/env python3
"""Base Tool - Abstract base class for all tools."""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger("BaseTool")

class BaseTool(ABC):
    """Abstract base class for JARVIS tools."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.enabled = True
        self.execution_count = 0
        self.last_execution = None
        
        logger.info(f"✓ Tool initialized: {name}")
    
    @abstractmethod
    def execute(self, args: str, **kwargs) -> Dict[str, Any]:
        """Execute tool with given arguments."""
        pass
    
    def validate_input(self, args: str) -> bool:
        """Validate input arguments."""
        if args is None or not isinstance(args, str):
            return False
        return True
    
    def log_execution(self, result: Dict):
        """Log tool execution."""
        self.execution_count += 1
        from datetime import datetime
        self.last_execution = datetime.now().isoformat()
        logger.debug(f"Tool executed: {self.name} (count: {self.execution_count})")
    
    def get_stats(self) -> Dict:
        """Get tool statistics."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "execution_count": self.execution_count,
            "last_execution": self.last_execution,
        }
