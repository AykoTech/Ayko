#!/usr/bin/env python3
"""
Mood Analyzer - Detect emotional context from user input.
GNU General Public License v3.0

STRICT RULE: Analyzes text ONLY. Returns mood type.
Does NOT modify responses. Does NOT execute anything.
TTS engine uses this to adjust voice parameters.
"""

import logging

logger = logging.getLogger("MoodAnalyzer")

class MoodAnalyzer:
    """Single responsibility: Detect mood from text input."""
    
    MOODS = {
        "urgent": {
            "keywords": ["help", "crash", "error", "asap", "emergency", "immediately", "now", "urgent", "!"],
            "rate": 1.3,  # 30% faster
            "pitch": 1.15  # Slightly higher
        },
        "happy": {
            "keywords": ["thanks", "great", "awesome", "excellent", "love", "happy", "perfect", "yes", ":)"],
            "rate": 0.9,  # 10% slower, warm
            "pitch": 0.95
        },
        "sad": {
            "keywords": ["sorry", "sad", "broken", "failed", "lost", "delete", "wrong", ":("],
            "rate": 0.85,
            "pitch": 0.9
        },
        "curious": {
            "keywords": ["what", "how", "why", "?", "can you", "could you", "would you"],
            "rate": 1.0,
            "pitch": 1.05
        }
    }
    
    def detect(self, text: str) -> dict:
        """Analyze input text, return mood parameters.
        
        Returns: {mood, rate_modifier, pitch_modifier, confidence}
        """
        if not text:
            return self._neutral()
        
        text_lower = text.lower()
        best_mood = None
        best_score = 0
        
        # Find mood with most keyword matches
        for mood_name, config in self.MOODS.items():
            score = sum(1 for kw in config["keywords"] if kw in text_lower)
            
            if score > best_score:
                best_score = score
                best_mood = mood_name
        
        if best_mood and best_score > 0:
            config = self.MOODS[best_mood]
            confidence = min(0.95, best_score * 0.3)
            
            logger.debug(f"Mood: {best_mood} (score: {best_score})")
            
            return {
                "mood": best_mood,
                "rate": config["rate"],
                "pitch": config["pitch"],
                "confidence": confidence
            }
        
        return self._neutral()
    
    def _neutral(self) -> dict:
        """Default neutral mood."""
        return {
            "mood": "neutral",
            "rate": 1.0,
            "pitch": 1.0,
            "confidence": 0.5
        }
