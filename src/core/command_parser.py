
"""Command Parser - SINGLE responsibility: intent → tool routing."""

import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger("CommandParser")

class CommandParser:
    """Map intent to tool name. ONLY routing."""
    
    # STATIC mapping - NO logic, NO conditions
    INTENT_TO_TOOL = {
        # System control
        "open_app": "open_app",
        "close_app": "close_app",
        
        # System info
        "system_info": "system_info",
        "get_time": "system_info",
        "get_date": "system_info",
        
        # Audio
        "volume_control": "volume_control",
        "set_volume": "volume_control",
        
        # Web
        "web_search": "web_search",
        "search": "web_search",
        "open_url": "open_url",
        "open_website": "open_url",
    }
    
    def parse(self, intent: str, args: Dict[str, Any]) -> Tuple[str, Dict]:
        """Convert intent → tool + args.
        
        Args:
            intent: From LLM
            args: From LLM
        
        Returns:
            (tool_name: str, args: dict)
        """
        
        intent = intent.lower().strip()
        
        # Simple direct lookup
        tool = self.INTENT_TO_TOOL.get(intent)
        
        if not tool:
            logger.warning(f"Unknown intent: {intent}")
            return ("unknown", args)
        
        logger.info(f"Mapped {intent} → {tool}")
        return (tool, args)
    
    def register_intent(self, intent: str, tool_name: str):
        """Register new intent mapping. For future extensions."""
        self.INTENT_TO_TOOL[intent] = tool_name
        logger.info(f"Registered: {intent} → {tool_name}")

    def parse_with_memory(self, intent: str, args: dict, memory=None) -> tuple:
        """Parse intent to tool, checking memory for suggestions.
        
        If exact intent not found, check if similar command in history.
        """
        
        # Try exact match first
        tool, mapped_args = self.parse(intent, args)
        
        if tool and memory:
            # Suggest similar command if confidence low
            similar = memory.suggest_similar(intent, threshold=0.65)
            
            if similar:
                logger.debug(f"Similar command found: {similar['original']}")
                return (tool, mapped_args, {
                    "suggestion": similar["original"],
                    "confidence": similar["similarity"],
                    "hint": f"Did you mean: {similar['original']}?"
                })
        
        return (tool, mapped_args, None)
