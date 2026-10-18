# Percorso: tests/unit/test_startup_resilience.py
"""Tests for startup behavior across Windows console and model layouts."""

import io
import logging

from core.audio_input import AudioInputManager
from utils.logger import ConsoleStreamHandler


def test_console_handler_falls_back_for_cp1252_unicode_output():
    """Unicode log messages do not produce a logging traceback on CP1252 consoles."""
    stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
    handler = ConsoleStreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))

    handler.emit(logging.LogRecord("test", logging.INFO, __file__, 0, "✓ ready", (), None))
    stream.seek(0)

    assert stream.read() == "\\u2713 ready\n"


def test_audio_input_resolves_a_model_nested_under_model_root(tmp_path):
    """The bundled Vosk model is found even though it lives in a named subdirectory."""
    model = tmp_path / "model" / "vosk-model-small-it-0.22"
    (model / "am").mkdir(parents=True)
    (model / "conf").mkdir()

    assert AudioInputManager._resolve_model_path(tmp_path / "model") == model


def test_audio_input_rejects_a_directory_without_a_vosk_model(tmp_path):
    """An arbitrary directory is not treated as a usable Vosk model."""
    assert AudioInputManager._resolve_model_path(tmp_path) is None
