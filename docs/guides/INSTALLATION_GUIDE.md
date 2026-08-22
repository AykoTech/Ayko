# 🤖 GUIDA INSTALLAZIONE AYKO - PER IGNORANTI DI INFORMATICA

**Leggi questa guida COMPLETAMENTE prima di iniziare.**

---

## ⚡ QUICK START (Persone che sanno usare il PC)

```bash
# Windows PowerShell
.\install.bat
python run.py

# macOS/Linux Terminal
./install.sh
source venv/bin/activate
python run.py
```

---

## 📖 GUIDA DETTAGLIATA (Per chi non sa niente)

### PREREQUISITI (Verifica PRIMA di iniziare)

#### 1️⃣ Hai scaricato TUTTI i file?
- Dovresti avere una cartella contenente ~45 file
- Se manca il file `install.bat` o `install.sh` → **DOWNLOAD INCOMPLETO**
- **Soluzione:** Torna indietro e scarica tutti i file

#### 2️⃣ Quanto spazio disco libero hai?
- **Minimo richiesto:** 15 GB
- Controlla cliccando il tasto Windows/Apple → Impostazioni → Archiviazione
- **Se hai < 15 GB:** Cancella file grandi e libera spazio PRIMA di continuare

#### 3️⃣ Hai 8GB di RAM?
- Windows: Tasto destro "Questo PC" → Proprietà → "RAM installata"
- macOS: Apple menu → "Informazioni su questo Mac" → Memoria
- Linux: Terminal → `free -h` → visualizza memoria
- **Se hai < 8GB:** AYKO NON funzionerà bene

#### 4️⃣ Quale sistema operativo hai?
- **Windows 10/11** → Usa `install.bat`
- **macOS** → Usa `install.sh`
- **Linux (Ubuntu/Debian)** → Usa `install.sh`

---

## 🪟 INSTALLAZIONE SU WINDOWS

### STEP 1: Verifica Python (2 min)

**Cos'è Python?** È un linguaggio di programmazione che AYKO usa per funzionare.

**Che fare:**

1. Premi il tasto `Windows` sulla tastiera (quello con il logo Windows)
2. Digita: `powershell`
3. Clicca su "Windows PowerShell" (l'applicazione che appare)
4. Si apre una finestra nera con scritto `C:\Users\TuoNome>`

**Nella finestra digitare:**
```
python --version
```

**Premi INVIO**

**Possibili risultati:**

✅ **BENE:** Vedi scritto `Python 3.10` oppure `Python 3.11` o `Python 3.12`
- Vai a STEP 2

❌ **MALE:** Vedi scritto `python : The term 'python' is not recognized` oppure simile
- **Significa:** Python non è installato
- **Soluzione:**
  1. Scarica Python da: https://www.python.org/downloads/
  2. Clicca il tasto giallo grande "Download Python 3.12"
  3. Apri il file scaricato (.exe)
  4. **IMPORTANTE:** Metti il segno di spunta ✓ su "Add Python to PATH"
  5. Clicca "Install Now"
  6. Aspetta che finisca
  7. Ripeti il test `python --version` sopra

---

### STEP 2: Vai nella cartella AYKO (1 min)

1. Apri Esplora File (icona cartella nella barra)
2. Naviga fino alla cartella che contiene i file AYKO
3. Premi `Shift` + tasto destro del mouse nello spazio vuoto
4. Clicca "Apri finestra PowerShell qui"
5. Dovrebbe aparire la finestra nera con qualcosa tipo: `C:\Users\TuoNome\Desktop\ayko-ai>`

---

### STEP 3: Esegui l'installazione (15-30 min)

Nella finestra PowerShell digita:
```
.\install.bat
```

**Premi INVIO**

Vedrai apparire:
- Controlli colorati con ✅ (bene) e ❌ (errore)
- Scritte tipo `[1/6]`, `[2/6]`, ecc. (è il progresso)
- Barre di download
- Messaggi in italiano

**Cosa fa il programma:**
1. Verifica Python ✅
2. Crea "ambiente isolato" (cartella venv) ✅
3. Installa moduli Python (~30 sec di attesa)
4. Scarica modello Vosk (speech-to-text) ~40 MB
5. Chiede di installare Ollama (l'IA)
6. Scarica modello TinyLlama (700 MB, 5-10 minuti)

**Durante Step 5 (Ollama):**
Se vedi:
```
⚠️  Ollama NON installato (necessario per IA)
```

Significa che Ollama non è su questo PC.

**Che fare:**
1. Clicca il link: https://ollama.ai/download
2. Clicca "Download" per Windows
3. Apri il file scaricato (.exe)
4. Segui l'installazione (clicca Next, Next, Installa)
5. Riapri la finestra PowerShell
6. Esegui di nuovo: `.\install.bat`

**Quando vedi:**
```
╔════════════════════════════════════════════════════════╗
║          ✅ INSTALLAZIONE COMPLETATA! ✅             ║
╚════════════════════════════════════════════════════════╝
```

**PERFETTO!** L'installazione è finita. Premi un tasto per chiudere.

---

### STEP 4: Avvia AYKO (1 min)

1. Nella stessa cartella, premi `Shift` + tasto destro → "Apri finestra PowerShell qui"
2. Digita:
```
.\venv\Scripts\activate.bat
```
**Premi INVIO**

Dovrebbe apparire `(venv)` all'inizio della riga. Esempio:
```
(venv) C:\Users\TuoNome\Desktop\ayko-ai>
```

3. Digita:
```
python run.py
```
**Premi INVIO**

**Cosa succede:**
- Si apre una finestra PyQt6
- Vedi una sfera 3D verde che ruota
- In basso scritto "● READY"

**FATTO!** AYKO è avviato! 🎉

---

## 🍎 INSTALLAZIONE SU macOS

### STEP 1: Verifica Python (2 min)

1. Premi `Cmd + Spazio` (comando + spacebar)
2. Digita: `Terminale`
3. Premi INVIO
4. Si apre una finestra nera

Digita:
```
python3 --version
```
**Premi INVIO**

**Risultati:**

✅ Vedi `Python 3.10` o superiore → Vai a STEP 2

❌ Vedi errore → Installa Python:
```
brew install python3
```
(Se ti chiede la password, digita la password del Mac)

---

### STEP 2: Vai nella cartella AYKO (1 min)

Nel Terminale digita:
```
cd Desktop/ayko-ai
```
(O il percorso dove hai messo la cartella)

**Premi INVIO**

---

### STEP 3: Dai permessi allo script (1 min)

Nel Terminale digita:
```
chmod +x install.sh
```
**Premi INVIO**

---

### STEP 4: Esegui installazione (15-30 min)

Nel Terminale digita:
```
./install.sh
```
**Premi INVIO**

Vedrai il progresso con emoji e colori.

**Se chiede password:** Digita la password del Mac

**Se chiede conferma su Ollama:** Digita `y` e premi INVIO

Quando vedi:
```
✅ INSTALLAZIONE COMPLETATA! ✅
```

L'installazione è finita!

---

### STEP 5: Avvia AYKO (1 min)

Nel Terminale digita:
```
source venv/bin/activate
```
**Premi INVIO**

Dovrebbe apparire `(venv)` all'inizio.

Poi digita:
```
python run.py
```
**Premi INVIO**

Si apre AYKO! 🎉

---

## 🐧 INSTALLAZIONE SU LINUX (Ubuntu/Debian)

### STEP 1: Apri Terminale

Premi `Ctrl + Alt + T`

---

### STEP 2: Vai nella cartella

```
cd Downloads/ayko-ai
```
(O dove hai messo la cartella)

**Premi INVIO**

---

### STEP 3: Dai permessi

```
chmod +x install.sh
```
**Premi INVIO**

---

### STEP 4: Esegui installazione

```
./install.sh
```
**Premi INVIO**

Se chiede password: digita la tua password Linux (non vedrai i caratteri, è normale)

Aspetta 15-30 minuti.

---

### STEP 5: Avvia AYKO

```
source venv/bin/activate
python run.py
```

Si apre AYKO! 🎉

---

## 🎤 PRIMO USO DI AYKO

**Finestra aperta con sfera verde che ruota:**

1. Clicca il pulsante **"🎤 Start Listening"** (blu)
2. La sfera diventa **blu** (significa che sta ascoltando)
3. Parla ad alta voce:
   ```
   "AYKO, apri youtube"
   ```
4. Aspetta 1-2 secondi
5. La sfera ritorna verde
6. Si apre YouTube nel browser

**FUNZIONA!** 🎉

---

## ⚠️ ERRORI COMUNI E SOLUZIONI

### Errore: "Python not found"
**Causa:** Python non installato o non in PATH
**Soluzione:** Reinstalla Python e SEGNA "Add Python to PATH" durante installazione

### Errore: "Ollama not found"
**Causa:** Ollama non installato
**Soluzione:** Scarica da https://ollama.ai/download e installa

### Errore: "ModuleNotFoundError: No module named 'vosk'"
**Causa:** Vosk non scaricato bene
**Soluzione:** Elimina cartella `model` e riesegui `install.bat/install.sh`

### Errore: "PyAudio not found" (macOS/Linux)
**Causa:** PyAudio non compila
**Soluzione:**
```bash
# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt install portaudio19-dev
pip install pyaudio
```

### Errore: "Port 11434 already in use"
**Causa:** Ollama già in esecuzione
**Soluzione:** Riavvia il PC

### AYKO non sente il microfono
**Causa:** Permessi microfono
**Soluzione:**
- Windows: Impostazioni → Privacy → Microfono → Consenti
- macOS: Impostazioni → Sicurezza → Microfono → Consenti Terminale
- Linux: Test con `arecord -l` nel Terminale

### AYKO si apre ma non fa niente quando parlo
**Causa:** Ollama non ha scaricato il modello
**Soluzione:** Nel Terminale esegui:
```bash
ollama pull tinyllama
```
Aspetta 10 minuti che finisca il download.

---

## 🔧 VERIFICA CHE TUTTO FUNZIONI

Prima di avviare AYKO, puoi testare l'ambiente:

```bash
python check_environment.py
```

Questo script ti dirà se:
- ✅ Python è corretto
- ✅ Vosk è installato
- ✅ Ollama è installato
- ✅ Modelli sono scaricati

Se tutto è ✅ → Avvia AYKO con `python run.py`

---

## 📞 SE RIMANI BLOCCATO

1. **Leggi gli errori:** Copia il messaggio di errore esatto
2. **Google it:** Cerca l'errore su Google
3. **Check GitHub Issues:** https://github.com/edoardopensi/ayko-ai/issues
4. **Run diagnostics:**
   ```bash
   python check_environment.py
   python test_system.py
   ```

---

## ✅ CHECKLIST FINALE

Prima di dire "è installato":

- [ ] Ho scaricato TUTTI i file
- [ ] Ho spazio disco (15+ GB)
- [ ] Ho RAM (8+ GB)
- [ ] Ho installato Python 3.10+
- [ ] Ho eseguito `install.bat` (Windows) o `./install.sh` (Mac/Linux)
- [ ] Ho visto il messaggio "✅ INSTALLAZIONE COMPLETATA"
- [ ] Ho eseguito `python run.py`
- [ ] Si è aperta una finestra con sfera 3D verde
- [ ] Ho cliccato "Start Listening"
- [ ] Ho parlato: "AYKO, apri youtube"
- [ ] YouTube si è aperto nel browser

**Se TUTTO è ✅** → AYKO è installato e funzionante! 🚀

---

## 🎓 PROSSIMI PASSI

1. **Usa AYKO:** Prova i comandi in `COMMANDS.md`
2. **Personalizza:** Apri `config/settings.json` e cambia il wake-word
3. **Estendi:** Leggi `DEVELOPMENT.md` per aggiungere nuovi comandi
4. **Migliora:** Fornisci feedback su GitHub

---

**Buon divertimento! 🤖**
