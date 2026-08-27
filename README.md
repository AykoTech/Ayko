# 🤖 AYKO v0.0.01 - Desktop AI Coworker

> **Coworker AI vocale completamente locale - Privacy first**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

---

## ⚡ QUICK START

### Windows
```powershell
pip install -r requirements.txt
python src/main.py
```

### macOS / Linux
```bash
pip install -r requirements.txt
python src/main.py
```

---

## 🏗️ ARCHITETTURA

Audio (Vosk) → LLMEngine → CommandParser → AYKOCore → ToolExecutor → TTS


- **100% locale** — nessun dato inviato al cloud
- **Ollama** come backend LLM (modello: tinyllama di default)
- **Vosk** per il riconoscimento vocale offline
- **pyttsx3** per il text-to-speech nativo OS

Dettagli tecnici: → [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)

---

## 📁 STRUTTURA PROGETTO

```text
ayko/
├── .gitattributes
├── .gitignore
├── README.md
├── check_environment.py
├── code-quality.yml
├── docker-compose.yml
├── requirements.txt
├── setup.py
├── setup_advanced.sh
├── assets/
│   └── ayko_dashboard.html          # Dashboard HTML con bridge Qt
├── config/
│   ├── default_settings.json
│   └── settings.json
├── docs/
│   ├── api/
│   │   ├── core_api.md
│   │   └── tools_api.md
│   ├── architecture/
│   │   └── ARCHITECTURE.md
│   └── guides/
│       └── COMMANDS.md
├── src/
│   ├── __init__.py
│   ├── main.py                       # Avvio dell'applicazione
│   ├── core/
│   │   ├── __init__.py
│   │   ├── advanced_features.py
│   │   ├── advanced_hotkey.py
│   │   ├── audio_input.py            # Vosk STT e wake-word
│   │   ├── clipboard_manager.py
│   │   ├── command_memory.py
│   │   ├── command_parser.py
│   │   ├── command_suggester.py
│   │   ├── core.py                   # Orchestratore AYKOCore
│   │   ├── custom_commands.py
│   │   ├── history_search.py
│   │   ├── learning_schedule.py
│   │   ├── llm_engine.py             # Integrazione Ollama
│   │   ├── mood_analyzer.py
│   │   ├── multi_monitor.py
│   │   ├── news_briefing.py
│   │   ├── personality.py
│   │   ├── process_monitor.py
│   │   ├── screen_analyzer.py
│   │   ├── screen_capture.py
│   │   ├── smart_launcher.py
│   │   ├── time_awareness.py
│   │   ├── tool_base.py
│   │   ├── tool_registry.py
│   │   ├── tools.py
│   │   ├── tts_engine.py
│   │   ├── tutorial_mode.py
│   │   └── voice_emotion.py
│   ├── ui/
│   │   └── ayko_app.py               # Finestra Qt e bridge QWebChannel
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       ├── logger.py
│       └── system_control.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_audio.py
    ├── validate_architecture.py
    ├── integration/
    │   ├── __init__.py
    │   └── test_full_flow.py
    └── unit/
        ├── __init__.py
        └── test_command_memory.py
```

---

## ⚙️ REQUISITI

| Requisito | Minimo |
|-----------|--------|
| Python | 3.10+ |
| RAM | 8 GB |
| Disk | 15 GB |
| OS | Windows 10, macOS 11, Ubuntu 20.04 |

**Dipendenze esterne:**
- [Ollama](https://ollama.ai) — backend LLM locale
- Modello Vosk — speech-to-text offline

---

## 🛠️ TOOL DISPONIBILI

| Tool | Intent | Descrizione |
|---|---|---|
| `OpenAppTool` | `open_app` | Apre un'applicazione |
| `CloseAppTool` | `close_app` | Chiude un'applicazione |
| `SystemInfoTool` | `system_info` | Info di sistema (ora, CPU, RAM) |
| `VolumeControlTool` | `volume_control` | Controlla il volume |
| `WebSearchTool` | `web_search` | Ricerca web |
| `OpenUrlTool` | `open_url` | Apre un URL |
| `MemoryTool` | `memory` | Storico comandi |
| `SuggesterTool` | `suggest` | Suggerimenti comandi |
| `ContextAwarenessTool` | `context_awareness` | Analisi schermo |

---

## 📚 DOCUMENTAZIONE

| Documento | Contenuto |
|-----------|-----------|
| [ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) | Pipeline tecnica completa |
| [COMMANDS.md](docs/guides/COMMANDS.md) | Lista comandi disponibili |
| [core_api.md](docs/api/core_api.md) | API di AYKOCore |
| [tools_api.md](docs/api/tools_api.md) | API dei tool |

---

## 📄 LICENZA

GNU General Public License v3.0 — [LICENSE](LICENSE)

**Creator:** Edoardo Pensi
