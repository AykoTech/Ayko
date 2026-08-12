# 🤖 JARVIS - GUIDA INSTALLAZIONE PER PRINCIPIANTI

## PRIMA DI INIZIARE: Verifica 3 Cose

| Cosa | Come Verificare | Se Non Hai |
|------|-----------------|-----------|
| **Python 3.10+** | Apri Terminale/PowerShell, digita `python --version` | Scarica da https://www.python.org/downloads/ |
| **Ollama** | Apri Terminale, digita `ollama --version` | Scarica da https://ollama.ai/download |
| **8GB RAM** | Impostazioni PC → Informazioni di sistema | Aumenta memoria disponibile |

---

## ⭐ METODO PIÙ FACILE: Auto-Installer (5 minuti)

### 🪟 **WINDOWS**

1. **Scarica i file JARVIS**
   - Clicca bottone "Download" (avrai ZIP con tutti file)
   - Estrai in cartella (es: `C:\Users\TuoNome\Desktop\JARVIS`)

2. **Apri PowerShell in quella cartella**
   - Tasto Windows + R
   - Digita: `powershell`
   - Incolla: `cd C:\Users\TuoNome\Desktop\JARVIS`
   
3. **Esegui installer**
   - Digita: `.\install.bat`
   - Premi INVIO
   - **Aspetta** (dirà quando finisce - non chiudere!)

4. **Se ti chiede Ollama**
   - Scarica da https://ollama.ai/download
   - Apri file .exe e installa
   - Riapri PowerShell e ripeti step 3

5. **Avvia JARVIS**
   - Digita: `python run.py`
   - Aspetta caricamento
   - Clicca "Start Listening"
   - Parla!

---

### 🍎 **macOS / Linux**

1. **Scarica i file JARVIS**
   - Clicca bottone "Download" (avrai ZIP con tutti file)
   - Estrai in cartella (es: Desktop)

2. **Apri Terminale**
   - Applicazioni → Utilità → Terminale
   - Digita: `cd Desktop/JARVIS`

3. **Dai permessi allo script**
   - Digita: `chmod +x install.sh`

4. **Esegui installer**
   - Digita: `./install.sh`
   - Aspetta (dirà quando finisce)

5. **Se ti chiede Ollama**
   - Scarica da https://ollama.ai/download
   - Installa normalmente
   - Riapri Terminale e ripeti step 4

6. **Avvia JARVIS**
   - Digita: `source venv/bin/activate`
   - Digita: `python run.py`
   - Clicca "Start Listening"
   - Parla!

---

## ❌ SE QUALCOSA VA MALE

### Errore: "Python not found"
```
❌ Soluzione breve:
   1. Scarica Python da python.org
   2. Segna casella "Add Python to PATH"
   3. Riapri PowerShell/Terminale
   4. Riprova installer
```

### Errore: "Ollama not found"
```
❌ Soluzione breve:
   1. Scarica Ollama da ollama.ai/download
   2. Installa normalmente
   3. Chiudi PowerShell/Terminale completamente
   4. Riapri e ripeti install
```

### Errore: "Permission denied"
```
❌ Solo macOS/Linux:
   1. Digita: chmod +x install.sh
   2. Riprova installer
```

### Errore: "pip install failed"
```
❌ Soluzione rapida:
   1. Digita: pip install --upgrade pip
   2. Digita: pip install -r requirements.txt
   3. Se ancora errore, scrivi quale pacchetto fallisce
```

### PyAudio non installa
```
❌ Se vedi errore su "pyaudio" durante pip:
   
   Windows:
   - Ignora (non è critico)
   - JARVIS funziona comunque
   
   macOS:
   - Apri Terminale
   - Digita: brew install portaudio
   - Riprova installer
   
   Linux:
   - Digita: sudo apt install python3-pyaudio
   - Riprova installer
```

---

## 🎮 AVVIA JARVIS (Ogni Volta)

### 🪟 **Windows**

```
1. Apri PowerShell in cartella JARVIS
2. Digita: .\venv\Scripts\activate.bat
3. Digita: python run.py
4. Clicca bottone "Start Listening"
5. Parla: "JARVIS, apri youtube"
```

### 🍎 **macOS/Linux**

```
1. Apri Terminale in cartella JARVIS
2. Digita: source venv/bin/activate
3. Digita: python run.py
4. Clicca bottone "Start Listening"
5. Parla: "JARVIS, apri youtube"
```

---

## 📖 COMANDI DI PROVA

Dopo "Start Listening", prova questi:

```
"JARVIS, apri youtube"
"JARVIS, che ora è"
"JARVIS, ricerca python tutorial"
"JARVIS, volume 80"
"JARVIS, chiudi chrome"
```

Vedi **COMMANDS.md** per altri 80+ comandi.

---

## ⚡ VELOCE: Metodo Manuale (Se Auto-Installer Fallisce)

```bash
# 1. Apri Terminale/PowerShell in cartella JARVIS

# 2. Crea ambiente
python -m venv venv

# 3. Attiva
# Windows:
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# 4. Installa moduli
pip install -r requirements.txt

# 5. Scarica modello LLM (~700MB, 5-10 min)
ollama pull tinyllama

# 6. Avvia
python run.py
```

---

## 🆘 AIUTO EXTRA

| Se... | Fai questo |
|-------|-----------|
| Microfono non funziona | Impostazioni → Privacy → Microfono → Consenti |
| JARVIS non risponde | Prova comando: `python check_environment.py` |
| Sfera 3D non si vede | Installa driver GPU, oppure funziona comunque |
| Vuoi spegnere | Premi Ctrl+C nel Terminale |
| Vuoi riavviare | Stessi comandi di "Avvia JARVIS" |

---

## ✅ VERIFICHE FINALI

Se tutto installato correttamente, dovresti vedere:

```
✓ Python 3.10+ trovato
✓ Moduli Python installati
✓ Ollama disponibile
✓ Modello TinyLlama scaricato
✓ Finestra JARVIS apre
✓ Sfera 3D verde pulsa
```

Se vedi questo → **Perfetto! Pronto a usare JARVIS** 🚀

---

## 📞 Se Ancora Non Funziona

1. Leggi file: **README.md**
2. Esegui: `python check_environment.py`
3. Leggi output (dice cosa manca)
4. Installa cosa manca
5. Riprova

---

**Versione: 1.0 | Data: 2026-05-27 | Lingua: Italiano**
