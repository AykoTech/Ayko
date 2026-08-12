
import subprocess
import platform
import webbrowser
import logging
from pathlib import Path
from datetime import datetime
import psutil
import os

from .tool_base import Tool

from .command_memory import CommandMemory
from .command_suggester import CommandSuggester
from .screen_capture import ScreenCaptureManager
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

class MemoryTool(Tool):
    """Query command history."""
    
    def __init__(self):
        super().__init__("memory")
        self.memory = None  # Set by Core
    
    def validate_args(self, args: dict) -> tuple:
        """Validate memory query args."""
        query_type = args.get("query", "recent")
        valid_queries = ["recent", "stats", "frequency", "clear"]
        
        if query_type not in valid_queries:
            return False, f"Invalid query: {query_type}"
        
        return True, None
    
    def execute(self, args: dict, state: dict) -> dict:
        """Execute memory query."""
        
        if not self.memory:
            return {
                "success": False,
                "result": "Memory not initialized",
                "state_updates": None,
                "log": "Memory tool error"
            }
        
        query_type = args.get("query", "recent")
        
        try:
            if query_type == "recent":
                recent = self.memory.get_recent(10)
                result = f"Recent {len(recent)} commands: " + ", ".join([
                    cmd["text"] for cmd in recent[-5:]
                ])
            
            elif query_type == "stats":
                stats = self.memory.get_stats()
                result = f"You've issued {stats['total_commands']} commands. "                         f"Success rate: {stats['success_rate']:.0%}. "                         f"Most used: {stats['top_intent']}"
            
            elif query_type == "frequency":
                freq = self.memory.get_command_frequency()
                top_3 = list(freq.items())[:3]
                result = "Most used commands: " + ", ".join([
                    f"{intent} ({count}x)" for intent, count in top_3
                ])
            
            elif query_type == "clear":
                self.memory.clear_history()
                result = "Command history cleared"
            
            return {
                "success": True,
                "result": result,
                "state_updates": None,
                "log": f"Memory query: {query_type}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "result": f"Memory error: {str(e)}",
                "state_updates": None,
                "log": f"Memory tool error: {e}"
            }

class SuggesterTool(Tool):
    """Show command suggestions based on user input."""
    
    def __init__(self):
        super().__init__("suggest")
        self.suggester = CommandSuggester()
    
    def validate_args(self, args: dict) -> tuple:
        """Validate suggester args."""
        query = args.get("query", "")
        
        if not query:
            return False, "Query required"
        
        return True, None
    
    def execute(self, args: dict, state: dict) -> dict:
        """Get suggestions for user query."""
        
        query = args.get("query", "")
        limit = args.get("limit", 3)
        
        try:
            suggestions = self.suggester.suggest(query, threshold=0.5, max_suggestions=limit)
            
            if suggestions:
                suggestion_list = [s["command"] for s in suggestions]
                result = f"I found {len(suggestions)} similar commands: " + ", ".join(suggestion_list)
                
                return {
                    "success": True,
                    "result": result,
                    "state_updates": None,
                    "log": f"Suggestions for '{query}': {suggestion_list}"
                }
            else:
                return {
                    "success": True,
                    "result": f"No suggestions found for '{query}'",
                    "state_updates": None,
                    "log": f"No suggestions for '{query}'"
                }
        
        except Exception as e:
            return {
                "success": False,
                "result": f"Error getting suggestions: {str(e)}",
                "state_updates": None,
                "log": f"Suggester error: {e}"
            }

class ContextAwarnessTool(Tool):
    """Answer questions about current screen context."""
    
    def __init__(self):
        super().__init__("context_awareness")
        self.screen_capture = ScreenCaptureManager()
    
    def validate_args(self, args: dict) -> tuple:
        """Validate context query."""
        question = args.get("question", "")
        
        if not question:
            return False, "Question required"
        
        return True, None
    
    def execute(self, args: dict, state: dict) -> dict:
        """Answer question about screen."""
        
        question = args.get("question", "")
        
        try:
            # Capture current screen
            analysis = self.screen_capture.capture_screenshot()
            
            if not analysis:
                return {
                    "success": False,
                    "result": "Unable to capture screen",
                    "state_updates": None,
                    "log": "Screen capture failed"
                }
            
            # Answer question about context
            answer = self.screen_capture.answer_question_about_screen(question)
            
            if answer:
                return {
                    "success": True,
                    "result": answer,
                    "state_updates": {"screen_context": analysis},
                    "log": f"Context question answered: {question}"
                }
            else:
                return {
                    "success": True,
                    "result": f"I can see you're working on {analysis['window_title']}",
                    "state_updates": {"screen_context": analysis},
                    "log": f"General context returned"
                }
        
        except Exception as e:
            return {
                "success": False,
                "result": f"Context error: {str(e)}",
                "state_updates": None,
                "log": f"Context error: {e}"
            }
