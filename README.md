# JARVIS - Desktop AI Assistant

**Versione:** 0.0.01  
**Creatore:** Edoardo Pensi  
**Descrizione:** Platform di controllo desktop con AI vocal-enabled per eseguire qualsiasi comando di sistema

---

## 📋 Requisiti di Sistema

- **CPU:** Intel i3 13a gen o equivalente
- **RAM:** 8GB minimo
- **Spazio disco:** 8GB (per modelli LLM)
- **OS:** Windows 10+, macOS 11+, Linux (Ubuntu 20.04+)
- **Microfono e altoparlanti:** Necessari

---

## 🚀 Quick Setup (Automatico)

### Windows
```bash
# Scarica il progetto
git clone https://github.com/NovaAI-Games/J.A.R.V.I.S..git
cd J.A.R.V.I.S.

# Esegui installer
.\install.bat
```

### macOS/Linux
```bash
# Scarica il progetto
git clone https://github.com/NovaAI-Games/J.A.R.V.I.S..git
cd J.A.R.V.I.S.

# Rendi eseguibile
chmod +x install.sh

# Esegui installer
./install.sh
```

---

## 📖 Setup Manuale Dettagliato (Se lo script fallisce)

### Step 1: Installa Python 3.10+

**Windows:**
- Scarica da https://www.python.org/downloads/
- Durante installazione: ☑️ "Add Python to PATH"
- Verifica: `python --version`

**macOS:**
```bash
# Via Homebrew
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-dev
python3 --version
```

---

### Step 2: Scarica Progetto

```bash
git clone https://github.com/NovaAI-Games/J.A.R.V.I.S..git
cd J.A.R.V.I.S.
```

---

### Step 3: Crea Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 4: Installa Dipendenze Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Attenderà ~5-10 minuti. Non interrompere.

---

### Step 5: Installa Ollama (LLM Backend)

**Windows:**
- Scarica da https://ollama.ai/download
- Esegui installer
- Dopo: apri PowerShell e verifica:
```bash
ollama --version
```

**macOS:**
```bash
brew install ollama
ollama --version
```

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
ollama --version
```

---

### Step 6: Scarica Modelli LLM (IMPORTANTE)

Esegui nel terminale (venv attivo):

```bash
# Scarica TinyLlama (1.1B - velocissimo)
ollama pull tinyllama

# Opzionale: Mistral 7B (migliore qualità, più lento)
# ollama pull mistral
```

Questo scaricherà ~700MB (TinyLlama) o ~3.5GB (Mistral).

---

### Step 7: Dipendenze di Sistema (Platform-specific)

#### Windows (Voice)
```bash
# Niente da fare - Windows ha TTS nativo
```

#### macOS
```bash
# Niente da fare - macOS ha TTS nativo
```

#### Linux
```bash
# Installa festival TTS
sudo apt install festival espeak

# Oppure Piper TTS (migliore):
git clone https://github.com/rhasspy/piper.git
cd piper
./install.sh
```

---

### Step 8: Verifica Installazione

```bash
# Controlla Python modules
python -c "import torch, pyqt6, vosk; print('✓ Moduli OK')"

# Controlla Ollama
ollama list

# Controlla Audio
python src/test_audio.py
```

---

### Step 9: Prima Accensione

```bash
# Venv attivo!
python src/main.py
```

Apparirà finestra con sfera JARVIS 3D. Aspetta 30 secondi per caricamento completo.

---

## 🎤 Comandi Disponibili

### Sistema
- "apri [nomefile]" → Apri file dal desktop
- "chiudi [app]" → Chiudi applicazione
- "attiva screensaver" → Avvia screensaver
- "spegni" → Shutdown (con conferma)
- "riavvia" → Reboot
- "volume [0-100]" → Imposta volume
- "luminosità [0-100]" → Regola brightness

### File & Cartelle
- "apri cartella downloads" → Apri explorer/finder
- "elimina [file]" → Elimina file (con conferma)
- "copia file [nome]" → Copia negli appunti
- "cerca [nome] sul desktop" → Ricerca file

### Browser
- "apri youtube" → Avvia browser con YouTube
- "cerca [query] su google" → Google search
- "vai a [url]" → Apri URL diretto
- "scarica [link]" → Download file

### Media
- "riproduci musica" → Apri player (VLC/iTunes)
- "play [canzone]" → Riproduci su Spotify/local
- "pausa" → Pausa media
- "volume su/giù" → Regola audio

### App Launcher
- "apri vscode" / "apri spotify" / "apri discord" / "apri steam"
- Qualsiasi app nel sistema (if findable)

### Sistema Informativo
- "che ora è" → Mostra ora attuale
- "meteo" → Temperatura locale (richiede Internet)
- "uso CPU" → % CPU in tempo reale
- "memoria libera" → RAM disponibile
- "batteria" → % batteria (laptop)

### Custom & Avanzati
- "esegui [comando]" → Esegui comando shell
- "apri powershell/terminal" → Command prompt
- "crea appunto [testo]" → Salva appunto
- "leggi appunti" → Lista appunti salvati

---

## ⚙️ Impostazioni (Settings Panel)

Accedi da menu in alto a destra. Configurabili:

- **Wake Word:** Default "JARVIS" → personalizza a piacimento
- **Modello LLM:** TinyLlama (veloce) ↔ Mistral (accurato)
- **Volume Risposta:** 0-100%
- **Sensitivity Microfono:** 0-100%
- **Timeout Comando:** 1-30 secondi
- **Theme:** Dark/Light
- **Autostart al boot:** On/Off
- **Log File Location:** Path personalizzato

---

## 🔧 Troubleshooting

### "Ollama non trovato"
- Verifica: `ollama --version`
- Restart container/sistema
- Reinstalla da https://ollama.ai

### "Microfono non funziona"
- Windows: Settings > Privacy > Microphone > Allow
- macOS: System Preferences > Security > Microphone
- Linux: `pactl list | grep input`

### "Sfera 3D lagga"
- Riduci risoluzione in Settings
- Chiudi altre app (Chrome usa GPU)
- Aggiorna drivers GPU

### "Risposta molto lenta"
- Usa TinyLlama invece di Mistral
- Aumenta RAM allocata a Ollama
- Riduci altre app aperte

### "Wake-word non riconosce"
- Aumenta sensitivity in Settings
- Parla più chiaramente
- Controlla microfono da Sistema > Devices

---

## 📁 Struttura Progetto

```
jarvis-ai/
├── src/
│   ├── main.py                 # Entry point principale
│   ├── core/
│   │   ├── audio_input.py      # Vosk STT + Wake-word
│   │   ├── llm_engine.py       # Ollama integration
│   │   ├── tts_engine.py       # Text-to-Speech
│   │   └── command_parser.py   # Intent recognition
│   ├── ui/
│   │   ├── main_window.py      # PyQt6 UI principale
│   │   ├── jarvis_sphere.py    # Sfera 3D (Three.js)
│   │   └── settings_panel.py   # Settings
│   ├── utils/
│   │   ├── system_control.py   # OS commands
│   │   ├── config.py           # Gestione settings.json
│   │   └── logger.py           # Logging
│   └── test_audio.py           # Audio test script
├── assets/
│   ├── sphere.html             # THREE.js sfera 3D
│   └── icon.png
├── config/
│   └── settings.json           # Config default
├── requirements.txt            # Python dipendenze
├── install.bat                 # Installer Windows
├── install.sh                  # Installer macOS/Linux
├── README.md                   # Questo file
└── .gitignore

```

---

## 🎓 Per Sviluppatori (Estendere JARVIS)

### Aggiungere Comando Custom

Modifica `src/core/command_parser.py`:

```python
# In COMMAND_MAP dict
"play youtube": {
    "intent": "open_app",
    "app": "youtube",
    "browser": True
}

# In execute_command()
if intent == "open_app":
    open_application(command["app"])
```

### Aggiungere Nuovo Modello LLM

Modifica `src/core/llm_engine.py`:

```python
# In __init__
self.available_models = [
    "tinyllama",
    "mistral",
    "neural-chat"  # Nuovo modello
]

# Scarica: ollama pull neural-chat
```

### Customizzare Sfera 3D

Modifica `assets/sphere.html` - è Three.js puro:
- Colori: `geometry.material.color.set(0x...)`
- Animazioni: aggiungi `requestAnimationFrame()`
- Texture: carica da asset

---

## 📝 License & Credits

- **JARVIS Concept:** Marvel/Iron Man
- **Framework:** PyQt6, Ollama, Vosk, pyttsx3
- **Creator:** Edoardo Pensi v0.0.01

---

## 🐛 Bug Report & Contributi

Issues: https://github.com/NovaAI-Games/J.A.R.V.I.S./issues  
Forks welcome per miglioramenti!

---

**Ultima modifica:** 2026-05-11  
**Status:** Alpha - Feedback & Contributi apprezzati!
