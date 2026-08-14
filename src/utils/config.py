#!/usr/bin/env python3
"""Configuration Management.

Unico punto di lettura/scrittura per le impostazioni JARVIS.
Il file vive SEMPRE dentro config/ (mai in home directory), come da
regola di progetto.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()  # carica .env se presente; non fallisce se assente
except ImportError:
    pass

logger = logging.getLogger("Config")

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"
SETTINGS_PATH = CONFIG_DIR / "settings.json"
DEFAULTS_PATH = CONFIG_DIR / "default_settings.json"


class Config:
    """Configuration manager."""

    def __init__(self, config_path: Path = None):
        self.config_path = config_path or SETTINGS_PATH
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _get_defaults(self) -> Dict[str, Any]:
        """Default di fallback, letti da config/default_settings.json."""
        if DEFAULTS_PATH.exists():
            try:
                with open(DEFAULTS_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Impossibile leggere {DEFAULTS_PATH}: {e}")

        # Fallback finale se anche default_settings.json manca o è corrotto
        return {
            "version": "0.0.01",
            "voice": {"engine": "pyttsx3", "rate": 1.0, "volume": 0.9, "pitch": 1.0},
            "ai": {
                "model": "tinyllama",
                "host": "http://localhost:11434",
                "max_tokens": 256,
                "temperature": 0.7,
                "offline_mode": True,
            },
            "hotkeys": {
                "activate": "alt+j",
                "settings": "alt+j+s",
                "help": "alt+j+h",
                "clear_history": "alt+j+c",
            },
            "features": {
                "learning_enabled": True,
                "personality_enabled": True,
                "emotion_synthesis": True,
                "screen_awareness": True,
                "multi_monitor": True,
            },
            "privacy": {
                "mask_clipboard": True,
                "offline_mode": True,
                "store_commands": True,
                "max_history": 50,
            },
            "ui": {"theme": "dark", "animation_speed": 1.0, "refresh_rate": 60},
        }

    def _load_config(self):
        """Carica config/settings.json. Se manca, lo crea dai default."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                logger.info(f"Config caricata da {self.config_path}")
            else:
                self.config = self._get_defaults()
                self._save_config()
                logger.info(f"Config non trovata, creata con i default in {self.config_path}")
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Errore caricamento config: {e}")
            self.config = self._get_defaults()

    def _save_config(self):
        """Salva l'intero stato su disco."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Config salvata su {self.config_path}")
        except IOError as e:
            logger.error(f"Errore salvataggio config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Legge una sezione top-level (es. 'ai', 'voice')."""
        return self.config.get(key, default)

    def get_nested(self, *keys: str, default: Any = None) -> Any:
        """Legge un valore annidato. Es: get_nested('ai', 'model')."""
        value = self.config
        for key in keys:
            if not isinstance(value, dict) or key not in value:
                return default
            value = value[key]
        return value

    def set(self, key: str, value: Any) -> bool:
        """Sovrascrive un'intera sezione top-level e salva."""
        try:
            self.config[key] = value
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Errore impostando '{key}': {e}")
            return False

    def set_nested(self, section: str, updates: Dict[str, Any]) -> bool:
        """Aggiorna solo alcune chiavi dentro una sezione, senza cancellare le altre.

        Es: set_nested('ai', {'model': 'mistral'}) NON tocca 'ai.host'.
        Usare questo invece di 'set()' per salvataggi parziali (es. da una UI)
        per evitare di perdere sezioni come 'hotkeys' o 'privacy'.
        """
        try:
            if section not in self.config or not isinstance(self.config[section], dict):
                self.config[section] = {}
            self.config[section].update(updates)
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Errore aggiornando sezione '{section}': {e}")
            return False

    def reload(self):
        """Ricarica da disco (se il file è stato modificato esternamente)."""
        self._load_config()

    @staticmethod
    def get_env(key: str, default: Any = None) -> Any:
        """Legge una variabile d'ambiente/.env. Per credenziali future (es. API key cloud)."""
        return os.getenv(key, default)
