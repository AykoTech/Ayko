#!/usr/bin/env python3
"""Clipboard Manager - Ultimate version with security."""

import logging
import re
from typing import List, Optional, Dict
from collections import deque
from datetime import datetime

logger = logging.getLogger("Clipboard")

class ClipboardManager:
    """Ultimate clipboard manager."""
    
    SENSITIVE_PATTERNS = {
        "credit_card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "api_key": r'(?:api_key|apikey|token)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_-]+)',
        "password": r'(?:password|passwd|pwd)["\']?\s*[:=]\s*["\']?([^"\'\\s]+)',
        "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    }
    
    def __init__(self, max_history: int = 20):
        self.clipboard_history: deque = deque(maxlen=max_history)
        logger.info("✓ ClipboardManager initialized")
    
    def set_clipboard(self, content: str) -> bool:
        """Set clipboard safely."""
        
        if content is None or not isinstance(content, str):
            logger.warning("Invalid clipboard content type")
            return False
        
        if len(content) > 1000000:
            logger.warning("Clipboard content too large")
            return False
        
        try:
            self.clipboard_history.append({
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "size": len(content.encode('utf-8')),
                "is_sensitive": self._is_sensitive(content),
            })
            return True
        
        except Exception as e:
            logger.error(f"Error setting clipboard: {e}")
            return False
    
    def get_clipboard(self, masked: bool = True) -> Optional[str]:
        """Get clipboard safely."""
        
        if not self.clipboard_history:
            return None
        
        latest = self.clipboard_history[-1]
        content = latest.get("content", "")
        
        if masked:
            content = self._mask_sensitive_data(content)
        
        return content if content else None
    
    def _is_sensitive(self, content: str) -> bool:
        """Check if content is sensitive."""
        
        if not isinstance(content, str):
            return False
        
        for pattern in self.SENSITIVE_PATTERNS.values():
            try:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
            except re.error:
                continue
        
        return False
    
    def _mask_sensitive_data(self, text: str) -> str:
        """Mask sensitive data."""
        
        if not isinstance(text, str):
            return ""
        
        masked = text
        
        for data_type, pattern in self.SENSITIVE_PATTERNS.items():
            try:
                masked = re.sub(
                    pattern,
                    f"[{data_type.upper()} MASKED]",
                    masked,
                    flags=re.IGNORECASE
                )
            except re.error as e:
                logger.warning(f"Regex error: {e}")
                continue
        
        return masked
    
    def get_clipboard_history(self, limit: int = 10) -> List[Dict]:
        """Get clipboard history safely."""
        
        if limit is None or limit < 0:
            limit = 10
        
        return [
            {
                "timestamp": entry.get("timestamp"),
                "size": entry.get("size"),
                "is_sensitive": entry.get("is_sensitive", False),
                "preview": entry.get("content", "")[:50] + "..."
            }
            for entry in list(self.clipboard_history)[-limit:]
        ]
    
    def clear_history(self) -> bool:
        """Clear history safely."""
        
        try:
            self.clipboard_history.clear()
            logger.info("Clipboard history cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing: {e}")
            return False
