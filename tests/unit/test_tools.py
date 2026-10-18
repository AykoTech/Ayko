# Percorso: tests/unit/test_tools.py
"""Unit tests for system-facing tools."""

from subprocess import CompletedProcess
from unittest.mock import patch

from core.tools import (
    CloseAppTool,
    MemoryTool,
    OpenAppTool,
    OpenUrlTool,
    VolumeControlTool,
    WebSearchTool,
)
from core.command_memory import CommandMemory


def test_open_app_windows_uses_shell_execute_without_a_command_shell():
    """Opening an app on Windows must not parse the app name as shell code."""
    tool = OpenAppTool()
    tool.system = "Windows"

    with patch("core.tools.os.startfile", create=True) as startfile:
        result = tool.execute({"app": "calculator & unexpected-command"}, {})

    startfile.assert_called_once_with("calculator & unexpected-command")
    assert result["success"] is True


def test_close_app_reports_system_command_failure():
    """Closing an app must fail when the operating system rejects the request."""
    tool = CloseAppTool()
    tool.system = "Windows"

    with patch(
        "core.tools.subprocess.run",
        return_value=CompletedProcess([], 128, stderr="Process not found"),
    ):
        result = tool.execute({"app": "missing.exe"}, {})

    assert result["success"] is False
    assert result["result"] == "Process not found"


def test_volume_control_windows_sets_the_requested_level():
    """Windows volume control must call the native API with the requested level."""
    tool = VolumeControlTool()
    tool.system = "Windows"

    with patch("core.tools.ctypes.windll.winmm.waveOutSetVolume", return_value=0) as setter:
        result = tool.execute({"level": 50}, {})

    _, volume = setter.call_args.args
    assert volume & 0xFFFF == round(50 * 0xFFFF / 100)
    assert volume >> 16 == round(50 * 0xFFFF / 100)
    assert result["success"] is True


def test_volume_control_rejects_a_non_numeric_level():
    """Invalid volume input must produce a validation failure instead of an exception."""
    tool = VolumeControlTool()

    assert tool.validate_args({"level": None}) == (False, "level must be integer")


def test_text_tools_reject_missing_non_text_or_blank_input():
    """System and web tools require meaningful text inputs."""
    assert OpenAppTool().validate_args({"app": "  "}) == (False, "app parameter required")
    assert CloseAppTool().validate_args({"app": ["calculator"]}) == (
        False,
        "app parameter required",
    )
    assert WebSearchTool().validate_args({"query": None}) == (
        False,
        "query parameter required",
    )


def test_web_search_url_encodes_special_characters():
    """Search input becomes a query parameter rather than part of the URL syntax."""
    tool = WebSearchTool()

    with patch("core.tools.webbrowser.open", return_value=True) as open_browser:
        result = tool.execute({"query": "c++ & python"}, {})

    open_browser.assert_called_once_with("https://google.com/search?q=c%2B%2B+%26+python")
    assert result["success"] is True


def test_open_url_allows_only_web_schemes():
    """The browser tool only accepts HTTP(S) URLs."""
    tool = OpenUrlTool()

    assert tool.validate_args({"url": "https://example.com"}) == (True, "")
    assert tool.validate_args({"url": "file:///sensitive.txt"}) == (
        False,
        "url must use http or https",
    )


def test_memory_tool_reads_the_memory_provided_by_the_core(tmp_path):
    """The memory tool reports statistics from the memory instance in its state."""
    memory = CommandMemory(config_path=tmp_path / "history.json")
    memory.add_command("open calculator", "open_app", True)
    memory.add_command("open browser", "open_app", False)

    result = MemoryTool().execute(
        {"query": "stats"}, {"memory": memory}
    )

    assert result["success"] is True
    assert "issued 2 commands" in result["result"]
    assert "Most used: open_app" in result["result"]
