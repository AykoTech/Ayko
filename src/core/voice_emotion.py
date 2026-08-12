#!/usr/bin/env python3
"""Voice Emotion - Ultimate version with all fixes."""

import logging
import random
import re
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from functools import lru_cache

logger = logging.getLogger("VoiceEmotion")

class VoiceEmotionSynthesis:
    """Ultimate voice emotion synthesis."""
    
    def __init__(self):
        self._responses = None
        self._compiled_patterns = {}
        self._emotion_cache = {}
        self._cache_lock_simple = {}
        
        self.emotion_voice_map: Dict[str, Dict] = {
            "happy": {"rate": 0.9, "pitch": 1.1, "volume": 1.0, "emphasis": True},
            "sad": {"rate": 0.8, "pitch": 0.9, "volume": 0.8, "emphasis": False},
            "angry": {"rate": 1.3, "pitch": 1.2, "volume": 1.1, "emphasis": True},
            "surprised": {"rate": 1.1, "pitch": 1.3, "volume": 1.0, "emphasis": True},
            "nervous": {"rate": 1.2, "pitch": 1.1, "volume": 0.9, "emphasis": False},
            "confident": {"rate": 0.95, "pitch": 0.95, "volume": 1.0, "emphasis": True},
            "apologetic": {"rate": 0.85, "pitch": 0.9, "volume": 0.85, "emphasis": False},
        }
        
        self._validate_emotion_map()
        self._compile_patterns()
        logger.info("✓ VoiceEmotionSynthesis initialized")
    
    def _validate_emotion_map(self) -> None:
        """Validate emotion map."""
        
        required_keys = {"rate", "pitch", "volume", "emphasis"}
        
        for emotion, params in self.emotion_voice_map.items():
            if not isinstance(emotion, str):
                logger.error(f"Invalid emotion key type: {type(emotion)}")
                continue
            
            if not isinstance(params, dict):
                logger.error(f"Invalid params type for {emotion}")
                continue
            
            missing = required_keys - set(params.keys())
            if missing:
                logger.warning(f"Missing keys in {emotion}: {missing}")
                for key in missing:
                    params[key] = self._get_default_param(key)
            
            if not isinstance(params.get("rate"), (int, float)):
                params["rate"] = 1.0
            if not isinstance(params.get("pitch"), (int, float)):
                params["pitch"] = 1.0
            if not isinstance(params.get("volume"), (int, float)):
                params["volume"] = 1.0
            if not isinstance(params.get("emphasis"), bool):
                params["emphasis"] = False
            
            params["rate"] = max(0.5, min(2.0, float(params["rate"])))
            params["pitch"] = max(0.5, min(2.0, float(params["pitch"])))
            params["volume"] = max(0.0, min(1.0, float(params["volume"])))
    
    def _get_default_param(self, key: str) -> any:
        """Get default param value."""
        defaults = {
            "rate": 1.0,
            "pitch": 1.0,
            "volume": 1.0,
            "emphasis": False,
        }
        return defaults.get(key, None)
    
    def _compile_patterns(self) -> None:
        """Pre-compile regex patterns."""
        
        patterns = {
            "error": r"(error|fail|problem|issue)",
            "success": r"(success|great|excellent|perfect)",
            "warning": r"(warning|careful|attention)",
            "question": r"(\?|what|why|how|when|where)",
            "apology": r"(sorry|apologize|regret)",
        }
        
        for key, pattern in patterns.items():
            try:
                self._compiled_patterns[key] = re.compile(pattern, re.IGNORECASE)
            except re.error as e:
                logger.error(f"Regex compile error for {key}: {e}")
    
    @property
    def responses(self) -> Dict[str, List[str]]:
        """Lazy load responses."""
        if self._responses is None:
            self._responses = self._load_responses()
        return self._responses
    
    def _load_responses(self) -> Dict[str, List[str]]:
        """Load responses."""
        return {
            "apology": [
                "I sincerely apologize",
                "My deepest apologies, sir",
                "I regret to inform you",
                "I'm terribly sorry about that",
            ],
        }
    
    def get_emotion_voice_params(self, emotion: str) -> Dict:
        """Get params safely."""
        
        if emotion is None or not isinstance(emotion, str):
            logger.warning(f"Invalid emotion type: {type(emotion)}")
            return self.emotion_voice_map.get("confident", self._get_safe_default())
        
        emotion_lower = emotion.lower().strip()
        
        if not emotion_lower:
            return self.emotion_voice_map.get("confident", self._get_safe_default())
        
        params = self.emotion_voice_map.get(emotion_lower)
        
        if params is None:
            logger.warning(f"Unknown emotion: {emotion_lower}")
            return self.emotion_voice_map.get("confident", self._get_safe_default())
        
        return dict(params)
    
    def _get_safe_default(self) -> Dict:
        """Get safe default."""
        return {
            "rate": 1.0,
            "pitch": 1.0,
            "volume": 1.0,
            "emphasis": False,
        }
    
    def get_emotion_from_context(self, context: str) -> str:
        """Detect emotion safely."""
        
        if context is None or not isinstance(context, str):
            return "confident"
        
        context_lower = context.lower()
        
        for emotion_key, compiled_pattern in self._compiled_patterns.items():
            if compiled_pattern.search(context_lower):
                emotion_map = {
                    "error": "concerned",
                    "success": "happy",
                    "warning": "nervous",
                    "question": "curious",
                    "apology": "apologetic",
                }
                return emotion_map.get(emotion_key, "confident")
        
        return "confident"
    
    def synthesize_emotional_speech(self, text: str, emotion: str = "confident") -> Dict:
        """Synthesize with emotion."""
        
        if text is None or not isinstance(text, str):
            return {"success": False, "error": "Invalid text"}
        
        if len(text) > 10000:
            logger.warning("Text too long")
            return {"success": False, "error": "Text too long"}
        
        params = self.get_emotion_voice_params(emotion)
        
        return {
            "text": text,
            "emotion": emotion,
            "voice_params": params,
            "ready": True,
        }
