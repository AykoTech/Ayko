#!/usr/bin/env python3
"""Logging Configuration."""

import logging
import sys
from pathlib import Path
from typing import Optional

class AYKOLogger:
    """AYKO logging system."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.log_dir = Path.home() / ".ayko" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._setup_root_logger()
    
    def _setup_root_logger(self):
        """Setup root logger."""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(
            self.log_dir / "ayko.log"
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get logger instance."""
        return logging.getLogger(name)


def setup_logger(name: str) -> logging.Logger:
    """Setup and return a named logger."""
    AYKOLogger()  # ensure root logger configured
    return logging.getLogger(name)
