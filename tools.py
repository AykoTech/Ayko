
import subprocess
import platform
import webbrowser
import logging
from pathlib import Path
from datetime import datetime
import psutil
import os

from .tool_base import Tool

logger = logging.getLogger("Tools")

class OpenAppTool(Tool):
    """Open application. Single responsibility: launch process."""
    
    def __init__(self):
        super().__init__("open_app")
        self.system = platform.system()
    
    def validate_args(self, args):
        if "app" not in args or not args["app"]:
            return (False, "app parameter required")
        return (True, "")
    
    def execute(self, args, state):
        app_name = args.get("app", "").strip()
        
        try:
            if self.system == "Windows":
                subprocess.Popen(f"start {app_name}", shell=True)
            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
            
            return {
                "success": True,
                "result": f"Opened {app_name}",
                "state_updates": {"last_action": "open_app", "target": app_name},
                "log": f"Launched app: {app_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"Failed to open {app_name}: {e}"
            }


class CloseAppTool(Tool):
    """Close application."""
    
    def __init__(self):
        super().__init__("close_app")
        self.system = platform.system()
    
    def validate_args(self, args):
        if "app" not in args or not args["app"]:
            return (False, "app parameter required")
        return (True, "")
    
    def execute(self, args, state):
        app_name = args.get("app", "").strip()
        
        try:
            if self.system == "Windows":
                subprocess.run(["taskkill", "/IM", f"{app_name}.exe", "/F"], capture_output=True)
            elif self.system == "Darwin":
                subprocess.run(["killall", app_name], capture_output=True)
            else:
                subprocess.run(["pkill", "-f", app_name], capture_output=True)
            
            return {
                "success": True,
                "result": f"Closed {app_name}",
                "state_updates": {"last_action": "close_app", "target": app_name},
                "log": f"Closed app: {app_name}"
            }
        except Exception as e:
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"Failed to close {app_name}: {e}"
            }


class SystemInfoTool(Tool):
    """Get system information."""
    
    def __init__(self):
        super().__init__("system_info")
    
    def execute(self, args, state):
        info_type = args.get("type", "").lower()
        
        info_map = {
            "time": lambda: datetime.now().strftime("%H:%M:%S"),
            "date": lambda: datetime.now().strftime("%d/%m/%Y"),
            "cpu": lambda: f"CPU {psutil.cpu_percent(interval=1)}%",
            "memory": lambda: f"Memory {psutil.virtual_memory().percent}%",
            "battery": self._get_battery,
        }
        
        handler = info_map.get(info_type, lambda: "Unknown info type")
        
        try:
            result = handler()
            return {
                "success": True,
                "result": result,
                "state_updates": None,
                "log": f"System info: {info_type}"
            }
        except Exception as e:
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"System info error: {e}"
            }
    
    def _get_battery(self):
        try:
            battery = psutil.sensors_battery()
            return f"Battery {battery.percent}%" if battery else "No battery"
        except:
            return "Battery N/A"


class VolumeControlTool(Tool):
    """Set system volume."""
    
    def __init__(self):
        super().__init__("volume_control")
        self.system = platform.system()
    
    def validate_args(self, args):
        if "level" not in args:
            return (False, "level parameter required")
        try:
            level = int(args["level"])
            if not (0 <= level <= 100):
                return (False, "level must be 0-100")
        except ValueError:
            return (False, "level must be integer")
        return (True, "")
    
    def execute(self, args, state):
        level = int(args.get("level", 50))
        
        try:
            if self.system == "Windows":
                subprocess.run(
                    ["powershell", "-Command", f"(Get-Volume).SetPowerState(1)"],
                    capture_output=True
                )
            elif self.system == "Darwin":
                subprocess.run(
                    f"osascript -e 'set volume output volume {level}'",
                    shell=True, capture_output=True
                )
            else:
                subprocess.run(["amixer", "set", "Master", f"{level}%"], capture_output=True)
            
            return {
                "success": True,
                "result": f"Volume set to {level}",
                "state_updates": {"volume": level},
                "log": f"Volume: {level}%"
            }
        except Exception as e:
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"Volume error: {e}"
            }


class WebSearchTool(Tool):
    """Open web search result."""
    
    def __init__(self):
        super().__init__("web_search")
    
    def validate_args(self, args):
        if "query" not in args or not args["query"]:
            return (False, "query parameter required")
        return (True, "")
    
    def execute(self, args, state):
        query = args.get("query", "").strip()
        url = f"https://google.com/search?q={query.replace(' ', '+')}"
        
        try:
            webbrowser.open(url)
            return {
                "success": True,
                "result": f"Searched: {query}",
                "state_updates": None,
                "log": f"Web search: {query}"
            }
        except Exception as e:
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"Search error: {e}"
            }


class OpenUrlTool(Tool):
    """Open URL in browser."""
    
    def __init__(self):
        super().__init__("open_url")
    
    def validate_args(self, args):
        if "url" not in args or not args["url"]:
            return (False, "url parameter required")
        return (True, "")
    
    def execute(self, args, state):
        url = args.get("url", "").strip()
        
        # Add protocol if missing
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        
        try:
            webbrowser.open(url)
            return {
                "success": True,
                "result": f"Opened {url}",
                "state_updates": None,
                "log": f"URL opened: {url}"
            }
        except Exception as e:
            return {
                "success": False,
                "result": str(e),
                "state_updates": None,
                "log": f"URL error: {e}"
            }
