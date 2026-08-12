#!/usr/bin/env python3
"""Tests for CommandMemory."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.command_memory import CommandMemory

def test_add_command(mock_command_memory):
    """Test adding command."""
    assert mock_command_memory.add_command("test", "test", True)
    assert len(mock_command_memory.history) == 1

def test_command_validation(mock_command_memory):
    """Test command validation."""
    assert not mock_command_memory.add_command("", "test", True)
    assert not mock_command_memory.add_command(None, "test", True)

def test_get_recent(mock_command_memory):
    """Test getting recent commands."""
    mock_command_memory.add_command("cmd1", "intent1", True)
    mock_command_memory.add_command("cmd2", "intent2", False)
    
    recent = mock_command_memory.get_recent(1)
    assert len(recent) == 1
    assert recent[0]["text"] == "cmd2"

def test_success_rate(mock_command_memory):
    """Test success rate calculation."""
    mock_command_memory.add_command("cmd1", "test", True)
    mock_command_memory.add_command("cmd2", "test", True)
    mock_command_memory.add_command("cmd3", "test", False)
    
    rate = mock_command_memory.get_success_rate()
    assert rate == pytest.approx(2/3, rel=0.1)

def test_empty_history(mock_command_memory):
    """Test empty history."""
    assert mock_command_memory.get_success_rate() == 0.0
    assert len(mock_command_memory.get_recent()) == 0
