#!/usr/bin/env python3
"""
Command Suggester - Suggest similar commands when input unrecognized.
GNU General Public License v3.0

RESPONSIBILITY: Find similar commands, rank by relevance, return suggestions.
Does NOT execute. Does NOT make decisions.
Returns: List of suggestion dictionaries.
"""

import logging
from typing import List, Dict, Optional
from difflib import SequenceMatcher

logger = logging.getLogger("CommandSuggester")

class CommandSuggester:
    """Suggest similar commands based on user input."""
    
    def __init__(self):
        # Predefined command examples and intents
        self.command_database = {
            "open_app": [
                "open chrome", "open firefox", "open vscode", "open notepad",
                "open spotify", "open discord", "open slack", "open telegram",
                "launch chrome", "start chrome", "run chrome"
            ],
            "close_app": [
                "close chrome", "close firefox", "close notepad", "close spotify",
                "kill chrome", "terminate chrome", "exit chrome", "quit chrome",
                "close vscode"
            ],
            "system_info": [
                "what time is it", "current time", "what's the time",
                "system information", "device info", "cpu usage", "memory usage",
                "battery status", "disk space", "temperature"
            ],
            "web_search": [
                "search google", "search python", "google it", "find",
                "lookup", "search web", "bing search", "internet search"
            ],
            "volume_control": [
                "set volume", "volume 80", "mute", "unmute", "volume up",
                "volume down", "increase volume", "decrease volume"
            ],
            "show_history": [
                "what did i do", "show history", "recent commands", "my history",
                "command history", "what have i done"
            ]
        }
        
        logger.info(f"✓ CommandSuggester initialized with {len(self.command_database)} intents")
    
    def suggest(self, user_input: str, threshold: float = 0.5, max_suggestions: int = 3) -> Optional[List[Dict]]:
        """Suggest similar commands.
        
        Args:
            user_input: User's unrecognized command
            threshold: Similarity threshold (0.0-1.0)
            max_suggestions: Maximum suggestions to return
            
        Returns:
            List of suggestions or None if no good matches
        """
        if not user_input or not user_input.strip():
            return None
        
        user_input_lower = user_input.lower().strip()
        all_suggestions = []
        
        # Compare against all known commands
        for intent, commands in self.command_database.items():
            for command in commands:
                similarity = SequenceMatcher(None, user_input_lower, command).ratio()
                
                if similarity >= threshold:
                    all_suggestions.append({
                        "command": command,
                        "intent": intent,
                        "similarity": similarity,
                        "confidence": self._calculate_confidence(similarity)
                    })
        
        if not all_suggestions:
            logger.debug(f"No suggestions found for: {user_input}")
            return None
        
        # Sort by similarity descending
        all_suggestions.sort(key=lambda x: x["similarity"], reverse=True)
        
        # Return top suggestions
        suggestions = all_suggestions[:max_suggestions]
        
        logger.debug(f"Found {len(suggestions)} suggestions for '{user_input}'")
        return suggestions
    
    def suggest_by_intent(self, user_intent: str, max_suggestions: int = 3) -> Optional[List[Dict]]:
        """Suggest commands for a specific intent.
        
        Used when parser couldn't find tool for intent.
        Example: User says "open xyz" → LLM detects "open_app"
                 But "xyz" is not recognized
        """
        if user_intent not in self.command_database:
            return None
        
        commands = self.command_database[user_intent]
        suggestions = [
            {
                "command": cmd,
                "intent": user_intent,
                "similarity": 1.0,
                "confidence": "high",
                "reason": "Similar intent detected"
            }
            for cmd in commands[:max_suggestions]
        ]
        
        return suggestions
    
    def autocomplete(self, partial_input: str) -> Optional[List[str]]:
        """Autocomplete based on partial input.
        
        Used for UI autocomplete dropdown.
        Example: User types "op" → suggests "open chrome", "open vscode"
        """
        if not partial_input or len(partial_input) < 2:
            return None
        
        partial_lower = partial_input.lower()
        matches = []
        
        for intent, commands in self.command_database.items():
            for command in commands:
                if command.startswith(partial_lower):
                    matches.append(command)
        
        return matches[:5] if matches else None
    
    def get_intent_description(self, intent: str) -> Optional[str]:
        """Get human-readable description for intent.
        
        Used for help text.
        """
        descriptions = {
            "open_app": "Open or launch an application",
            "close_app": "Close or quit an application",
            "system_info": "Get system information (time, CPU, memory, etc)",
            "web_search": "Search the web for information",
            "volume_control": "Adjust system volume",
            "show_history": "Show your command history",
        }
        
        return descriptions.get(intent)
    
    def _calculate_confidence(self, similarity: float) -> str:
        """Convert similarity score to confidence level."""
        if similarity >= 0.9:
            return "very_high"
        elif similarity >= 0.75:
            return "high"
        elif similarity >= 0.6:
            return "medium"
        else:
            return "low"
    
    def get_all_commands(self) -> Dict[str, List[str]]:
        """Get all available commands (for help/documentation)."""
        return self.command_database.copy()
    
    def add_custom_command(self, intent: str, command: str) -> bool:
        """Add custom command example.
        
        Used when user creates custom action.
        """
        if intent not in self.command_database:
            self.command_database[intent] = []
        
        if command not in self.command_database[intent]:
            self.command_database[intent].append(command)
            logger.info(f"Custom command added: {command} → {intent}")
            return True
        
        return False
