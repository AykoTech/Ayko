"""LLM Engine - local Ollama provider for intent extraction."""

import json
import logging
from typing import Tuple, Dict, Any

import requests

logger = logging.getLogger("LLM")


class LLMEngine:
    """Small, defensive Ollama client used by AYKOCore."""

    def __init__(
        self,
        model: str = "tinyllama",
        host: str = "http://localhost:11434",
        timeout: int = 30,
        temperature: float = 0.1,
        max_tokens: int = 256,
    ):
        self.model = model
        self.host = host.rstrip("/")
        self.url = f"{self.host}/api/generate"
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.is_ready = False
        self.last_error = ""
        self.available_models = []
        self._check_health()

    def _check_health(self):
        """Check Ollama and verify that the configured model is installed."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=3)
            response.raise_for_status()
            data = response.json()
            self.available_models = [
                item.get("name", "") for item in data.get("models", [])
                if item.get("name")
            ]

            configured = self.model
            configured_base = configured.split(":")[0]
            installed = any(
                name == configured
                or name.split(":")[0] == configured_base
                for name in self.available_models
            )

            if not installed:
                self.last_error = (
                    f"Modello Ollama '{configured}' non installato. "
                    f"Modelli disponibili: {', '.join(self.available_models) or 'nessuno'}"
                )
                logger.error(self.last_error)
                return

            self.is_ready = True
            logger.info("Ollama OK. Model: %s", self.model)
        except requests.RequestException as exc:
            self.last_error = (
                f"Ollama non raggiungibile su {self.host}. "
                "Avvia Ollama e verifica che sia in esecuzione."
            )
            logger.error("%s: %s", self.last_error, exc)
        except (ValueError, KeyError) as exc:
            self.last_error = f"Risposta Ollama non valida: {exc}"
            logger.error(self.last_error)

    def interpret(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Interpret user text into a strict intent + args JSON object."""
        if not self.is_ready:
            raise RuntimeError(self.last_error or "Ollama non pronto")

        system_prompt = """You are a JSON generator.
Extract the user's intent and parameters ONLY.

Return ONLY valid JSON:
{"intent":"action_name","args":{"key":"value"}}

INTENTS: open_app, close_app, system_info, volume_control, web_search, open_url, memory, suggest, context_awareness

Examples:
"open youtube" -> {"intent":"open_app","args":{"app":"youtube"}}
"what time is it" -> {"intent":"system_info","args":{"type":"time"}}
"search python" -> {"intent":"web_search","args":{"query":"python"}}
"what did i do earlier" -> {"intent":"memory","args":{"query":"recent"}}
"what can i say" -> {"intent":"suggest","args":{"query":"help"}}
"what's on my screen" -> {"intent":"context_awareness","args":{"question":"what's on my screen"}}

If no supported intent matches, return {"intent":"unknown","args":{}}.
"""

        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "system": system_prompt,
                    "prompt": text,
                    "stream": False,
                    "format": "json",
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens,
                    },
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            result_text = response.json().get("response", "").strip()
            if not result_text:
                raise RuntimeError("Ollama ha restituito una risposta vuota")

            parsed = json.loads(result_text)
            intent = parsed.get("intent", "unknown")
            args = parsed.get("args", {})

            if not isinstance(intent, str) or not isinstance(args, dict):
                raise ValueError("JSON Ollama non conforme allo schema intent/args")

            logger.info("Interpreted: %s %s", intent, args)
            self.last_error = ""
            return intent, args

        except requests.RequestException as exc:
            self.last_error = f"Errore Ollama durante la generazione: {exc}"
            logger.error(self.last_error)
            raise RuntimeError(self.last_error) from exc
        except (json.JSONDecodeError, ValueError) as exc:
            self.last_error = f"Risposta JSON Ollama non valida: {exc}"
            logger.error(self.last_error)
            raise RuntimeError(self.last_error) from exc
