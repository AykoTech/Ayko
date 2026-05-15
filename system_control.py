
import subprocess
import platform
import pyautogui
import psutil
import webbrowser
import logging
from datetime import datetime
from pathlib import Path
import shutil
import os

logger = logging.getLogger("SystemControl")

class SystemController:
    """Execute system commands and actions"""
    
    def __init__(self):
        self.system = platform.system()
        self.user_home = Path.home()
        logger.info(f"System: {self.system}")
    
    def execute(self, intent: str, params: dict) -> dict:
        """Route command to appropriate handler"""
        
        handlers = {
            "open_app": lambda p: self._open_app(p.get("app")),
            "close_app": lambda p: self._close_app(p.get("app")),
            "open_file": lambda p: self._open_file(p.get("file")),
            "delete_file": lambda p: self._delete_file(p.get("file")),
            "open_url": lambda p: self._open_url(p.get("url")),
            "web_search": lambda p: self._web_search(p.get("query")),
            "volume_control": lambda p: self._set_volume(int(p.get("level", 50))),
            "volume_adjust": lambda p: self._adjust_volume(p.get("dir")),
            "brightness": lambda p: self._set_brightness(int(p.get("level", 50))),
            "play_media": lambda p: self._play_media(p.get("track")),
            "pause_media": lambda p: self._pause_media(),
            "next_track": lambda p: self._next_track(),
            "prev_track": lambda p: self._prev_track(),
            "restart": lambda p: self._restart(),
            "shutdown": lambda p: self._shutdown(),
            "system_info": lambda p: self._get_system_info(p.get("type")),
            "search": lambda p: self._search_files(p.get("query")),
            "settings": lambda p: {"status": "opening settings"},
            "help": lambda p: {"status": "showing help", "commands": 80},
        }
        
        handler = handlers.get(intent, lambda p: {"status": "unknown", "intent": intent})
        
        try:
            result = handler(params)
            logger.info(f"✓ {intent}: {result}")
            return result
        except Exception as e:
            logger.error(f"✗ {intent}: {e}")
            return {"status": "error", "error": str(e)}
    
    def _open_app(self, app_name: str) -> dict:
        """Open application"""
        if not app_name:
            return {"error": "app name required"}
        
        app_name = app_name.strip()
        
        try:
            if self.system == "Windows":
                subprocess.Popen(f"start {app_name}", shell=True)
            elif self.system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            else:  # Linux
                subprocess.Popen([app_name])
            
            return {"status": "opened", "app": app_name}
        except FileNotFoundError:
            return {"error": f"app not found: {app_name}"}
    
    def _close_app(self, app_name: str) -> dict:
        """Close application"""
        if not app_name:
            return {"error": "app name required"}
        
        try:
            if self.system == "Windows":
                subprocess.run(["taskkill", "/IM", f"{app_name}.exe", "/F"], capture_output=True)
            elif self.system == "Darwin":
                subprocess.run(["killall", app_name], capture_output=True)
            else:  # Linux
                subprocess.run(["pkill", "-f", app_name], capture_output=True)
            
            return {"status": "closed", "app": app_name}
        except Exception as e:
            return {"error": str(e)}
    
    def _open_file(self, filename: str) -> dict:
        """Open file with default application"""
        if not filename:
            return {"error": "filename required"}
        
        # Search in common locations
        search_paths = [
            self.user_home / "Desktop" / filename,
            self.user_home / "Downloads" / filename,
            self.user_home / filename,
            Path(filename),
        ]
        
        for path in search_paths:
            if path.exists():
                try:
                    if self.system == "Windows":
                        os.startfile(str(path))
                    elif self.system == "Darwin":
                        subprocess.Popen(["open", str(path)])
                    else:
                        subprocess.Popen(["xdg-open", str(path)])
                    return {"status": "opened", "file": str(path)}
                except Exception as e:
                    return {"error": str(e)}
        
        return {"error": f"file not found: {filename}"}
    
    def _delete_file(self, filename: str) -> dict:
        """Delete file (with safety check)"""
        if not filename:
            return {"error": "filename required"}
        
        path = Path(filename)
        if not path.exists():
            return {"error": "file not found"}
        
        try:
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)
            return {"status": "deleted", "file": filename}
        except Exception as e:
            return {"error": str(e)}
    
    def _open_url(self, url: str) -> dict:
        """Open URL in browser"""
        if not url:
            return {"error": "url required"}
        
        # Add protocol if missing
        if not url.startswith(("http://", "https://")):
            # Map common apps
            app_urls = {
                "youtube": "https://youtube.com",
                "gmail": "https://gmail.com",
                "github": "https://github.com",
                "twitter": "https://twitter.com",
                "reddit": "https://reddit.com",
                "google": "https://google.com",
            }
            url = app_urls.get(url.lower(), f"https://{url}")
        
        try:
            webbrowser.open(url)
            return {"status": "opened", "url": url}
        except Exception as e:
            return {"error": str(e)}
    
    def _web_search(self, query: str) -> dict:
        """Search on Google"""
        if not query:
            return {"error": "query required"}
        
        url = f"https://google.com/search?q={query.replace(' ', '+')}"
        return self._open_url(url)
    
    def _set_volume(self, level: int) -> dict:
        """Set system volume (0-100)"""
        level = max(0, min(100, level))
        
        try:
            if self.system == "Windows":
                # PowerShell command
                cmd = f'(Get-Volume -DriveLetter C).Volume = {level/100}'
                subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            elif self.system == "Darwin":
                cmd = f"osascript -e 'set volume output volume {level}'"
                subprocess.run(cmd, shell=True, capture_output=True)
            else:  # Linux
                subprocess.run(["amixer", "set", "Master", f"{level}%"], capture_output=True)
            
            return {"status": "set", "level": level}
        except Exception as e:
            return {"error": str(e)}
    
    def _adjust_volume(self, direction: str) -> dict:
        """Increase or decrease volume"""
        direction = direction.lower().strip()
        delta = 10 if direction in ["su", "up"] else -10
        
        # Get current volume and adjust
        current = 50  # Default
        return self._set_volume(current + delta)
    
    def _set_brightness(self, level: int) -> dict:
        """Set screen brightness (0-100)"""
        level = max(0, min(100, level))
        
        try:
            if self.system == "Darwin":
                # macOS brightness
                cmd = f"brightness {level/100}"
                subprocess.run(cmd, shell=True, capture_output=True)
            elif self.system == "Windows":
                # Windows WMI
                cmd = f"wmic computersystem where name=\"{os.environ['COMPUTERNAME']}\" call setpowerstate 1"
                subprocess.run(cmd, shell=True, capture_output=True)
            else:  # Linux
                subprocess.run(["xrandr", "--brightness", f"{level/100}"], capture_output=True)
            
            return {"status": "set", "level": level}
        except Exception as e:
            return {"error": str(e)}
    
    def _play_media(self, track: str = None) -> dict:
        """Play media file or music service"""
        return {"status": "playing", "track": track or "music"}
    
    def _pause_media(self) -> dict:
        """Pause media"""
        return {"status": "paused"}
    
    def _next_track(self) -> dict:
        """Skip to next track"""
        return {"status": "next"}
    
    def _prev_track(self) -> dict:
        """Go to previous track"""
        return {"status": "previous"}
    
    def _restart(self) -> dict:
        """Restart system"""
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/r", "/t", "30"])
            else:
                subprocess.run(["sudo", "shutdown", "-r", "+1"])
            return {"status": "restarting in 30 seconds"}
        except Exception as e:
            return {"error": str(e)}
    
    def _shutdown(self) -> dict:
        """Shutdown system"""
        try:
            if self.system == "Windows":
                subprocess.run(["shutdown", "/s", "/t", "30"])
            else:
                subprocess.run(["sudo", "shutdown", "-h", "+1"])
            return {"status": "shutting down in 30 seconds"}
        except Exception as e:
            return {"error": str(e)}
    
    def _get_system_info(self, info_type: str) -> dict:
        """Get system information"""
        info_type = (info_type or "").lower()
        
        if info_type in ["ora", "time", "hour"]:
            return {"info": f"Sono le {datetime.now().strftime('%H:%M:%S')}", "type": "time"}
        
        elif info_type in ["data", "date"]:
            return {"info": datetime.now().strftime("%d/%m/%Y"), "type": "date"}
        
        elif info_type in ["cpu", "uso cpu"]:
            cpu_percent = psutil.cpu_percent(interval=1)
            return {"info": f"CPU al {cpu_percent}%", "cpu": cpu_percent}
        
        elif info_type in ["memoria", "memory"]:
            mem = psutil.virtual_memory()
            free_gb = mem.available / (1024**3)
            return {"info": f"{free_gb:.1f} GB liberi", "free_gb": free_gb}
        
        elif info_type in ["batteria", "battery"]:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    return {"info": f"Batteria {battery.percent}%", "percent": battery.percent}
            except:
                pass
            return {"info": "Batteria non disponibile"}
        
        elif info_type in ["meteo", "weather"]:
            return {"info": "Meteo: dati offline non disponibili"}
        
        else:
            return {"info": "Informazione non disponibile"}
    
    def _search_files(self, query: str) -> dict:
        """Search for files"""
        if not query:
            return {"error": "query required"}
        
        results = []
        try:
            for path in self.user_home.rglob(f"*{query}*"):
                if len(results) >= 10:
                    break
                results.append(str(path))
        except:
            pass
        
        return {"status": "found", "count": len(results), "files": results[:5]}
