#!/usr/bin/env python3
"""
AYKO v0.0.01 - Desktop AI Coworker
GNU General Public License v3.0
"""

import sys
import logging

from utils.logger import AYKOLogger
_ayko_logger = AYKOLogger()
logger = logging.getLogger("AYKO_MAIN")

try:
    from PyQt6.QtWidgets import QApplication
    from core.audio_input import AudioInputManager
    from core.llm_engine import LLMEngine
    from core.tts_engine import TTSEngine
    from core.core import AYKOCore
    from utils.config import Config
    from ui.ayko_app import AYKOApp
except ImportError as e:
    print(f"ERROR: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def build_core(config: Config) -> AYKOCore:
    """Composition root: costruisce le dipendenze concrete e le inietta
    in AYKOCore. Core stesso non sa COME si costruisce un LLM/TTS/Audio,
    riceve solo istanze già pronte."""

    try:
        llm = LLMEngine(
            model=config.get_nested("ai", "model", default="tinyllama"),
            host=config.get_nested("ai", "host", default="http://localhost:11434"),
        )
    except Exception as e:
        logger.warning(f"LLM unavailable: {e}")
        llm = None

    try:
        rate = int(150 * config.get_nested("voice", "rate", default=1.0))
        volume = config.get_nested("voice", "volume", default=0.9)
        tts = TTSEngine(rate=rate, volume=volume)
    except Exception as e:
        logger.warning(f"TTS unavailable: {e}")
        tts = None

    audio = None
    try:
        candidate = AudioInputManager(wake_word="AYKO")
        if candidate.model_loaded:
            audio = candidate
        else:
            logger.warning("Audio unavailable: modello Vosk non trovato in ./model")
    except Exception as e:
        logger.warning(f"Audio unavailable: {e}")

    return AYKOCore(llm=llm, tts=tts, audio=audio)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AYKO")

    config = Config()
    core = build_core(config)

    window = AYKOApp(core)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
