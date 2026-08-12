#!/usr/bin/env python3
"""JARVIS Core - Orchestrator."""

import logging
import threading
from typing import Dict, Optional
from datetime import datetime, timezone

logger = logging.getLogger("JARVISCore")


class JARVISCore:
    def __init__(self, llm=None):
        self.llm = llm
        self.state = "idle"
        self.timeline = []
        self.execution_lock = threading.RLock()
        self._timeline_lock = threading.RLock()
        self._parser = None
        self._executor = None
        self._init_components()
        logger.info("JARVISCore initialized")

    def _init_components(self):
        try:
            from .command_parser import CommandParser
            self._parser = CommandParser()
        except Exception as e:
            logger.warning(f"Parser unavailable: {e}")
        try:
            from .tool_registry import ToolExecutor
            self._executor = ToolExecutor
        except Exception as e:
            logger.warning(f"ToolExecutor unavailable: {e}")

    def execute_command(self, text: str) -> Dict:
        if not isinstance(text, str):
            raise TypeError("Command must be string")
        text = text.strip()
        if not text:
            return {"success": False, "result": "Empty command", "error": "ValidationError",
                    "intent": "unknown", "tool": "none", "timeline": []}
        if len(text.encode('utf-8')) > 5000:
            raise ValueError("Command exceeds maximum length")

        with self.execution_lock:
            timestamp = datetime.now(timezone.utc).isoformat()
            tl = []
            try:
                tl.append(f"[{timestamp}] START: {text[:50]}")

                intent, args = "unknown", {}
                if self.llm and self.llm.is_ready:
                    intent, args = self.llm.interpret(text)
                    tl.append(f"Intent: {intent}")

                tool_name = "unknown"
                if self._parser and intent != "unknown":
                    tool_name, args = self._parser.parse(intent, args)
                    tl.append(f"Tool: {tool_name}")

                result = {"success": True, "result": f"Executed: {text}", "state_updates": None, "log": ""}
                if self._executor and tool_name != "unknown":
                    result = self._executor.execute(tool_name, args, {"state": self.state})
                    if result.get("state_updates"):
                        self.state = str(result["state_updates"])

                tl.append(f"[{timestamp}] END: {'SUCCESS' if result['success'] else 'FAIL'}")
                with self._timeline_lock:
                    self.timeline.extend(tl)

                return {**result, "intent": intent, "tool": tool_name,
                        "timestamp": timestamp, "timeline": tl}

            except Exception as e:
                tl.append(f"[{timestamp}] ERROR: {type(e).__name__}: {e}")
                logger.error(f"Execution error: {e}", exc_info=True)
                return {"success": False, "result": "Execution error", "error": type(e).__name__,
                        "intent": "unknown", "tool": "none", "timestamp": timestamp, "timeline": tl}
