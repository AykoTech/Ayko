#!/usr/bin/env python3
"""JARVIS Core - Orchestrator.

Punto centrale della pipeline: riceve testo (da microfono o da input
diretto), lo interpreta via LLM, lo instrada al tool corretto, e
restituisce/pronuncia il risultato. Espone segnali Qt cosi' che
qualunque UI (widget PyQt oppure bridge JS in QWebEngineView) possa
collegarsi senza che Core sappia nulla della UI stessa.

Le dipendenze pesanti (LLM, TTS, Audio) sono iniettate dall'esterno,
mai costruite qui dentro: chi assembla l'applicazione (es. main.py)
decide come costruirle. Questo mantiene Core testabile con
JARVISCore() a zero dipendenze, senza toccare microfono/Ollama/TTS.
"""

import logging
import threading
from typing import Dict, Optional
from datetime import datetime, timezone

from PyQt6.QtCore import QObject, pyqtSignal

logger = logging.getLogger("JARVISCore")


class JARVISCore(QObject):
    """Orchestratore: Audio -> LLM -> Parser -> Tool -> TTS."""

    command_received = pyqtSignal(str)     # testo grezzo (microfono o chiamata diretta)
    command_processing = pyqtSignal(str)   # comando in elaborazione
    command_completed = pyqtSignal(dict)   # risultato completo di execute_command
    speaking = pyqtSignal(str)             # testo che sta per essere pronunciato
    error_occurred = pyqtSignal(str)

    def __init__(self, llm=None, tts=None, audio=None, parent=None):
        super().__init__(parent)
        self.llm = llm
        self.tts = tts
        self.audio = audio

        self.state = "idle"           # stato macro (idle/processing/error)
        self.context: Dict = {}       # dati accumulati dai tool, mai stringificati
        self.timeline = []

        self.execution_lock = threading.RLock()
        self._timeline_lock = threading.RLock()

        self._parser = None
        self._executor = None
        self._init_components()

        if self.audio is not None:
            self.audio.command_detected.connect(self._on_audio_command)

        logger.info("JARVISCore initialized")

    def _init_components(self):
        try:
            from .command_parser import CommandParser
            self._parser = CommandParser()
        except Exception as e:
            logger.warning(f"Parser unavailable: {e}")
        try:
            from .tool_registry import ToolExecutor
            self._executor = ToolExecutor
        except Exception as e:
            logger.warning(f"ToolExecutor unavailable: {e}")

    # ---- Controllo microfono (se un AudioInputManager è stato iniettato) ----

    def start_listening(self):
        """Avvia l'ascolto del microfono, se disponibile."""
        if self.audio is not None:
            self.audio.start()
        else:
            logger.warning("start_listening() chiamato ma nessun AudioInputManager iniettato")

    def stop_listening(self):
        """Ferma l'ascolto del microfono, se disponibile."""
        if self.audio is not None:
            self.audio.stop()

    def process_text_command(self, text: str):
        """Punto d'ingresso per input testuale diretto (bypassa il microfono).
        Utile per test da terminale o per un futuro input testo nella UI.
        Esegue il comando e lo pronuncia, come un comando vocale."""
        self._dispatch(text)

    def _on_audio_command(self, text: str):
        """Gira sul thread del microfono: passa subito il lavoro pesante
        a un thread dedicato, per non bloccare mai il loop audio."""
        self._dispatch(text)

    def _dispatch(self, text: str):
        self.command_received.emit(text)
        worker = threading.Thread(target=self._handle_command, args=(text,), daemon=True)
        worker.start()

    def _handle_command(self, text: str):
        """Gira su thread dedicato: esegue il comando e lo pronuncia."""
        try:
            self.command_processing.emit(text)
            result = self.execute_command(text)
            self.command_completed.emit(result)
            self._speak_result(result)
        except Exception as e:
            logger.error(f"Command handling error: {e}", exc_info=True)
            self.error_occurred.emit(str(e))

    def _speak_result(self, result: Dict):
        feedback = self._build_feedback(result)
        if feedback:
            self.speaking.emit(feedback)
            if self.tts is not None:
                self.tts.speak(feedback)

    @staticmethod
    def _build_feedback(result: Dict) -> str:
        """Trasforma il risultato di execute_command in una frase pronunciabile."""
        if not isinstance(result, dict):
            return ""
        if result.get("success"):
            text = result.get("result")
            return str(text) if text else "Fatto."
        return f"Non sono riuscito a completare il comando: {result.get('result', 'errore sconosciuto')}"

    # ---- Esecuzione comando ----

    def execute_command(self, text: str) -> Dict:
        """Esegue un comando testuale attraverso LLM -> Parser -> Tool.
        Chiamabile direttamente (sincrono) per test o uso da terminale."""
        if not isinstance(text, str):
            raise TypeError("Command must be string")
        text = text.strip()
        if not text:
            return {"success": False, "result": "Empty command", "error": "ValidationError",
                    "intent": "unknown", "tool": "none", "timeline": []}
        if len(text.encode('utf-8')) > 5000:
            raise ValueError("Command exceeds maximum length")

        with self.execution_lock:
            timestamp = datetime.now(timezone.utc).isoformat()
            tl = []
            self.state = "processing"
            try:
                tl.append(f"[{timestamp}] START: {text[:50]}")

                intent, args = "unknown", {}
                if self.llm and self.llm.is_ready:
                    intent, args = self.llm.interpret(text)
                    tl.append(f"Intent: {intent}")

                tool_name = "unknown"
                if self._parser and intent != "unknown":
                    tool_name, args = self._parser.parse(intent, args)
                    tl.append(f"Tool: {tool_name}")

                result = {"success": True, "result": f"Executed: {text}", "state_updates": None, "log": ""}
                if self._executor and tool_name != "unknown":
                    result = self._executor.execute(tool_name, args, {"context": self.context})
                    if result.get("state_updates"):
                        self.context.update(result["state_updates"])

                self.state = "idle" if result.get("success") else "error"
                tl.append(f"[{timestamp}] END: {'SUCCESS' if result['success'] else 'FAIL'}")
                with self._timeline_lock:
                    self.timeline.extend(tl)

                return {**result, "intent": intent, "tool": tool_name,
                        "timestamp": timestamp, "timeline": tl}

            except Exception as e:
                self.state = "error"
                tl.append(f"[{timestamp}] ERROR: {type(e).__name__}: {e}")
                logger.error(f"Execution error: {e}", exc_info=True)
                return {"success": False, "result": "Execution error", "error": type(e).__name__,
                        "intent": "unknown", "tool": "none", "timestamp": timestamp, "timeline": tl}
