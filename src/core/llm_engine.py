"""LLM Engine - SINGLE responsibility: generate JSON intent + args."""

import requests
import json
import logging
from typing import Tuple, Dict, Any

logger = logging.getLogger("LLM")

class LLMEngine:
    """Generate intent + args from user text. ONLY interpretation."""
    
    def __init__(self, model: str = "tinyllama", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.url = f"{host}/api/generate"
        self.is_ready = False
        self.timeout = 10
        
        self._check_health()
    
    def _check_health(self):
        """Verify Ollama is running."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            if response.status_code == 200:
                self.is_ready = True
                logger.info(f"✓ Ollama OK. Model: {self.model}")
        except Exception as e:
            logger.error(f"Ollama error: {e}")
    
    def interpret(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """Interpret user text → intent + args.
        
        Args:
            text: User input
        
        Returns:
            (intent: str, args: dict)
        
        NOTE: Does NOT select tool. Does NOT execute anything.
        Chiamata di rete bloccante: va sempre invocata da un thread
        dedicato, mai dal thread audio/UI.
        """
        
        if not self.is_ready:
            logger.error("LLM not ready")
            return ("unknown", {})
        
        system_prompt = """You are a JSON generator.
Extract the user's intent and parameters ONLY.

Return ONLY valid JSON:
{
  "intent": "action_name",
  "args": {"key": "value"}
}

INTENTS: open_app, close_app, system_info, volume_control, web_search, open_url, memory, suggest, context_awareness

Examples:
"open youtube" → {"intent": "open_app", "args": {"app": "youtube"}}
"what time is it" → {"intent": "system_info", "args": {"type": "time"}}
"search python" → {"intent": "web_search", "args": {"query": "python"}}
"what did i do earlier" → {"intent": "memory", "args": {"query": "recent"}}
"what can I say" → {"intent": "suggest", "args": {"query": "help"}}
"what's on my screen" → {"intent": "context_awareness", "args": {"question": "what's on my screen"}}

NO explanations. JSON ONLY.
"""
        
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\nUser: {text}",
                    "stream": False,
                    "options": {"temperature": 0.1},
                },
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                logger.error(f"LLM error: {response.status_code}")
                return ("unknown", {})
            
            result_text = response.json().get("response", "")
            
            # Extract JSON
            start = result_text.find("{")
            end = result_text.rfind("}") + 1
            
            if start == -1 or end == 0:
                logger.warning(f"No JSON found in: {result_text[:50]}")
                return ("unknown", {})
            
            json_str = result_text[start:end]
            parsed = json.loads(json_str)
            
            intent = parsed.get("intent", "unknown")
            args = parsed.get("args", {})
            
            logger.info(f"Interpreted: {intent} {args}")
            return (intent, args)
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return ("unknown", {})
        except Exception as e:
            logger.error(f"Interpretation error: {e}")
            return ("unknown", {})
