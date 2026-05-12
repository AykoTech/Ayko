# JARVIS - Developer Guide

## Architettura

```
User Voice Input
    ↓
Audio Input Manager (Vosk)
    ↓
Command Parser (Intent Recognition)
    ↓
LLM Engine (Ollama - per comandi complessi)
    ↓
System Controller (Esecuzione)
    ↓
TTS Engine (pyttsx3 - Feedback vocale)
    ↓
UI Update (PyQt6)
```

## Come Estendere

### 1. Aggiungere Nuovo Comando

**File:** `src/core/command_parser.py`

```python
# Aggiungi pattern regex
self.command_map = {
    r"apri\s+(\w+)": ("open_app", "app"),
    r"crea reminder (.+)": ("create_reminder", "text"),  # NUOVO
}
```

**File:** `src/utils/system_control.py`

```python
def execute(self, intent, params):
    if intent == "create_reminder":
        return self._create_reminder(params.get("text"))
    # ...

def _create_reminder(self, text):
    # Implementa logica
    return {"status": "created", "reminder": text}
```

### 2. Aggiungere Nuovo Modello LLM

**File:** `src/core/llm_engine.py`

```python
class LLMEngine:
    MODELS = ["tinyllama", "mistral", "neural-chat", "orca-mini"]
    
    def __init__(self, model="tinyllama", ...):
        if model not in self.MODELS:
            raise ValueError(f"Model deve essere in {self.MODELS}")
```

**Scarica il modello:**
```bash
ollama pull orca-mini
```

### 3. Customizzare Sfera 3D

**File:** `assets/sphere.html`

Modifica le costanti:

```javascript
// Colore sfera
const mat = new THREE.MeshPhongMaterial({
    color: 0xff0000,  // Rosso
    emissive: 0xaa0000
});

// Velocità rotazione
sphere.rotation.y += 0.003;  // Più veloce

// Particelle
for (let i = 0; i < 500; i++) {  // Più particelle
    positions.push(...);
}

// Aggiungi animazione custom
window.jarvisAPI.pulse = function(intensity) {
    sphere.scale.set(1 + intensity, 1 + intensity, 1 + intensity);
};
```

### 4. Aggiungere TTS Multilingual

**File:** `src/core/tts_engine.py`

```python
class TTSEngine:
    def __init__(self, language="it", ...):
        self.engine.setProperty('voice', self._get_voice(language))
    
    def _get_voice(self, lang):
        voices = self.engine.getProperty('voices')
        for v in voices:
            if lang in v.languages:
                return v.id
```

### 5. Gestione Impostazioni Avanzate

Ogni modulo legge da `config/settings.json`:

```python
# In qualsiasi modulo
from utils.config import Config
cfg = Config()
cfg.load()

wake_word = cfg.get("wake_word", "JARVIS")
model = cfg.get("llm_model", "tinyllama")

# Modifica
cfg.set("volume", 0.8)  # Salva automaticamente
```

## Performance Tips

- **Modelli leggeri:** TinyLlama 1.1B perfetto per i3
- **Quantizzazione:** Usa Q4 per ridurre RAM 70%
- **Caching comandi:** Salva risultati frequenti
- **Lazy loading:** Carica modelli solo se necessario

## Testing

```bash
# Audio test
python src/test_audio.py

# Verifica LLM
ollama list

# Run con debug
python -u src/main.py 2>&1 | tee debug.log
```

## Compilare per Release

```bash
# Freeze dependencies esatte
pip freeze > requirements-lock.txt

# Build wheel
python setup.py bdist_wheel

# Distribuzione
# → dist/jarvis_ai-0.0.01-py3-none-any.whl
```

## Troubleshooting Dev

| Problema | Soluzione |
|----------|-----------|
| Import error | Verifica `__init__.py` in cartelle |
| Ollama timeout | Aumenta timeout in `llm_engine.py` |
| Audio latency | Riduci buffer size in `audio_input.py` |
| Sfera lag | Riduci particles in `sphere.html` |
| Memory leak | Usa `del` oggetti grandi, test con `psutil` |

---

**Nota:** Ogni versione deve incrementare `version` in `setup.py` e questo file.
