# AYKO v0.0.01 - Architettura Tecnica

## Pipeline

Audio (Vosk) → LLMEngine.interpret() → CommandParser.parse() → AYKOCore.execute_command() → ToolExecutor → Tool.execute() → TTSEngine


## Componenti

### AudioInputManager (`src/core/audio_input.py`)
- Cattura audio in tempo reale via `sounddevice`
- Rileva la wake-word ("AYKO") con Vosk
- Emette `command_detected(text: str)` sul thread audio
- **Non blocca mai** — passa subito il testo a `AYKOCore` via segnale Qt

### LLMEngine (`src/core/llm_engine.py`)
- Chiama Ollama (`/api/generate`) con prompt strutturato
- Ritorna `(intent: str, args: dict)` — **solo interpretazione linguistica**
- Non seleziona tool, non esegue azioni
- Chiamata bloccante: sempre invocata su thread dedicato

### CommandParser (`src/core/command_parser.py`)
- Mappa `intent` → `tool_name` via dizionario statico `INTENT_TO_TOOL`
- **Nessuna logica**, solo lookup O(1)
- Estendibile: `register_intent(intent, tool_name)`

### AYKOCore (`src/core/core.py`)
- Orchestratore centrale: coordina tutti i componenti
- Riceve testo (da microfono o input diretto)
- Gestisce stato globale (`idle/processing/error`) e contesto accumulato
- Espone segnali Qt: `command_received`, `command_completed`, `speaking`, `error_occurred`
- Le dipendenze (LLM, TTS, Audio) sono **iniettate dall'esterno** (testabilità)

### ToolExecutor + TOOL_REGISTRY (`src/core/tool_registry.py`)
- `TOOL_REGISTRY`: dizionario statico `{tool_name: Tool()}`
- `ToolExecutor.execute(tool_name, args, state)`: valida args, delega a `tool.execute()`

### Tool (`src/core/tools.py`)
- Ogni tool ha **una sola responsabilità**
- Interfaccia standard: `execute(args: dict, state: dict) → dict`
- Risultato sempre: `{success, result, state_updates, log}`

### TTSEngine (`src/core/tts_engine.py`)
- Text-to-speech via `pyttsx3`
- Modulazione rate/pitch opzionale

## Aggiungere un nuovo Tool

```python
# 1. Crea la classe in src/core/tools.py
class MyTool(Tool):
    def __init__(self):
        super().__init__("my_tool")

    def validate_args(self, args):
        return (True, "")

    def execute(self, args, state):
        return {
            "success": True,
            "result": "fatto",
            "state_updates": None,
            "log": "my_tool executed"
        }

# 2. Registra in src/core/tool_registry.py
TOOL_REGISTRY["my_tool"] = MyTool()

# 3. Mappa l'intent in src/core/command_parser.py
INTENT_TO_TOOL["my_intent"] = "my_tool"

# 4. Aggiungi l'intent al prompt LLM in src/core/llm_engine.py
# INTENTS: ..., my_intent
```

## Thread Safety

- Il thread audio **non blocca mai**: emette un segnale Qt e torna subito
- Il lavoro pesante (LLM, tool) gira su **thread dedicati** (`threading.Thread(daemon=True)`)
- `AYKOCore.execution_lock` (RLock) protegge lo stato condiviso
- I segnali Qt gestiscono la comunicazione cross-thread in sicurezza
