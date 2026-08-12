#!/usr/bin/env python3
"""Modern UI launcher for JARVIS."""

import sys
import logging
from pathlib import Path

logger = logging.getLogger("ModernUI")


def launch_modern_ui():
    """Launch JARVIS modern interface."""
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("PyQt6 not found. Run: pip install PyQt6 PyQt6-WebEngine")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    app.setApplicationVersion("0.0.01")

    try:
        from .jarvis_app import JARVISApp
        window = JARVISApp()
        window.show()
    except Exception as e:
        logger.warning(f"Full app failed ({e}), launching minimal UI")
        from .main_window import MainWindow
        window = MinimalLauncher()
        window.show()

    sys.exit(app.exec())


class MinimalLauncher:
    """Fallback minimal launcher when full app components missing."""
    def __init__(self):
        from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont

        self._win = QMainWindow()
        self._win.setWindowTitle("JARVIS v0.0.01")
        self._win.setGeometry(100, 100, 900, 600)
        self._win.setStyleSheet("background-color: #0a0e27; color: #00ff41;")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("🤖 JARVIS v0.0.01")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff41;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Desktop AI Assistant — Privacy First")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #00aa20; font-size: 13px;")
        layout.addWidget(subtitle)

        self._status = QLabel("● READY")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setStyleSheet("color: #00ff41; font-size: 16px; font-weight: bold;")
        layout.addWidget(self._status)

        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setStyleSheet(
            "background-color: #0a0e27; color: #00ff41; border: 1px solid #00ff41;"
            "font-family: Courier; font-size: 11px;"
        )
        layout.addWidget(self._log)

        btn_style = (
            "QPushButton { background-color: #1a1a2e; color: #00ff41; border: 2px solid #00ff41;"
            "border-radius: 5px; padding: 10px; font-weight: bold; }"
            "QPushButton:hover { background-color: #0f3a0f; }"
            "QPushButton:pressed { background-color: #00ff41; color: #000; }"
        )

        self._btn = QPushButton("🎤 Start Listening")
        self._btn.setStyleSheet(btn_style)
        self._btn.clicked.connect(self._toggle_listen)
        layout.addWidget(self._btn)

        self._win.setCentralWidget(central)
        self._log_entry("JARVIS initialized. Ollama + Vosk required for full functionality.")
        self._log_entry("Install: pip install -r requirements.txt")
        self._log_entry("LLM: ollama pull tinyllama")

    def _log_entry(self, text):
        from datetime import datetime
        t = datetime.now().strftime("%H:%M:%S")
        self._log.append(f"[{t}] {text}")

    def _toggle_listen(self):
        self._log_entry("Voice input requires Vosk model. See README.md for setup.")

    def show(self):
        self._win.show()
