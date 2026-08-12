#!/usr/bin/env python3
"""Suggestions Panel - Fixed version."""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger("SuggestionsPanel")

class CommandSuggestionsPanel:
    """Suggestions panel with all fixes."""
    
    def __init__(self):
        self.visible = False
        self.suggestions = []
        self.selected_index = 0
        
        self.command_categories = {
            "Applications": [
                {"command": "open chrome", "description": "Open Google Chrome"},
                {"command": "open vscode", "description": "Open VS Code"},
            ],
            "System": [
                {"command": "what time is it", "description": "Get current time"},
                {"command": "system info", "description": "System information"},
            ],
        }
        
        logger.info("✓ CommandSuggestionsPanel initialized")
    
    def search_suggestions(self, query: str) -> List[Dict]:
        """Search safely."""
        
        if not isinstance(query, str):
            return []
        
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        results = []
        try:
            for category, commands in self.command_categories.items():
                for cmd in commands:
                    if query_lower in cmd.get("command", "").lower():
                        results.append({**cmd, "category": category})
        except Exception as e:
            logger.error(f"Error: {e}")
        
        return results
    
    def get_all_suggestions(self) -> Dict:
        """Get all suggestions."""
        return self.command_categories.copy()
