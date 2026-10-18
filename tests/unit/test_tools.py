# Percorso: tests/unit/test_tools.py
"""Unit tests for system-facing tools."""

from unittest.mock import patch

from core.tools import OpenAppTool


def test_open_app_windows_uses_shell_execute_without_a_command_shell():
    """Opening an app on Windows must not parse the app name as shell code."""
    tool = OpenAppTool()
    tool.system = "Windows"

    with patch("core.tools.os.startfile", create=True) as startfile:
        result = tool.execute({"app": "calculator & unexpected-command"}, {})

    startfile.assert_called_once_with("calculator & unexpected-command")
    assert result["success"] is True
