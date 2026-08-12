#!/usr/bin/env python3
"""Tutorial Mode - Fixed version with validation."""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger("Tutorial")

class TutorialMode:
    """Tutorial system with all fixes."""
    
    def __init__(self):
        self.enabled = False
        self.current_step = 0
        self.completed_steps = set()
        
        self.tutorial_steps = [
            {
                "id": 0,
                "title": "Welcome",
                "description": "Press ALT+J to activate",
                "commands": ["Say JARVIS"],
                "tips": ["You can activate from any app"],
                "duration": "1 minute"
            },
            {
                "id": 1,
                "title": "Commands",
                "description": "Try: 'Open Chrome'",
                "commands": ["open chrome"],
                "tips": ["Natural language supported"],
                "duration": "2 minutes"
            },
        ]
        
        logger.info("✓ TutorialMode initialized")
    
    def start_tutorial(self) -> bool:
        """Start tutorial."""
        try:
            self.enabled = True
            self.current_step = 0
            self.completed_steps.clear()
            return True
        except Exception as e:
            logger.error(f"Error: {e}")
            return False
    
    def next_step(self) -> Optional[Dict]:
        """Get next step."""
        try:
            if self.current_step < len(self.tutorial_steps):
                step = dict(self.tutorial_steps[self.current_step])
                self.completed_steps.add(self.current_step)
                self.current_step += 1
                return step
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def get_progress(self) -> Dict:
        """Get progress."""
        total = len(self.tutorial_steps)
        try:
            return {
                "current_step": self.current_step,
                "total_steps": total,
                "progress_percent": (self.current_step / total * 100) if total > 0 else 0,
                "completed_steps": len(self.completed_steps),
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return {}
