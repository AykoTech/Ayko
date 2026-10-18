# Percorso: tests/unit/test_tools.py
"""Unit tests for system-facing tools."""

from subprocess import CompletedProcess
from unittest.mock import patch

from core.tools import CloseAppTool, OpenAppTool, VolumeControlTool


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
