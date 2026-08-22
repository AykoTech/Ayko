# Tools API Reference

## Interfaccia base (`src/core/tool_base.py`)

```python
class Tool(ABC):
    def __init__(self, name: str): ...
    def validate_args(self, args: dict) -> tuple[bool, str]: ...
    def execute(self, args: dict, state: dict) -> dict: ...
```

### Struttura risposta `execute()`

```python
{
    "success": bool,
    "result": str,
    "state_updates": dict | None,
    "log": str
}
```

---

## Tool disponibili

### OpenAppTool
```python
args = {"app": "chrome"}
result = tool.execute(args, state)
```

### CloseAppTool
```python
args = {"app": "chrome"}
```

### SystemInfoTool
```python
args = {"type": "time"}      # "time", "date", "cpu", "memory", "battery"
```

### VolumeControlTool
```python
args = {"level": 80}         # 0-100
```

### WebSearchTool
```python
args = {"query": "python tutorial"}
```

### OpenUrlTool
```python
args = {"url": "youtube.com"}    # protocollo aggiunto automaticamente
```

### MemoryTool
```python
args = {"query": "recent"}   # "recent", "stats", "frequency", "clear"
```

### SuggesterTool
```python
args = {"query": "open", "limit": 3}
```

### ContextAwarenessTool
```python
args = {"question": "what's on my screen"}
```

---

## Aggiungere un tool

Vedi [ARCHITECTURE.md](../architecture/ARCHITECTURE.md) — sezione "Aggiungere un nuovo Tool".
