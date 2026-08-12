#!/usr/bin/env python3
"""Learning Schedule - Ultimate version with all fixes."""

import logging
import threading
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from collections import Counter, deque

logger = logging.getLogger("Learning")

class LearningSchedule:
    """Ultimate learning schedule."""
    
    def __init__(self, max_history: int = 1000):
        self.command_patterns: Dict[str, deque] = {}
        self.time_patterns: Dict[int, deque] = {}
        self.weekly_patterns: Dict[str, deque] = {}
        self.user_preferences: Dict = {}
        self.max_history = max_history
        self._lock = threading.RLock()
        
        logger.info("✓ LearningSchedule initialized")
    
    def record_command_usage(self, command: str, time: datetime = None) -> bool:
        """Record command safely."""
        
        if command is None or not isinstance(command, str):
            return False
        
        command = command.strip()
        if not command:
            return False
        
        if time is None:
            time = datetime.now(timezone.utc)
        
        if not isinstance(time, datetime):
            return False
        
        hour = time.hour
        day = time.strftime("%A")
        
        try:
            with self._lock:
                if command not in self.command_patterns:
                    self.command_patterns[command] = deque(maxlen=self.max_history)
                
                self.command_patterns[command].append(hour)
                
                if hour not in self.time_patterns:
                    self.time_patterns[hour] = deque(maxlen=self.max_history)
                
                self.time_patterns[hour].append(command)
                
                if day not in self.weekly_patterns:
                    self.weekly_patterns[day] = deque(maxlen=self.max_history)
                
                self.weekly_patterns[day].append(command)
            
            return True
        
        except Exception as e:
            logger.error(f"Error recording: {e}", exc_info=True)
            return False
    
    def get_peak_hours_for_command(self, command: str) -> Optional[int]:
        """Get peak hour safely."""
        
        if command is None or not isinstance(command, str):
            return None
        
        command = command.strip()
        
        with self._lock:
            if command not in self.command_patterns:
                return None
            
            hours = list(self.command_patterns[command])
            
            if not hours:
                return None
            
            try:
                counter = Counter(hours)
                most_common_hour, count = counter.most_common(1)[0]
                return most_common_hour
            except (IndexError, ValueError) as e:
                logger.warning(f"Error finding peak: {e}")
                return None
    
    def predict_next_command(self) -> Optional[str]:
        """Predict next command safely."""
        
        now = datetime.now(timezone.utc)
        hour = now.hour
        
        with self._lock:
            if hour not in self.time_patterns:
                return None
            
            commands = list(self.time_patterns[hour])
            
            if not commands:
                return None
            
            try:
                counter = Counter(commands)
                predicted_command, _ = counter.most_common(1)[0]
                return predicted_command
            except (IndexError, ValueError) as e:
                logger.warning(f"Error predicting: {e}")
                return None
    
    def get_commands_for_time(self, hour: int) -> List[str]:
        """Get commands for time."""
        
        if hour is None or not isinstance(hour, int):
            return []
        
        if not (0 <= hour < 24):
            return []
        
        with self._lock:
            return list(self.time_patterns.get(hour, []))
    
    def get_commands_for_day(self, day: str) -> List[str]:
        """Get commands for day."""
        
        if day is None or not isinstance(day, str):
            return []
        
        day = day.strip()
        
        with self._lock:
            return list(self.weekly_patterns.get(day, []))
    
    def get_command_frequency(self, command: str = None) -> Dict[str, int]:
        """Get frequency safely."""
        
        with self._lock:
            if command is None:
                frequency = {}
                for cmd, hours in self.command_patterns.items():
                    frequency[cmd] = len(list(hours))
                return frequency
            else:
                cmd_stripped = command.strip() if isinstance(command, str) else None
                if cmd_stripped in self.command_patterns:
                    return {cmd_stripped: len(list(self.command_patterns[cmd_stripped]))}
                return {}
    
    def analyze_patterns(self) -> Dict:
        """Analyze patterns safely."""
        
        with self._lock:
            if not self.command_patterns:
                return {"status": "No patterns"}
            
            total = sum(len(h) for h in self.command_patterns.values())
            
            peak_hour = None
            max_count = 0
            for hour, cmds in self.time_patterns.items():
                if len(cmds) > max_count:
                    max_count = len(cmds)
                    peak_hour = hour
            
            return {
                "total_commands_tracked": len(self.command_patterns),
                "total_executions": total,
                "peak_hour": peak_hour,
                "patterns_detected": len([c for c in self.command_patterns.values() if len(c) > 2]),
            }
    
    def record_preference(self, key: str, value) -> bool:
        """Record preference safely."""
        
        if key is None or not isinstance(key, str):
            return False
        
        key = key.strip()
        if not key:
            return False
        
        try:
            with self._lock:
                self.user_preferences[key] = value
                logger.debug(f"Preference: {key}")
                return True
        except Exception as e:
            logger.error(f"Error recording preference: {e}")
            return False
    
    def get_learning_stats(self) -> Dict:
        """Get stats safely."""
        
        with self._lock:
            return {
                "commands_tracked": len(self.command_patterns),
                "total_usage": sum(len(h) for h in self.command_patterns.values()),
                "peak_hours": self.analyze_patterns().get("peak_hour"),
                "preferences_stored": len(self.user_preferences),
                "weekly_patterns": len(self.weekly_patterns),
            }
