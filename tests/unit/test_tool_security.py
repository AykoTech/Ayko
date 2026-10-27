"""Tests for the default-deny tool capability policy."""

import pytest

from core.tool_runtime import ToolRuntime
from core.tool_security import (
    PROTECTED_CAPABILITIES,
    TOOL_CAPABILITIES,
    is_capability_allowed,
    is_tool_authorized,
)


class StubTool:
    def __init__(self):
        self.validated = False
        self.executed = False

    def validate_args(self, args):
        self.validated = True
        return True, ""

    def execute(self, args, state):
        self.executed = True
        return {
            "success": True,
            "result": "executed",
            "state_updates": None,
            "log": "stub executed",
        }


@pytest.mark.parametrize("capability", sorted(PROTECTED_CAPABILITIES))
def test_protected_capabilities_are_never_allowed(capability):
    assert is_capability_allowed(capability) is False


@pytest.mark.parametrize("tool_name", sorted(TOOL_CAPABILITIES))
def test_existing_tools_are_explicitly_authorized(tool_name):
    assert is_tool_authorized(tool_name) is True


@pytest.mark.parametrize(
    "tool_name",
    [
        "set_permissions",
        "disable_monitoring",
        "stop_monitoring",
        "modify_operation_logs",
        "delete_operation_logs",
    ],
)
def test_registered_tool_without_policy_entry_is_denied_before_execution(tool_name):
    tool = StubTool()
    runtime = ToolRuntime({tool_name: tool})

    result = runtime.execute(tool_name, {}, {})

    assert result["success"] is False
    assert "not authorized" in result["result"].lower()
    assert tool.validated is False
    assert tool.executed is False


def test_authorized_tool_still_executes():
    tool = StubTool()
    runtime = ToolRuntime({"system_info": tool})

    result = runtime.execute("system_info", {}, {})

    assert result["success"] is True
    assert tool.validated is True
    assert tool.executed is True


def test_unknown_tool_capability_defaults_to_denied():
    assert is_tool_authorized("new_tool_not_in_policy") is False
