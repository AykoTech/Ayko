#!/usr/bin/env python3
"""Command Memory - Ultimate version with ALL bugs fixed."""

import logging
import threading
import json
import unicodedata
from typing import List, Dict, Optional, Tuple
from collections import deque, Counter
from datetime import datetime, timezone
from pathlib import Path
import re

logger = logging.getLogger("CommandMemory")

class CommandMemory:
    """Ultimate command memory with all fixes applied."""
    
    MAX_COMMAND_BYTES = 5000
    MAX_HISTORY_SIZE = 50
    
    def __init__(self, max_size: int = MAX_HISTORY_SIZE, config_path: Path = None):
        self.history: deque = deque(maxlen=max_size)
        self.config_path = config_path or Path.home() / ".ayko" / "command_history.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._lock = threading.RLock()
        self._frequency_cache = {}
        self._cache_valid = False
        self._discarded_items_count = 0
        
        self._load_history()
        logger.info(f"✓ CommandMemory initialized (max_size={max_size})")
    
    def add_command(self, text: str, intent: str, success: bool) -> bool:
        """Add command with comprehensive validation."""
        
        if text is None or not isinstance(text, str):
            logger.warning(f"Invalid command type: {type(text)}")
            return False
        
        text_stripped = text.strip()
        
        if not text_stripped:
            logger.debug("Empty command rejected")
            return False
        
        text_bytes = text_stripped.encode('utf-8')
        if len(text_bytes) > self.MAX_COMMAND_BYTES:
            logger.warning(f"Command too long: {len(text_bytes)} bytes")
            return False
        
        intent_stripped = str(intent).strip() if intent else "unknown"
        
        safe_text = self._sanitize_text(text_stripped)
        
        with self._lock:
            old_size = len(self.history)
            
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "text": safe_text,
                "intent": intent_stripped,
                "success": bool(success),
                "text_length_bytes": len(safe_text.encode('utf-8')),
            }
            
            self.history.append(entry)
            new_size = len(self.history)
            
            if new_size < old_size:
                self._discarded_items_count += 1
            
            self._invalidate_cache()
            self._save_history()
        
        return True
    
    def _sanitize_text(self, text: str) -> str:
        """Sanitize text for storage."""
        
        normalized = unicodedata.normalize('NFKC', text)
        
        cleaned = ''.join(
            c for c in normalized
            if unicodedata.category(c)[0] != 'C' or c == '\n'
        )
        
        cleaned = re.sub(r'\x00', '', cleaned)
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', cleaned)
        
        return cleaned.strip()
    
    def get_recent(self, n: int = 10) -> List[Dict]:
        """Get recent commands thread-safely."""
        
        if n is None or n < 0:
            n = 10
        
        with self._lock:
            return [dict(cmd) for cmd in list(self.history)[-n:]]
    
    def search_commands(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search commands safely."""
        
        if query is None or not isinstance(query, str):
            return []
        
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        with self._lock:
            results = [
                dict(cmd) for cmd in self.history
                if query_lower in cmd["text"].lower()
            ]
        
        return results[-max_results:] if max_results and max_results > 0 else results
    
    def get_command_frequency(self) -> Dict[str, int]:
        """Get frequency with caching."""
        
        if self._cache_valid:
            return dict(self._frequency_cache)
        
        with self._lock:
            intents = [cmd["intent"] for cmd in self.history]
            self._frequency_cache = dict(Counter(intents))
            self._cache_valid = True
        
        return dict(self._frequency_cache)
    
    def get_success_rate(self) -> float:
        """Calculate success rate safely."""
        
        with self._lock:
            if not self.history:
                return 0.0
            
            try:
                successful = sum(1 for cmd in self.history if cmd.get("success", False))
                return successful / len(self.history)
            except ZeroDivisionError:
                return 0.0
    
    def get_stats(self) -> Dict:
        """Get statistics with safety."""
        
        with self._lock:
            if not self.history:
                return {
                    "total": 0,
                    "success_rate": 0.0,
                    "intents": {},
                    "oldest": None,
                    "newest": None,
                    "discarded": self._discarded_items_count,
                }
            
            commands_list = list(self.history)
            
            return {
                "total": len(commands_list),
                "success_rate": self.get_success_rate(),
                "intents": self.get_command_frequency(),
                "oldest": commands_list[0].get("timestamp"),
                "newest": commands_list[-1].get("timestamp"),
                "discarded": self._discarded_items_count,
            }
    
    def clear_history(self) -> bool:
        """Clear history securely."""
        
        with self._lock:
            try:
                self.history.clear()
                self._invalidate_cache()
                self._save_history()
                logger.info("History cleared")
                return True
            except Exception as e:
                logger.error(f"Error clearing history: {e}", exc_info=True)
                return False
    
    def _invalidate_cache(self):
        """Invalidate cache (must be called with lock)."""
        self._cache_valid = False
    
    def _save_history(self) -> bool:
        """Save history with validation."""
        
        try:
            data = []
            for entry in self.history:
                try:
                    validated = {
                        "timestamp": entry.get("timestamp", datetime.now(timezone.utc).isoformat()),
                        "text": str(entry.get("text", "")).strip(),
                        "intent": str(entry.get("intent", "unknown")).strip(),
                        "success": bool(entry.get("success", False)),
                        "text_length_bytes": int(entry.get("text_length_bytes", 0)),
                    }
                    data.append(validated)
                except (ValueError, TypeError) as e:
                    logger.warning(f"Skipping invalid entry: {e}")
                    continue
            
            temp_path = self.config_path.with_suffix('.tmp')
            
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            temp_path.replace(self.config_path)
            return True
        
        except IOError as e:
            logger.error(f"IO error saving history: {e}", exc_info=True)
            return False
        except json.JSONDecodeError as e:
            logger.error(f"JSON error: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.critical(f"Unexpected error saving: {e}", exc_info=True)
            return False
    
    def _load_history(self) -> bool:
        """Load history safely."""
        
        try:
            if not self.config_path.exists():
                logger.debug("History file not found, starting fresh")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                logger.error("Invalid history format")
                return False
            
            with self._lock:
                self.history.clear()
                for entry in data[-self.MAX_HISTORY_SIZE:]:
                    if isinstance(entry, dict):
                        self.history.append(entry)
            
            logger.debug(f"Loaded {len(self.history)} commands")
            return True
        
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in history: {e}")
            return False
        except IOError as e:
            logger.warning(f"Could not load history: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error loading history: {e}", exc_info=True)
            return False
    
    def __del__(self):
        """Cleanup on deletion."""
        try:
            self._save_history()
        except:
            pass
