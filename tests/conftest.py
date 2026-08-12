"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def temp_config(tmp_path):
    """Fixture for temporary config."""
    return tmp_path / "config.json"

@pytest.fixture
def mock_core():
    """Fixture for mock JARVIS core."""
    from core.core import JARVISCore
    return JARVISCore()

@pytest.fixture
def mock_command_memory(tmp_path):
    """Fixture for command memory."""
    from core.command_memory import CommandMemory
    return CommandMemory(config_path=tmp_path / "history.json")
