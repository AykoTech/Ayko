"""Tool Runtime - centralized execution boundary for registered tools."""

import logging
from typing import Any, Dict

from .audit_log import OperationAuditLog
from .tool_security import is_tool_authorized

logger = logging.getLogger("ToolRuntime")


class ToolRuntime:
    """Resolve, authorize, validate and execute tools through one boundary."""

    def __init__(self, registry: Dict[str, Any], audit_log=None):
        self.registry = registry
        self.audit_log = audit_log or OperationAuditLog()

    def get_tool(self, tool_name: str):
        """Return a registered tool, or None when it does not exist."""
        tool = self.registry.get(tool_name)
        if tool is None:
            logger.warning("Tool not found: %s", tool_name)
        return tool

    def _record_audit(self, event: str, tool_name: str, success=None):
        """Record metadata only; never persist command text, arguments or results."""
        try:
            self.audit_log.append(event, str(tool_name), success)
        except Exception as exc:
            logger.error(
                "Operation audit log failure during %s for %s: %s",
                event,
                tool_name,
                exc,
            )
            return "Operation audit log integrity/write check failed."
        return None

    @staticmethod
    def _failure(result: str, log: str, audit_warning=None) -> dict:
        response = {
            "success": False,
            "result": result,
            "state_updates": None,
            "log": log,
        }
        if audit_warning:
            response["audit_warning"] = audit_warning
        return response

    def execute(self, tool_name: str, args: dict, state: dict) -> dict:
        """Authorize, validate, audit and execute a tool through one boundary."""
        tool = self.get_tool(tool_name)
        if tool is None:
            warning = self._record_audit("tool_not_found", tool_name, False)
            return self._failure(
                f"Tool {tool_name} not found",
                f"Unknown tool: {tool_name}",
                warning,
            )

        if not is_tool_authorized(tool_name):
            logger.warning("Authorization denied for tool: %s", tool_name)
            warning = self._record_audit("authorization_denied", tool_name, False)
            return self._failure(
                f"Tool '{tool_name}' is not authorized by the security policy",
                f"Authorization denied for tool: {tool_name}",
                warning,
            )

        try:
            is_valid, error_msg = tool.validate_args(args)
        except Exception as exc:
            warning = self._record_audit("validation_error", tool_name, False)
            return self._failure(
                f"Tool argument validation failed: {exc}",
                f"Validation error for {tool_name}",
                warning,
            )

        if not is_valid:
            warning = self._record_audit("validation_rejected", tool_name, False)
            return self._failure(
                error_msg,
                f"Invalid args for {tool_name}: {error_msg}",
                warning,
            )

        # Fail closed: a tool is never invoked unless its start event is recorded.
        warning = self._record_audit("started", tool_name, None)
        if warning:
            return self._failure(
                "Tool execution blocked because the operation audit log could not be verified or written",
                "Audit log integrity/write check failed; tool was not executed",
                warning,
            )

        try:
            result = tool.execute(args, state)
        except Exception as exc:
            logger.error("Tool execution error for %s: %s", tool_name, exc)
            warning = self._record_audit("execution_failed", tool_name, False)
            return self._failure(
                str(exc),
                f"Execution error: {exc}",
                warning,
            )

        if not isinstance(result, dict) or not isinstance(result.get("success"), bool):
            result = self._failure(
                "Tool returned an invalid result",
                f"Invalid result from tool: {tool_name}",
            )

        logger.info("Tool %s: %s", tool_name, result.get("log", ""))
        warning = self._record_audit("completed", tool_name, result["success"])
        if warning:
            # The tool may already have produced a side effect. Preserve its real
            # outcome and report that the completion event could not be persisted.
            result = dict(result)
            result["audit_warning"] = (
                "Tool returned a result, but its outcome could not be recorded. "
                "Review the operation audit log."
            )
        return result
