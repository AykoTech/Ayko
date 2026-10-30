"""Tamper-evident local audit log for tool operations.

The hash chain detects edits and reordering. The in-memory checkpoint also
detects valid suffix truncation while this instance remains alive. After a
restart, truncation of a valid suffix still cannot be detected without an
independently stored trusted checkpoint. This is not an OS-level security
boundary: a process with write access can replace the file and its contents.
"""

import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


_ZERO_HASH = "0" * 64
_RECORD_KEYS = {"timestamp", "event", "tool", "success", "prev_hash", "hash"}


class AuditLogIntegrityError(RuntimeError):
    """Raised when the audit log cannot be verified or safely updated."""


class OperationAuditLog:
    """Append-only JSONL log with a SHA-256 hash chain and session checkpoint."""

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path is not None else (
            Path.home() / ".ayko" / "logs" / "operations.jsonl"
        )
        self._lock = threading.RLock()
        self._verified = False
        self._last_hash = _ZERO_HASH
        self._event_count = 0
        self._signature = None

    @staticmethod
    def _canonical_json(payload: dict) -> str:
        return json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )

    @classmethod
    def _digest(cls, payload: dict) -> str:
        return hashlib.sha256(cls._canonical_json(payload).encode("utf-8")).hexdigest()

    def _file_signature(self):
        try:
            stat = self.path.stat()
        except FileNotFoundError:
            return None
        return stat.st_size, stat.st_mtime_ns, getattr(stat, "st_ino", None)

    def verify(self) -> bool:
        """Verify every record and raise AuditLogIntegrityError on any mismatch."""
        with self._lock:
            self._verify_file()
        return True

    def _refresh_integrity(self) -> None:
        if not self._verified or self._file_signature() != self._signature:
            self._verify_file()

    def _verify_file(self) -> None:
        # Keep the last state verified by this live instance. A valid but shorter
        # chain must not replace that trusted state during the same session.
        was_verified = self._verified
        trusted_hash = self._last_hash
        trusted_count = self._event_count

        if not self.path.exists():
            if trusted_count:
                raise AuditLogIntegrityError("Audit log was removed during this session")
            self._last_hash = _ZERO_HASH
            self._event_count = 0
            self._signature = None
            self._verified = True
            return

        previous_hash = _ZERO_HASH
        count = 0
        try:
            with self.path.open("r", encoding="utf-8", newline="") as stream:
                for line_number, line in enumerate(stream, start=1):
                    if not line.endswith("\n"):
                        raise AuditLogIntegrityError(
                            f"Audit log has an incomplete record at line {line_number}"
                        )
                    try:
                        record = json.loads(line)
                    except (json.JSONDecodeError, TypeError) as exc:
                        raise AuditLogIntegrityError(
                            f"Audit log contains invalid JSON at line {line_number}"
                        ) from exc

                    if not isinstance(record, dict) or set(record) != _RECORD_KEYS:
                        raise AuditLogIntegrityError(
                            f"Audit log record has an invalid schema at line {line_number}"
                        )

                    payload = {key: value for key, value in record.items() if key != "hash"}
                    digest = record.get("hash")
                    if (
                        not isinstance(payload.get("timestamp"), str)
                        or not isinstance(payload.get("event"), str)
                        or not payload["event"]
                        or not isinstance(payload.get("tool"), str)
                        or not payload["tool"]
                        or payload.get("success") is not None
                        and not isinstance(payload.get("success"), bool)
                        or payload.get("prev_hash") != previous_hash
                        or not isinstance(digest, str)
                        or digest != self._digest(payload)
                    ):
                        raise AuditLogIntegrityError(
                            f"Audit log hash-chain verification failed at line {line_number}"
                        )

                    previous_hash = digest
                    count += 1
        except OSError as exc:
            raise AuditLogIntegrityError(f"Cannot read audit log: {exc}") from exc

        if was_verified and (
            count != trusted_count or previous_hash != trusted_hash
        ):
            raise AuditLogIntegrityError(
                "Audit log no longer matches the previously verified session checkpoint"
            )

        self._last_hash = previous_hash
        self._event_count = count
        self._signature = self._file_signature()
        self._verified = True

    def append(self, event: str, tool: str, success: Optional[bool] = None) -> str:
        """Append a minimal event; arguments and command/result text are not stored."""
        if not isinstance(event, str) or not event.strip():
            raise ValueError("event must be a non-empty string")
        if not isinstance(tool, str) or not tool.strip():
            raise ValueError("tool must be a non-empty string")
        if success is not None and not isinstance(success, bool):
            raise ValueError("success must be bool or None")

        with self._lock:
            self._refresh_integrity()
            payload = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event.strip(),
                "tool": tool.strip(),
                "success": success,
                "prev_hash": self._last_hash,
            }
            digest = self._digest(payload)
            record = {**payload, "hash": digest}
            serialized = self._canonical_json(record)

            try:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                    stream.write(serialized + "\n")
                    stream.flush()
                    os.fsync(stream.fileno())
            except OSError as exc:
                raise AuditLogIntegrityError(f"Cannot append to audit log: {exc}") from exc

            self._last_hash = digest
            self._event_count += 1
            self._signature = self._file_signature()
            self._verified = True
            return digest
