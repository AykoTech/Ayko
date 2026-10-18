# Percorso: tests/integration/test_full_flow.py
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


class UnknownParser:
    def parse(self, intent, args):
        return "unknown", args


class FakeExecutor:
    @staticmethod
    def execute(tool_name, args, context):
        return {
            "success": True,
            "result": "Mock tool executed",
            "state_updates": None,
            "log": "mock execution",
        }


class InvalidExecutor:
    @staticmethod
    def execute(tool_name, args, context):
        return {
            "success": "yes",
            "result": "This must not be accepted as success",
            "state_updates": None,
            "log": "invalid success type",
        }


def test_full_command_execution(mock_core):
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


def test_unknown_parser_tool_is_not_reported_as_success(mock_core):
    """An intent without a registered tool must fail."""
    mock_core.llm = FakeLLM()
    mock_core._parser = UnknownParser()
    mock_core._executor = FakeExecutor

    result = mock_core.execute_command("unsupported command")

    assert result["success"] is False
    assert result["tool"] == "unknown"


def test_invalid_executor_response_is_not_reported_as_success(mock_core):
    """The executor must return a dictionary with a boolean success field."""
    mock_core.llm = FakeLLM()
    mock_core._parser = FakeParser()
    mock_core._executor = InvalidExecutor

    result = mock_core.execute_command("test command")

    assert result["success"] is False
    assert result["result"] == "Risposta non valida dall'esecutore"


def test_missing_parser_reports_failure(mock_core):
    """A missing command parser must produce an explicit failure."""
    mock_core.llm = FakeLLM()
    mock_core._parser = None

    result = mock_core.execute_command("test command")

    assert result["success"] is False
    assert result["result"] == "Parser dei comandi non disponibile"


def test_missing_executor_reports_failure(mock_core):
    """A missing tool executor must produce an explicit failure."""
    mock_core.llm = FakeLLM()
    mock_core._parser = FakeParser()
    mock_core._executor = None

    result = mock_core.execute_command("test command")

    assert result["success"] is False
    assert result["result"] == "Esecutore degli strumenti non disponibile"


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


class FailedExecutorWithStateUpdates:
    @staticmethod
    def execute(tool_name, args, context):
        return {
            "success": False,
            "result": "Mock failure",
            "state_updates": {"unexpected": True},
            "log": "mock failure",
        }


class SuccessfulExecutorWithStateUpdates:
    @staticmethod
    def execute(tool_name, args, context):
        return {
            "success": True,
            "result": "Mock success",
            "state_updates": {"expected": True},
            "log": "mock success",
        }


def test_failed_tool_does_not_update_context(mock_core):
    """A failed tool must not mutate the core context."""
    mock_core.llm = FakeLLM()
    mock_core._parser = FakeParser()
    mock_core._executor = FailedExecutorWithStateUpdates

    result = mock_core.execute_command("test command")

    assert result["success"] is False
    assert "unexpected" not in mock_core.context


def test_successful_tool_updates_context(mock_core):
    """A successful tool may apply its state updates."""
    mock_core.llm = FakeLLM()
    mock_core._parser = FakeParser()
    mock_core._executor = SuccessfulExecutorWithStateUpdates

    result = mock_core.execute_command("test command")

    assert result["success"] is True
    assert mock_core.context["expected"] is True


class FailedExecutorThatMutatesContext:
    @staticmethod
    def execute(tool_name, args, state):
        state["context"]["nested"]["items"].append("unexpected")
        state["context"]["unexpected"] = True
        return {
            "success": False,
            "result": "Mock failure",
            "state_updates": None,
            "log": "mutated context before failure",
        }


def test_failed_tool_cannot_mutate_live_context(mock_core):
    """A failing tool cannot mutate even nested values in the core context."""
    mock_core.context = {"nested": {"items": ["original"]}}
    mock_core.llm = FakeLLM()
    mock_core._parser = FakeParser()
    mock_core._executor = FailedExecutorThatMutatesContext

    result = mock_core.execute_command("test command")

    assert result["success"] is False
    assert mock_core.context == {"nested": {"items": ["original"]}}
