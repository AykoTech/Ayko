#!/usr/bin/env python3
"""
Screen Analyzer - Capture and analyze screen content.
GNU General Public License v3.0

RESPONSIBILITY: Capture screenshots, extract text, provide descriptions.
Does NOT make decisions. Does NOT execute actions.
Returns: Screen description and extracted content.
"""

import logging
import io
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("ScreenAnalyzer")

class ScreenAnalyzer:
    """Analyze screen content to provide context awareness."""
    
    def __init__(self, enable_ocr: bool = False):
        """Initialize screen analyzer.
        
        Args:
            enable_ocr: Enable OCR text extraction (requires pytesseract)
        """
        self.enable_ocr = enable_ocr
        self.last_screenshot = None
        self.last_screenshot_time = None
        self.last_extracted_text = None
        
        # Try to import PIL
        try:
            from PIL import Image, ImageGrab
            self.Image = Image
            self.ImageGrab = ImageGrab
            self.pil_available = True
            logger.info("✓ PIL available")
        except ImportError:
            self.pil_available = False
            logger.warning("⚠ PIL not available (install pillow)")
        
        # Try to import pytesseract for OCR
        if enable_ocr:
            try:
                import pytesseract
                self.pytesseract = pytesseract
                self.ocr_available = True
                logger.info("✓ OCR available")
            except ImportError:
                self.ocr_available = False
                logger.warning("⚠ OCR not available (install pytesseract)")
        else:
            self.ocr_available = False
    
    def capture_screenshot(self) -> Optional[Dict]:
        """Capture current screen.
        
        Returns:
            {screenshot: PIL Image, timestamp: datetime}
            or None if capture fails
        """
        if not self.pil_available:
            logger.warning("PIL not available")
            return None
        
        try:
            screenshot = self.ImageGrab.grab()
            self.last_screenshot = screenshot
            self.last_screenshot_time = datetime.now()
            
            logger.debug("Screenshot captured")
            
            return {
                "screenshot": screenshot,
                "timestamp": self.last_screenshot_time,
                "size": screenshot.size
            }
        except Exception as e:
            logger.error(f"Screenshot capture failed: {e}")
            return None
    
    def extract_text(self) -> Optional[str]:
        """Extract text from last screenshot using OCR.
        
        Returns:
            Extracted text or None
        """
        if not self.enable_ocr or not self.ocr_available:
            logger.debug("OCR not enabled")
            return None
        
        if not self.last_screenshot:
            logger.warning("No screenshot to extract from")
            return None
        
        try:
            text = self.pytesseract.image_to_string(self.last_screenshot)
            self.last_extracted_text = text
            
            logger.debug(f"Text extracted ({len(text)} chars)")
            
            return text
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return None
    
    def get_window_title(self) -> Optional[str]:
        """Get current active window title.
        
        Platform-specific implementation needed.
        """
        # Placeholder - would need pygetwindow or similar
        return "Unknown Application"
    
    def describe_screen(self) -> Optional[str]:
        """Generate human-readable description of current screen.
        
        Returns:
            Description string or None
        """
        if not self.last_screenshot:
            logger.warning("No screenshot available")
            return None
        
        try:
            width, height = self.last_screenshot.size
            
            # Get dominant colors (simplified)
            colors = self._get_dominant_colors()
            
            description = f"Screen size: {width}x{height}"
            
            # Add window info if available
            window = self.get_window_title()
            if window:
                description += f". Active window: {window}"
            
            # Add text if available
            if self.last_extracted_text:
                lines = len(self.last_extracted_text.split('\n'))
                description += f". Contains {lines} lines of text"
            
            logger.debug(f"Screen description: {description}")
            
            return description
        except Exception as e:
            logger.error(f"Description generation failed: {e}")
            return None
    
    def search_text_on_screen(self, query: str) -> Optional[List[str]]:
        """Search for text on screen.
        
        Returns:
            List of matching lines or None
        """
        if not self.last_extracted_text:
            logger.warning("No text extracted from screen")
            return None
        
        query_lower = query.lower()
        lines = self.last_extracted_text.split('\n')
        
        matches = [
            line for line in lines
            if query_lower in line.lower()
        ]
        
        if matches:
            logger.debug(f"Found {len(matches)} matches for '{query}'")
            return matches
        
        return None
    
    def answer_screen_question(self, question: str) -> Optional[str]:
        """Answer questions about screen content.
        
        Examples:
            "What's the title bar?"
            "What file is open?"
            "What's on the screen?"
        """
        if not self.last_screenshot:
            return "I don't have a screenshot to analyze"
        
        question_lower = question.lower()
        
        # Simple heuristic-based answers
        if "title" in question_lower or "window" in question_lower:
            window = self.get_window_title()
            return f"The active window is: {window}"
        
        elif "file" in question_lower:
            if self.last_extracted_text and "filename" in self.last_extracted_text.lower():
                return "I can see a file is open, but can't determine which one"
            return "I don't see an obvious file open"
        
        elif "what" in question_lower or "see" in question_lower or "show" in question_lower:
            return self.describe_screen()
        
        else:
            # Try searching the screen text
            if self.last_extracted_text:
                lines = self.last_extracted_text.split('\n')
                return f"I can see {len(lines)} lines of content on screen"
            
            return "I can see the screen"
    
    def _get_dominant_colors(self) -> List[tuple]:
        """Get dominant colors from screenshot (simplified).
        
        Returns:
            List of (r, g, b) tuples
        """
        if not self.last_screenshot:
            return []
        
        try:
            # Simplified: just get corner colors
            w, h = self.last_screenshot.size
            pixels = [
                self.last_screenshot.getpixel((0, 0)),  # Top-left
                self.last_screenshot.getpixel((w-1, 0)),  # Top-right
                self.last_screenshot.getpixel((0, h-1)),  # Bottom-left
                self.last_screenshot.getpixel((w-1, h-1)),  # Bottom-right
            ]
            return pixels
        except Exception as e:
            logger.debug(f"Color extraction failed: {e}")
            return []
    
    def get_screen_info(self) -> Optional[Dict]:
        """Get comprehensive screen information.
        
        Returns:
            Dictionary with screen data
        """
        if not self.last_screenshot:
            return None
        
        return {
            "size": self.last_screenshot.size,
            "timestamp": self.last_screenshot_time,
            "window": self.get_window_title(),
            "text_extracted": bool(self.last_extracted_text),
            "text_length": len(self.last_extracted_text) if self.last_extracted_text else 0,
            "description": self.describe_screen()
        }
    
    def clear_cache(self) -> None:
        """Clear cached screenshot and text."""
        self.last_screenshot = None
        self.last_extracted_text = None
        self.last_screenshot_time = None
        logger.debug("Screen cache cleared")
