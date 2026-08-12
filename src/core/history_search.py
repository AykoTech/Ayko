#!/usr/bin/env python3
"""History Search - Fixed version with validation."""

import logging
from typing import List, Dict
from datetime import datetime, timezone
from collections import Counter

logger = logging.getLogger("HistorySearch")

class HistorySearch:
    """History search with all fixes."""
    
    def __init__(self):
        self.history = []
        logger.info("✓ HistorySearch initialized")
    
    def add_to_history(self, command: str, timestamp: datetime = None) -> bool:
        """Add to history safely."""
        
        if not isinstance(command, str):
            return False
        
        command = command.strip()
        if not command:
            return False
        
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        
        try:
            self.history.append({
                "command": command,
                "timestamp": timestamp.isoformat() if isinstance(timestamp, datetime) else str(timestamp),
                "date": timestamp.strftime("%Y-%m-%d") if isinstance(timestamp, datetime) else None,
            })
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    def search_text(self, query: str) -> List[Dict]:
        """Search safely."""
        
        if not isinstance(query, str):
            return []
        
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        try:
            return [e for e in self.history if query_lower in e.get("command", "").lower()]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
    
    def get_most_used(self, limit: int = 10) -> List[Dict]:
        """Get most used."""
        
        try:
            commands = [h.get("command") for h in self.history if h.get("command")]
            counter = Counter(commands)
            
            return [
                {"command": cmd, "count": count}
                for cmd, count in counter.most_common(limit if limit and limit > 0 else 10)
            ]
        except Exception as e:
            logger.error(f"Error: {e}")
            return []
