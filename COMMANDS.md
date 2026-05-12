# JARVIS - Complete Command Reference

## 📋 Comandi Disponibili (v0.0.01)

Parla al microfono dopo dire **"JARVIS"** per eseguire comandi.

---

### 🖥️ SISTEMA & CONTROLLO

| Comando | Effetto | Esempio |
|---------|---------|---------|
| apri [app] | Apri applicazione | "apri notepad", "apri spotify" |
| chiudi [app] | Chiudi app | "chiudi chrome" |
| riavvia | Riavvia computer | "riavvia" |
| spegni | Shutdown (con conferma) | "spegni" |
| volume [0-100] | Imposta volume | "volume 75" |
| volume su/giù | Aumenta/diminuisci | "volume su" |
| luminosità [0-100] | Regola brightness | "luminosità 50" |
| attiva screensaver | Avvia screensaver | "attiva screensaver" |
| blocca schermo | Blocca PC | "blocca schermo" |

---

### 📁 FILE & CARTELLE

| Comando | Effetto |
|---------|---------|
| apri file [nome] | Apri file dal desktop |
| apri cartella [nome] | Apri cartella (explorer/finder) |
| elimina [file] | Elimina file (chiede conferma) |
| copia file [nome] | Copia negli appunti |
| sposta [file] a [cartella] | Sposta file |
| cerca [nome] | Ricerca file nel sistema |
| nuovo documento | Crea file vuoto |
| apri downloads | Apri cartella download |

---

### 🌐 BROWSER & WEB

| Comando | Effetto |
|---------|---------|
| apri chrome/firefox/edge | Avvia browser |
| cerca [query] | Google search |
| vai a [url] | Apri URL diretto |
| apri youtube | YouTube |
| apri gmail | Gmail |
| apri github | GitHub |
| apri twitter | Twitter/X |
| apri reddit | Reddit |
| scarica [link] | Download file |

---

### 🎵 MEDIA & AUDIO

| Comando | Effetto |
|---------|---------|
| apri spotify | Avvia Spotify |
| apri vlc | VLC Media Player |
| riproduci musica | Riproduci brano |
| play [canzone] | Riproduci specifica |
| pausa | Pausa media |
| play/pausa | Toggle play |
| skip | Prossimo brano |
| precedente | Brano precedente |
| shuffle on/off | Attiva shuffle |
| repeat one/all | Modalità ripetizione |

---

### 📱 APPLICAZIONI COMUNI

| Comando | App Aperta |
|---------|-----------|
| apri word | Microsoft Word |
| apri excel | Microsoft Excel |
| apri powerpoint | PowerPoint |
| apri vscode | Visual Studio Code |
| apri discord | Discord |
| apri slack | Slack |
| apri zoom | Zoom |
| apri steam | Steam |
| apri telegram | Telegram |
| apri whatsapp | WhatsApp Web |
| apri calc | Calcolatrice |
| apri photoshop | Photoshop (se installato) |
| apri blender | Blender (se installato) |

---

### 🕐 SISTEMA INFORMATIVO

| Comando | Risposta |
|---------|----------|
| che ora è | Mostra ora attuale |
| che data è | Data odierna |
| giorno della settimana | Es: "Lunedì" |
| meteo | Temperatura locale (richiede Internet) |
| uso cpu | % CPU corrente |
| memoria libera | RAM disponibile |
| spazio disco | Storage info |
| batteria | % batteria (laptop) |
| indirizzo ip | IP locale/pubblico |
| sistema operativo | Windows/macOS/Linux versione |

---

### 🔧 SVILUPPO (DEV TOOLS)

| Comando | Effetto |
|---------|---------|
| apri terminal | Bash/PowerShell |
| apri powershell | PowerShell prompt |
| esegui [comando] | Esegui comando shell |
| git clone [repo] | Clone repository |
| python [script] | Esegui script Python |
| npm install [pkg] | NPM package |
| pip install [pkg] | Python package |

---

### 📝 NOTE & APPUNTI

| Comando | Effetto |
|---------|---------|
| crea appunto [testo] | Salva appunto |
| leggi appunti | Lista appunti salvati |
| elimina appunto | Cancella appunto |
| appunto numero [n] | Visualizza specifico |
| esporta appunti | Salva in file |

---

### 🎮 GAMING (se installato)

| Comando | Effetto |
|---------|---------|
| apri steam | Steam launcher |
| apri epic games | Epic Games Launcher |
| apri discord | Join server |
| apri twitch | Twitch streaming |

---

### ⚙️ JARVIS STESSO

| Comando | Effetto |
|---------|---------|
| impostazioni | Apri settings panel |
| aiuto | Mostra comandi disponibili |
| versione | v0.0.01 info |
| stato | Status sfera JARVIS |
| cambia wake-word | Personalizza wake-word |
| reset | Ripristina impostazioni default |
| log | Mostra log file |
| esci | Chiudi JARVIS |

---

## 🎙️ SINTASSI AVANZATA

### Parametri Opzionali
```
"apri file" (se non specifichi nome, chiede)
"apri documents [nome]" (cartella specifica)
```

### Operatori Logici
```
"apri chrome e cerca python" (esegui sequenza)
"pausa e vai a [timestamp]" (comandi multipli)
```

### Variabili Globali
```
[app] = qualsiasi applicazione nel sistema
[url] = indirizzo web completo
[file] = file sul desktop/downloads
[query] = termine di ricerca
[numero] = 0-100
```

---

## 🔗 COMANDI A CATENA

Puoi combinare comandi:

```
"apri youtube e cerca iron man trailer"
→ Apre YouTube, cerca "iron man trailer"

"volume 80 e riproduci musica"
→ Imposta volume 80%, avvia musica

"apri chrome e vai a github.com"
→ Apre Chrome, naviga a GitHub
```

---

## 🚫 COMANDI NON DISPONIBILI (v0.0.01)

- Voice call/video call (uso telefonata)
- Control smart home (versioni future)
- AI conversation (JARVIS non chiacchiera)
- Online API calls (tranne ricerca web)

---

## 💡 TIPS

1. **Pronuncia chiaramente** - JARVIS capisce meglio con pause
2. **Usa nomi esatti** - "apri GIMP" non "apri immagini"
3. **Comandi brevi** - Più diretti = più veloci
4. **Check impostazioni** - Personalizza wake-word e sensibilità
5. **Log file** - Controlla `logs/JARVIS.log` per debug

---

**Versione:** 0.0.01  
**Ultimo aggiornamento:** 2026-05-12
