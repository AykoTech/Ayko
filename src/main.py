#!/usr/bin/env python3
"""
JARVIS v0.0.01 - Desktop AI Coworker
GNU General Public License v3.0
"""

import sys
import logging
from pathlib import Path

from utils.logger import JARVISLogger
_jarvis_logger = JARVISLogger()
logger = logging.getLogger("JARVIS_MAIN")

try:
    from PyQt6.QtWidgets import QApplication
    from core.audio_input import AudioInputManager
    from core.llm_engine import LLMEngine
    from core.tts_engine import TTSEngine
    from core.core import JARVISCore
    from utils.config import Config
    from ui.jarvis_app import JARVISApp
except ImportError as e:
    print(f"ERROR: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")

    config = Config()

    try:
        llm = LLMEngine(
            model=config.get_nested("ai", "model", default="tinyllama"),
            host=config.get_nested("ai", "host", default="http://localhost:11434")
        )
    except Exception as e:
        logger.warning(f"LLM unavailable: {e}")
        llm = None

    try:
        voice_rate = int(150 * config.get_nested("voice", "rate", default=1.0))
        voice_volume = config.get_nested("voice", "volume", default=0.9)
        tts = TTSEngine(rate=voice_rate, volume=voice_volume)
    except Exception as e:
        logger.warning(f"TTS unavailable: {e}")
        tts = None

    window = JARVISApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
