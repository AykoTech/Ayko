#!/usr/bin/env python3
"""TTS Engine - Text-to-Speech with mood-based voice modulation."""

import logging
from typing import Optional

logger = logging.getLogger("TTSEngine")


class TTSEngine:
    def __init__(self, rate: int = 150, volume: float = 0.7):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            self._available = True
            logger.info("TTS Engine initialized")
        except Exception as e:
            logger.warning(f"TTS unavailable: {e}")
            self._available = False

    def speak(self, text: str, mood: Optional[dict] = None, wait: bool = True):
        if not text or not text.strip() or not self._available:
            return
        mood = mood or {"rate": 1.0, "pitch": 1.0}
        adjusted_rate = int(150 * mood.get("rate", 1.0))
        try:
            self.engine.setProperty('rate', adjusted_rate)
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS speak error: {e}")

    def stop(self):
        if self._available:
            try:
                self.engine.stop()
            except Exception:
                pass
