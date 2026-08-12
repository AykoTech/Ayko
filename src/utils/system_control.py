#!/usr/bin/env python3
"""System Control Utilities."""

import logging
import os
import platform
import subprocess
from typing import Optional, Dict, Any

logger = logging.getLogger("SystemControl")

class SystemControl:
    """System control operations."""
    
    @staticmethod
    def get_active_window() -> Optional[str]:
        """Get active window title."""
        try:
            system = platform.system()
            
            if system == "Linux":
                result = subprocess.run(
                    ["xdotool", "getactivewindow", "getwindowname"],
                    capture_output=True, text=True
                )
                return result.stdout.strip() if result.returncode == 0 else None
            
            elif system == "Darwin":  # macOS
                result = subprocess.run(
                    ["osascript", "-e", 
                     "tell application \"System Events\" to get name of (processes where frontmost is true)"],
                    capture_output=True, text=True
                )
                return result.stdout.strip() if result.returncode == 0 else None
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting active window: {e}")
            return None
    
    @staticmethod
    def lock_screen() -> bool:
        """Lock the screen."""
        try:
            system = platform.system()
            
            if system == "Linux":
                subprocess.run(["gnome-screensaver-command", "-l"])
            elif system == "Darwin":
                subprocess.run(["osascript", "-e", "tell application \"Finder\" to sleep"])
            elif system == "Windows":
                os.system("rundll32.exe user32.dll,LockWorkStation")
            
            return True
        
        except Exception as e:
            logger.error(f"Error locking screen: {e}")
            return False
