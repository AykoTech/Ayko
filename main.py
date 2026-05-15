#!/usr/bin/env python3
"""
JARVIS v0.0.01 - Desktop AI Assistant
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

import sys
from pathlib import Path

# Logging setup
import logging
from utils.logger import setup_logger
logger = setup_logger("JARVIS_MAIN")

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow
    
    from core.audio_input import AudioInputManager
    from core.llm_engine import LLMEngine
    from core.tts_engine import TTSEngine
    from core.core import JARVISCore
    from utils.config import Config
    from ui.main_window import MainWindow

except ImportError as e:
    print(f"ERROR: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


class JARVISApplication(QMainWindow):
    """Main JARVIS Application with strict architecture."""
    
    def __init__(self):
        super().__init__()
        
        logger.info("="*70)
        logger.info("JARVIS v0.0.01 - Initializing (STRICT ARCHITECTURE)")
        logger.info("="*70)
        
        self.config = Config()
        self.config.load()
        
        try:
            # Initialize components
            logger.info("[1/4] Audio Manager...")
            self.audio_manager = AudioInputManager(
                wake_word=self.config.get("wake_word", "JARVIS"),
                sensitivity=self.config.get("mic_sensitivity", 0.5)
            )
            
            logger.info("[2/4] LLM Engine...")
            self.llm = LLMEngine(
                model=self.config.get("llm_model", "tinyllama"),
                host=self.config.get("ollama_host", "http://localhost:11434")
            )
            
            logger.info("[3/4] TTS Engine...")
            self.tts = TTSEngine(
                rate=self.config.get("tts_rate", 150),
                volume=self.config.get("tts_volume", 0.7)
            )
            
            logger.info("[4/4] Core Orchestrator...")
            self.core = JARVISCore(self.llm)
            
            # UI
            self.ui = MainWindow(self)
            self.setCentralWidget(self.ui)
            self.setWindowTitle("JARVIS v0.0.01")
            self.setGeometry(50, 50, 1600, 900)
            
            # Connect signals
            self.audio_manager.command_detected.connect(self.process_command)
            
            logger.info("="*70)
            logger.info("✓ JARVIS Ready")
            logger.info("="*70)
            
            self.ui.update_status("Ready", "green")
            
        except Exception as e:
            logger.critical(f"Init failed: {e}", exc_info=True)
            sys.exit(1)
    
    def process_command(self, user_text: str):
        """Process user command through strict architecture.
        
        Flow: LLM → Parser → Core → Tools
        """
        
        logger.info(f"Processing: {user_text}")
        
        # Execute through Core orchestrator
        result = self.core.execute_command(user_text)
        
        # Log timeline
        for line in result.get("timeline", []):
            logger.info(line)
        
        # Feedback
        if result["success"]:
            feedback = f"Eseguito: {result['tool']}"
            self.tts.speak(feedback, wait=False)
        else:
            error = result.get("error", "Errore sconosciuto")
            self.tts.speak(f"Errore: {error}", wait=False)
        
        # UI update
        self.ui.on_command_executed(
            user_text,
            result["intent"],
            result
        )
    
    def closeEvent(self, event):
        """Cleanup."""
        logger.info("Shutting down...")
        try:
            self.audio_manager.stop()
            self.tts.cleanup()
        except:
            pass
        logger.info("✓ Goodbye")
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = JARVISApplication()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
