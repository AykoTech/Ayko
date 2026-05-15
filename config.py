import json
from pathlib import Path

class Config:
    def __init__(self):
        self.path = Path("config/settings.json")
        self.defaults = {
            "wake_word": "JARVIS",
            "llm_model": "tinyllama",
            "ollama_host": "http://localhost:11434",
            "mic_sensitivity": 0.5
        }
        self.data = self.defaults.copy()
    
    def load(self):
        if self.path.exists():
            with open(self.path) as f:
                self.data.update(json.load(f))
    
    def save(self):
        self.path.parent.mkdir(exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value):
        self.data[key] = value
        self.save()
