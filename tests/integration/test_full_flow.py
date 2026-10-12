#!/usr/bin/env python3
"""Integration tests for full AYKO flow."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


class FakeLLM:
    is_ready = True
    last_error = ""

    def __init__(self, intent="test_intent", args=None):
        self.intent = intent
        self.args = args or {}

    def interpret(self, text):
        return self.intent, self.args


class FakeParser:
    def parse(self, intent, args):
        return "test_tool", args


class FakeExecutor:
    @staticmethod
    def execute(tool_name, args, context):
        return {
            "success": True,
            "result": "Mock tool executed",
            "state_updates": None,
            "log": "mock execution",
        }


def test_full_command_execution(mock_core, monkeypatch):
    """A supported command succeeds only when a tool reports success."""
    mock_core.llm = FakeLLM()
    mock_core._parser = FakeParser()
    mock_core._executor = FakeExecutor

    result = mock_core.execute_command("test command")

    assert result["success"] is True
    assert result["result"] == "Mock tool executed"
    assert result["tool"] == "test_tool"
    assert result["timestamp"] is not None


def test_unknown_intent_is_not_reported_as_success(mock_core):
    """An unknown intent must not be reported as a successful execution."""
    mock_core.llm = FakeLLM(intent="unknown")

    result = mock_core.execute_command("unsupported command")

    assert result["success"] is False
    assert result["tool"] == "unknown"


def test_missing_llm_reports_failure(mock_core):
    """A missing AI engine must produce an explicit failure."""
    result = mock_core.execute_command("test command")

    assert result["success"] is False
    assert result["error"] == "RuntimeError"


def test_command_memory_integration(mock_command_memory):
    """Test command memory integration."""
    mock_command_memory.add_command("open chrome", "open_app", True)

    recent = mock_command_memory.get_recent()

    assert len(recent) > 0
    assert "open" in recent[0]["text"].lower()
