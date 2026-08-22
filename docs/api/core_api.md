# AYKOCore API Reference

## AYKOCore (`src/core/core.py`)

### Costruttore
```python
AYKOCore(llm=None, tts=None, audio=None, parent=None)
```

| Parametro | Tipo | Descrizione |
|---|---|---|
| `llm` | `LLMEngine \| None` | Motore LLM (Ollama) |
| `tts` | `TTSEngine \| None` | Motore TTS |
| `audio` | `AudioInputManager \| None` | Gestore microfono |

### Segnali Qt

| Segnale | Tipo | Quando |
|---|---|---|
| `command_received` | `str` | Testo grezzo riconosciuto |
| `command_processing` | `str` | Comando in elaborazione |
| `command_completed` | `dict` | Risultato completo |
| `speaking` | `str` | Testo che viene pronunciato |
| `error_occurred` | `str` | Errore durante elaborazione |

### Metodi

#### `execute_command(text: str) → dict`
Esegue un comando testuale. Sincrono.

```python
result = core.execute_command("what time is it")
# → {"success": True, "result": "14:32:00", "intent": "system_info",
#    "tool": "system_info", "timestamp": "...", "timeline": [...]}
```

#### `process_text_command(text: str)`
Esegue un comando testuale in modo asincrono (su thread dedicato). Utile per input da UI o test da terminale.

#### `start_listening()`
Avvia il microfono (se `AudioInputManager` è stato iniettato).

#### `stop_listening()`
Ferma il microfono.

### Struttura risultato `execute_command`

```python
{
    "success": bool,          # True se il tool ha eseguito correttamente
    "result": str,            # Testo del risultato (pronunciato da TTS)
    "intent": str,            # Intent rilevato dall'LLM
    "tool": str,              # Tool eseguito
    "timestamp": str,         # ISO 8601
    "timeline": list[str],    # Log step-by-step dell'esecuzione
    "state_updates": dict,    # Aggiornamenti di stato dal tool (opzionale)
    "error": str,             # Solo se success=False
}
```

---

## LLMEngine (`src/core/llm_engine.py`)

### `interpret(text: str) → tuple[str, dict]`
```python
intent, args = llm.interpret("open youtube")
# → ("open_app", {"app": "youtube"})
```

---

## CommandParser (`src/core/command_parser.py`)

### `parse(intent: str, args: dict) → tuple[str, dict]`
```python
tool_name, args = parser.parse("open_app", {"app": "youtube"})
# → ("open_app", {"app": "youtube"})
```

### `register_intent(intent: str, tool_name: str)`
Aggiunge una nuova mappatura intent→tool a runtime.
```python
parser.register_intent("my_intent", "my_tool")
```
