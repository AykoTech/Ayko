
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger("Tool")

class Tool(ABC):
    """Base interface for all tools - SINGLE RESPONSIBILITY"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def execute(self, args: Dict[str, Any], state: Dict) -> Dict:
        """Execute tool.
        
        Args:
            args: Tool-specific arguments (from parser)
            state: Global state dict
        
        Returns:
            {
                "success": bool,
                "result": any,
                "state_updates": dict | None,
                "log": str
            }
        """
        pass
    
    def validate_args(self, args: Dict) -> tuple[bool, str]:
        """Validate input arguments. Override if needed.
        
        Returns: (is_valid, error_message)
        """
        return (True, "")
