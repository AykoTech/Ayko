#!/usr/bin/env python3
"""
AYKO v0.0.01 - Desktop AI Coworker
GNU General Public License v3.0
Copyright (C) 2026 Edoardo Pensi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

For more info: https://www.gnu.org/licenses/gpl-3.0.html
"""

import sounddevice as sd
import threading
import json
from vosk import Model, KaldiRecognizer
from PyQt6.QtCore import QObject, pyqtSignal
from pathlib import Path
import logging

logger = logging.getLogger("AudioInput")

class AudioInputManager(QObject):
    """Real-time audio with Vosk - Emits raw command text."""
    
    command_detected = pyqtSignal(str)  # Raw user text
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    
    def __init__(self, wake_word="AYKO", sensitivity=0.5):
        super().__init__()
        self.wake_word = wake_word.lower()
        self.sensitivity = max(0.1, min(1.0, sensitivity))
        self.is_listening = False
        self.model_loaded = False
        self.recognizer = None
        self.model = None
        self._thread = None
        
        try:
            model_path = Path("model")
            if not model_path.exists():
                logger.error("Vosk model not found. Download from https://alphacephei.com/vosk/models")
                return
            
            self.model = Model(str(model_path))
            self.recognizer = KaldiRecognizer(self.model, 16000)
            self.model_loaded = True
            logger.info(f"✓ Vosk loaded. Wake-word: '{self.wake_word}'")
        except Exception as e:
            logger.error(f"Vosk init failed: {e}")
    
    def start(self):
        """Start listening for wake-word."""
        if not self.model_loaded:
            logger.error("Model not loaded")
            return
        
        if self.is_listening:
            logger.warning("Already listening, ignoring start()")
            return
        
        self.is_listening = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        logger.info("Listening started")
    
    def stop(self):
        """Stop listening."""
        self.is_listening = False
        logger.info("Listening stopped")
    
    def _listen_loop(self):
        """Main audio processing loop."""
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=4000, channels=1, dtype='int16') as stream:
                logger.info("Audio stream opened")
                
                while self.is_listening:
                    data, _ = stream.read(4000)
                    
                    if self.recognizer.AcceptWaveform(data.tobytes()):
                        result = json.loads(self.recognizer.Result())
                        text = result.get('text', '').strip()
                        
                        if text:
                            self._process_text(text)
        
        except Exception as e:
            logger.error(f"Audio loop error: {e}")
        finally:
            self.is_listening = False
    
    def _process_text(self, text):
        """Check for wake-word and emit command."""
        text_lower = text.lower().strip()
        
        if self.wake_word in text_lower:
            self.listening_started.emit()
            
            parts = text_lower.split(self.wake_word, 1)
            if len(parts) > 1:
                command = parts[1].strip()
                if command:
                    logger.info(f"Command detected: {command}")
                    self.command_detected.emit(command)
            
            self.listening_stopped.emit()
