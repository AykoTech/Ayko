#!/usr/bin/env python3
"""Time Awareness - Fixed version with proper validation."""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timezone
import random

logger = logging.getLogger("TimeAwareness")

class TimeAwarenessEngine:
    """Time-aware response system with all fixes."""
    
    def __init__(self):
        self.greetings = self._build_greetings()
        logger.info("✓ TimeAwarenessEngine initialized")
    
    def _build_greetings(self) -> Dict[str, List[str]]:
        """Build greetings safely."""
        return {
            "morning": ["Good morning, sir", "Rise and shine", "Morning briefing ready"],
            "afternoon": ["Good afternoon", "How's your day", "Afternoon check-in"],
            "evening": ["Good evening", "End of day review", "Evening update"],
            "night": ["Late night, sir", "Burning the midnight oil", "Night owl mode"],
        }
    
    def get_time_of_day(self) -> str:
        """Get time period safely."""
        try:
            hour = datetime.now(timezone.utc).hour
            
            if 6 <= hour < 12:
                return "morning"
            elif 12 <= hour < 17:
                return "afternoon"
            elif 17 <= hour < 22:
                return "evening"
            else:
                return "night"
        except Exception as e:
            logger.error(f"Error getting time: {e}")
            return "neutral"
    
    def get_greeting(self) -> Optional[str]:
        """Get greeting safely."""
        try:
            time_period = self.get_time_of_day()
            
            if time_period not in self.greetings:
                return None
            
            greetings_list = self.greetings[time_period]
            
            if not greetings_list:
                return None
            
            return random.choice(greetings_list)
        except Exception as e:
            logger.error(f"Error getting greeting: {e}")
            return None
