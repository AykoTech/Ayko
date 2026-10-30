"""Tests for the tamper-evident operation audit log."""

import json

import pytest

from core.audit_log import AuditLogIntegrityError, OperationAuditLog
from core.tool_runtime import ToolRuntime


def test_hash_chain_round_trips_and_links_records(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)

    first_hash = audit.append("started", "system_info")
    second_hash = audit.append("completed", "system_info", True)

    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert len(records) == 2
    assert records[0]["hash"] == first_hash
    assert records[1]["hash"] == second_hash
    assert records[1]["prev_hash"] == first_hash
    assert audit.verify() is True


def test_verify_detects_modified_record(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)
    audit.append("completed", "system_info", True)

    record = json.loads(path.read_text(encoding="utf-8"))
    record["tool"] = "open_app"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    with pytest.raises(AuditLogIntegrityError, match="verification failed"):
        audit.verify()


def test_verify_detects_valid_suffix_truncation_in_same_session(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)
    audit.append("started", "system_info")
    audit.append("completed", "system_info", True)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    path.write_text(lines[0] + "\n", encoding="utf-8")

    with pytest.raises(AuditLogIntegrityError, match="session checkpoint"):
        audit.verify()


def test_verify_rejects_incomplete_record(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)
    audit.append("started", "system_info")
    path.write_text(path.read_text(encoding="utf-8").rstrip("\n"), encoding="utf-8")

    with pytest.raises(AuditLogIntegrityError, match="incomplete record"):
        audit.verify()


def test_audit_record_contains_only_minimal_metadata(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)
    audit.append("completed", "open_url", True)

    record = json.loads(path.read_text(encoding="utf-8"))
    assert set(record) == {"timestamp", "event", "tool", "success", "prev_hash", "hash"}
    assert "arguments" not in record
    assert "result" not in record


class StubTool:
    def __init__(self):
        self.executed = False

    def validate_args(self, args):
        return True, ""

    def execute(self, args, state):
        self.executed = True
        return {
            "success": True,
            "result": "executed",
            "state_updates": None,
            "log": "stub executed",
        }


def test_runtime_blocks_execution_when_audit_log_is_tampered(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)
    audit.append("completed", "system_info", True)

    record = json.loads(path.read_text(encoding="utf-8"))
    record["tool"] = "open_app"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")

    tool = StubTool()
    runtime = ToolRuntime({"system_info": tool}, audit_log=audit)
    result = runtime.execute("system_info", {}, {})

    assert result["success"] is False
    assert "audit log" in result["result"].lower()
    assert tool.executed is False


def test_runtime_blocks_execution_after_valid_suffix_truncation(tmp_path):
    path = tmp_path / "operations.jsonl"
    audit = OperationAuditLog(path)
    audit.append("started", "system_info")
    audit.append("completed", "system_info", True)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    path.write_text(lines[0] + "\n", encoding="utf-8")

    tool = StubTool()
    runtime = ToolRuntime({"system_info": tool}, audit_log=audit)
    result = runtime.execute("system_info", {}, {})

    assert result["success"] is False
    assert "audit log" in result["result"].lower()
    assert tool.executed is False
