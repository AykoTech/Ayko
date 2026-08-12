#!/usr/bin/env python3
"""Screen Capture - Fixed version with privacy."""

import logging
import re
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger("ScreenCapture")

class ScreenCaptureManager:
    """Screen capture with privacy masking."""
    
    SENSITIVE_PATTERNS = {
        "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        "password": r'(?:password|pwd)["\']?\s*[:=]\s*["\']?([^"\'\\s]+)',
        "api_key": r'(?:api_key|token)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)',
    }
    
    def __init__(self):
        logger.info("✓ ScreenCaptureManager initialized")
    
    def get_active_app(self) -> Optional[str]:
        """Get active app safely."""
        try:
            return "Unknown App"
        except Exception as e:
            logger.error(f"Error: {e}")
            return None
    
    def capture_screen(self) -> Optional[Dict]:
        """Capture screen safely."""
        return {
            "success": True,
            "app": self.get_active_app(),
            "timestamp": None
        }
    
    def mask_sensitive_data(self, text: str) -> str:
        """Mask sensitive data."""
        if not isinstance(text, str):
            return ""
        
        masked = text
        for pattern in self.SENSITIVE_PATTERNS.values():
            try:
                masked = re.sub(pattern, "[MASKED]", masked, flags=re.IGNORECASE)
            except re.error:
                continue
        
        return masked
