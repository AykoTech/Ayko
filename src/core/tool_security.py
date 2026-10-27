"""Default-deny capability policy for tools callable through the LLM."""

from types import MappingProxyType
from typing import Final


# New tools must be explicitly listed here before ToolRuntime will execute them.
# The LLM cannot grant itself capabilities through command arguments or state.
TOOL_CAPABILITIES: Final = MappingProxyType(
    {
        "open_app": "process.launch",
        "close_app": "process.terminate",
        "system_info": "system.read",
        "volume_control": "audio.change",
        "web_search": "browser.open",
        "open_url": "browser.open",
        "memory": "memory.read",
        "suggest": "suggestions.read",
        "context_awareness": "screen.read",
    }
)

# These capabilities are reserved for trusted application code and are never
# granted to LLM-routed tools.
PROTECTED_CAPABILITIES: Final = frozenset(
    {
        "permissions.manage",
        "permissions.modify",
        "monitoring.disable",
        "monitoring.stop",
        "operation_logs.modify",
        "operation_logs.delete",
    }
)


def is_capability_allowed(capability: str) -> bool:
    """Return whether a capability may be assigned to an LLM-routed tool."""
    return (
        isinstance(capability, str)
        and bool(capability)
        and capability not in PROTECTED_CAPABILITIES
    )


def is_tool_authorized(tool_name: str) -> bool:
    """Authorize only explicitly listed tools with non-protected capabilities."""
    capability = TOOL_CAPABILITIES.get(tool_name)
    return capability is not None and is_capability_allowed(capability)
