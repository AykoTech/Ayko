#!/usr/bin/env python3
"""AYKO App - Finestra principale.

Carica la dashboard HTML (assets/ayko_dashboard.html) dentro una
QWebEngineView e la collega ad AYKOCore tramite QWebChannel.

Questo file NON modifica l'HTML: si limita a esporre un oggetto
`aykoBridge` che il JS della dashboard può chiamare, e a rilanciare
verso il JS i segnali Qt che AYKOCore già emette.
"""

import json
import logging
from pathlib import Path

from PyQt6.QtCore import QObject, QUrl, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

from core.core import AYKOCore

logger = logging.getLogger("AYKOApp")

DASHBOARD_PATH = Path(__file__).resolve().parent.parent.parent / "assets" / "ayko_dashboard.html"


class AykoBridge(QObject):
    """Oggetto esposto a JavaScript via QWebChannel come `aykoBridge`.

    - I metodi con @pyqtSlot sono chiamabili dal JS: aykoBridge.nomeMetodo(...)
    - I pyqtSignal sono ascoltabili dal JS: aykoBridge.nomeSegnale.connect(fn)
    - Ogni payload verso JS è una stringa JSON (JSON.parse() lato JS), per
      evitare ambiguità di marshalling tra tipi Python e JS.
    """

    commandReceived = pyqtSignal(str)    # {"text": "..."}
    commandProcessing = pyqtSignal(str)  # {"text": "..."}
    commandCompleted = pyqtSignal(str)   # risultato completo di execute_command (vedi core_api.md)
    speaking = pyqtSignal(str)           # {"text": "..."}
    errorOccurred = pyqtSignal(str)      # {"message": "..."}

    def __init__(self, core: AYKOCore, parent=None):
        super().__init__(parent)
        self._core = core

        self._core.command_received.connect(self._on_command_received)
        self._core.command_processing.connect(self._on_command_processing)
        self._core.command_completed.connect(self._on_command_completed)
        self._core.speaking.connect(self._on_speaking)
        self._core.error_occurred.connect(self._on_error_occurred)

    # ---- AYKOCore -> JS (rilancio come segnali JSON) ----

    def _on_command_received(self, text: str):
        self.commandReceived.emit(json.dumps({"text": text}))

    def _on_command_processing(self, text: str):
        self.commandProcessing.emit(json.dumps({"text": text}))

    def _on_command_completed(self, result: dict):
        self.commandCompleted.emit(json.dumps(result, default=str))

    def _on_speaking(self, text: str):
        self.speaking.emit(json.dumps({"text": text}))

    def _on_error_occurred(self, message: str):
        self.errorOccurred.emit(json.dumps({"message": message}))

    # ---- JS -> AYKOCore (slot chiamabili dalla dashboard) ----

    @pyqtSlot(str)
    def processTextCommand(self, text: str):
        """Chiamato dal JS quando l'utente invia un comando testuale."""
        self._core.process_text_command(text)

    @pyqtSlot()
    def startListening(self):
        """Chiamato dal JS quando l'utente attiva il microfono."""
        self._core.start_listening()

    @pyqtSlot()
    def stopListening(self):
        """Chiamato dal JS quando l'utente disattiva il microfono."""
        self._core.stop_listening()


class AYKOApp(QMainWindow):
    """Finestra principale: ospita la dashboard HTML e il bridge verso AYKOCore."""

    def __init__(self, core: AYKOCore, parent=None):
        super().__init__(parent)
        self._core = core

        self.setWindowTitle("AYKO - Desktop AI Coworker")
        self.resize(1280, 800)

        self._web_view = QWebEngineView()
        self.setCentralWidget(self._web_view)

        # Il canale va registrato PRIMA di caricare la pagina, cosi'
        # `qt.webChannelTransport` e' gia' pronto quando il JS della
        # dashboard lo usa.
        self._channel = QWebChannel()
        self._bridge = AykoBridge(core, parent=self)
        self._channel.registerObject("aykoBridge", self._bridge)
        self._web_view.page().setWebChannel(self._channel)

        self._load_dashboard()

        logger.info("✓ AYKOApp initialized")

    def _load_dashboard(self):
        if not DASHBOARD_PATH.exists():
            logger.error(f"Dashboard non trovata: {DASHBOARD_PATH}")
            self._web_view.setHtml(
                "<body style='background:#0a0e27;color:#e0e0e0;"
                "font-family:sans-serif;padding:40px'>"
                f"<h2>File non trovato</h2><p>{DASHBOARD_PATH}</p></body>"
            )
            return
        self._web_view.load(QUrl.fromLocalFile(str(DASHBOARD_PATH)))
        logger.info(f"✓ Dashboard caricata da {DASHBOARD_PATH}")

    def closeEvent(self, event):
        """Ferma il microfono in modo pulito alla chiusura della finestra."""
        self._core.stop_listening()
        super().closeEvent(event)
