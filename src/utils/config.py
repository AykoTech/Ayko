#!/usr/bin/env python3
"""Configuration Management."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger("Config")

class Config:
    """Configuration manager."""
    
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.home() / ".jarvis" / "config.json"
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Config loaded from {self.config_path}")
            else:
                self.config = self._get_defaults()
                self._save_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = self._get_defaults()
    
    def _get_defaults(self) -> Dict[str, Any]:
        """Get default config."""
        return {
            "version": "0.0.01",
            "voice": {"rate": 1.0, "volume": 0.9},
            "features": {"learning": True, "personality": True},
            "privacy": {"offline_mode": True, "store_commands": True},
        }
    
    def _save_config(self):
        """Save configuration."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Config saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set config value."""
        try:
            self.config[key] = value
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Error setting config: {e}")
            return False
