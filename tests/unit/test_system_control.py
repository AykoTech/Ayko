# Percorso: tests/unit/test_system_control.py
"""Unit tests for operating-system control helpers."""

from subprocess import CompletedProcess
from unittest.mock import patch

from utils.system_control import SystemControl


def test_lock_screen_reports_a_system_command_failure():
    """The helper must not report success when Windows rejects the request."""
    with patch("utils.system_control.platform.system", return_value="Windows"), patch(
        "utils.system_control.subprocess.run",
        return_value=CompletedProcess([], 1),
    ):
        result = SystemControl.lock_screen()

    assert result is False


def test_lock_screen_reports_successful_system_command():
    """The helper reports success only after the system accepts the request."""
    with patch("utils.system_control.platform.system", return_value="Windows"), patch(
        "utils.system_control.subprocess.run",
        return_value=CompletedProcess([], 0),
    ):
        result = SystemControl.lock_screen()

    assert result is True
