#!/usr/bin/env python3
"""
JARVIS v0.0.01 - Desktop AI Assistant
GNU General Public License v3.0
Copyright (C) 2026 Edoardo Pensi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

For more info: https://www.gnu.org/licenses/gpl-3.0.html
"""

import logging
from typing import Dict, Any, Tuple
from datetime import datetime

from .llm_engine import LLMEngine
from .command_parser import CommandParser
from .tool_registry import ToolExecutor

logger = logging.getLogger("Core")

class JARVISCore:
    """Orchestrate command execution.
    
    Flow:
    1. User text → LLM (interpret to intent + args)
    2. Intent + args → Parser (map to tool)
    3. Tool + args → Executor (run tool)
    4. Result → return
    """
    
    def __init__(self, llm_engine: LLMEngine):
        self.llm = llm_engine
        self.parser = CommandParser()
        self.state = {
            "last_action": None,
            "last_result": None,
            "volume": 50,
            "timestamp": None,
        }
        logger.info("✓ Core initialized")
    
    def execute_command(self, user_text: str) -> Dict[str, Any]:
        """Execute user command.
        
        Args:
            user_text: Raw user input
        
        Returns:
            {
                "success": bool,
                "user_text": str,
                "intent": str,
                "tool": str,
                "result": any,
                "state": dict,
                "error": str | None,
                "timeline": list
            }
        """
        
        timeline = []
        timestamp = datetime.now().isoformat()
        
        try:
            # STEP 1: LLM Interpretation
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] LLM interpreting...")
            logger.info(f"Step 1: LLM → {user_text}")
            
            intent, args = self.llm.interpret(user_text)
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] Intent: {intent}")
            
            if intent == "unknown":
                return {
                    "success": False,
                    "user_text": user_text,
                    "intent": "unknown",
                    "tool": None,
                    "result": "Could not understand command",
                    "state": self.state,
                    "error": "Intent not recognized",
                    "timeline": timeline
                }
            
            # STEP 2: Command Parser (Intent → Tool)
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] Parsing...")
            logger.info(f"Step 2: Parser → {intent}")
            
            tool, mapped_args = self.parser.parse(intent, args)
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] Tool: {tool}")
            
            if tool == "unknown":
                return {
                    "success": False,
                    "user_text": user_text,
                    "intent": intent,
                    "tool": "unknown",
                    "result": f"No tool for intent: {intent}",
                    "state": self.state,
                    "error": "Tool mapping failed",
                    "timeline": timeline
                }
            
            # STEP 3: Tool Execution
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] Executing tool...")
            logger.info(f"Step 3: Execute {tool} with {mapped_args}")
            
            tool_result = ToolExecutor.execute(tool, mapped_args, self.state)
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] {tool_result['log']}")
            
            # Update state if tool returned updates
            if tool_result.get("state_updates"):
                self.state.update(tool_result["state_updates"])
            
            self.state["last_action"] = tool
            self.state["last_result"] = tool_result
            self.state["timestamp"] = timestamp
            
            return {
                "success": tool_result["success"],
                "user_text": user_text,
                "intent": intent,
                "tool": tool,
                "result": tool_result["result"],
                "state": self.state,
                "error": None if tool_result["success"] else tool_result["result"],
                "timeline": timeline
            }
        
        except Exception as e:
            logger.error(f"Core execution error: {e}", exc_info=True)
            timeline.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {e}")
            
            return {
                "success": False,
                "user_text": user_text,
                "intent": None,
                "tool": None,
                "result": str(e),
                "state": self.state,
                "error": str(e),
                "timeline": timeline
            }
    
    def get_state(self) -> Dict:
        """Get current global state."""
        return self.state.copy()
    
    def reset_state(self):
        """Reset state to defaults."""
        self.state = {
            "last_action": None,
            "last_result": None,
            "volume": 50,
            "timestamp": None,
        }
        logger.info("State reset")
