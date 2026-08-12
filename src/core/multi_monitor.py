#!/usr/bin/env python3
"""Multi-Monitor - Fixed version."""

import logging
from typing import Dict, Optional

logger = logging.getLogger("MultiMonitor")

class MultiMonitorManager:
    """Multi-monitor support."""
    
    def __init__(self):
        self.monitors = [{"id": 0, "name": "Monitor 1", "width": 1920, "height": 1080, "primary": True}]
        self.active_monitor = 0
        logger.info("✓ MultiMonitorManager initialized")
    
    def get_monitor_count(self) -> int:
        """Get monitor count."""
        return len(self.monitors) if isinstance(self.monitors, list) else 0
    
    def set_active_monitor(self, monitor_id: int) -> bool:
        """Set active monitor safely."""
        
        if not isinstance(monitor_id, int):
            return False
        
        if 0 <= monitor_id < len(self.monitors):
            self.active_monitor = monitor_id
            return True
        
        return False
    
    def open_on_monitor(self, app: str, monitor_id: int) -> Dict:
        """Open on monitor safely."""
        
        if not isinstance(app, str):
            return {"success": False}
        
        app = app.strip()
        
        if not app or not isinstance(monitor_id, int):
            return {"success": False}
        
        if 0 <= monitor_id < len(self.monitors):
            return {"app": app, "monitor": monitor_id, "success": True}
        
        return {"success": False}
