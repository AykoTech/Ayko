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
├── src/
│ ├── core/
│ │ ├── core.py # Orchestratore principale
│ │ ├── audio_input.py # Vosk STT + wake-word
│ │ ├── llm_engine.py # Ollama LLM
│ │ ├── tts_engine.py # Text-to-speech
│ │ ├── command_parser.py # Intent → tool routing
│ │ ├── tool_base.py # Classe base Tool
│ │ ├── tool_registry.py # Registry + ToolExecutor
│ │ ├── tools.py # Implementazioni tool
│ │ └── [moduli orfani] # Feature future (skeleton)
│ ├── ui/
│ │ └── [in arrivo] # UI HTML + bridge PyQt6
│ └── utils/
│ ├── config.py # Config manager
│ └── logger.py # Logging setup
├── config/
│ ├── settings.json # Impostazioni utente
│ └── default_settings.json # Template default
├── docs/
│ ├── architecture/ARCHITECTURE.md
│ ├── guides/COMMANDS.md
│ ├── api/
│ │ ├── core_api.md
│ │ └── tools_api.md
│ ├── CHANGELOG.md
│ └── CONTRIBUTORS.md
├── tests/
├── requirements.txt
└── .env.example
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
| [CHANGELOG.md](docs/CHANGELOG.md) | Storia versioni |

---

## 📄 LICENZA

GNU General Public License v3.0 — [LICENSE](LICENSE)

**Creator:** Edoardo Pensi
