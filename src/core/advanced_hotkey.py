#!/usr/bin/env python3
"""Advanced Hotkey - Fixed version."""

import logging
from typing import Dict, List

logger = logging.getLogger("AdvancedHotkey")

class AdvancedHotkeyManager:
    """Advanced hotkey manager."""
    
    def __init__(self):
        self.custom_hotkeys = {}
        logger.info("✓ AdvancedHotkeyManager initialized")
    
    def create_custom_hotkey(self, name: str, keys: List[str], action: str) -> bool:
        """Create hotkey safely."""
        
        if not isinstance(name, str) or not isinstance(action, str):
            return False
        
        name = name.strip()
        action = action.strip()
        
        if not name or not action:
            return False
        
        if name in self.custom_hotkeys:
            return False
        
        try:
            self.custom_hotkeys[name] = {"keys": keys if isinstance(keys, list) else [], "action": action}
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    def get_custom_hotkeys(self) -> Dict:
        """Get hotkeys."""
        return self.custom_hotkeys.copy() if isinstance(self.custom_hotkeys, dict) else {}
