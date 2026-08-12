#!/usr/bin/env python3
"""Integration tests for full JARVIS flow."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def test_full_command_execution(mock_core, mock_command_memory):
    """Test full command execution flow."""
    # Execute command
    result = mock_core.execute_command("test command")
    
    assert result["success"] == True
    assert result["timestamp"] is not None

def test_command_memory_integration(mock_core, mock_command_memory):
    """Test command memory integration."""
    # Add command
    mock_command_memory.add_command("open chrome", "open_app", True)
    
    # Verify
    recent = mock_command_memory.get_recent()
    assert len(recent) > 0
    assert "open" in recent[0]["text"].lower()
