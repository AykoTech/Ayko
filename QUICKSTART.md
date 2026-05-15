# JARVIS v0.0.01 - QUICK START GUIDE

## 30 Seconds Setup

### Windows
```bash
# 1. Open PowerShell in project folder
# 2. Run:
.\install.bat

# 3. Wait for completion
# 4. Start JARVIS:
python run.py
```

### macOS/Linux
```bash
# 1. Open Terminal in project folder
# 2. Run:
chmod +x install.sh
./install.sh

# 3. Activate venv:
source venv/bin/activate

# 4. Start JARVIS:
python run.py
```

---

## What Happens During Setup

**install.bat / install.sh:**
1. ✓ Create Python virtual environment
2. ✓ Install Python dependencies
3. ✓ Check/install Ollama
4. ✓ Download TinyLlama model (~700MB)
5. ✓ Verify setup with tests

**Takes ~5-15 minutes** (depending on internet)

---

## First Run Checklist

- [ ] Install script completed without errors
- [ ] `python check_environment.py` shows ✓ for all critical items
- [ ] `python test_architecture.py` passes
- [ ] `python run.py` starts without crashes

---

## Using JARVIS

1. **Start the app:**
   ```bash
   python run.py
   ```

2. **You'll see:**
   - JARVIS window with 3D animated sphere
   - "Ready" status in green

3. **Speak a command:**
   - Click "Start Listening" (or microphone button)
   - Say: "JARVIS, open youtube"
   - JARVIS responds: "Ho aperto YouTube"
   - YouTube opens

4. **Try these commands:**
   ```
   "JARVIS, what time is it"
   "JARVIS, close chrome"
   "JARVIS, search python"
   "JARVIS, volume 80"
   ```

---

## Troubleshooting

### Ollama not found
```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
Download from https://ollama.ai/download
```

### Microphone not working
- Windows: Settings > Privacy > Microphone > Allow
- macOS: System Preferences > Security > Microphone
- Linux: Check audio settings

### "Model not found" error
```bash
# Download Vosk model to 'model/' directory
# OR download TinyLlama:
ollama pull tinyllama
```

### App crashes on startup
```bash
# Run environment check:
python check_environment.py

# Run tests:
python test_architecture.py
```

---

## Next Steps

1. **Customize wake-word:**
   - Click Settings in JARVIS
   - Change "JARVIS" to your custom word

2. **Create your first tool:**
   - Read DEVELOPMENT.md
   - Follow the 5-minute example

3. **Integrate with your workflow:**
   - Add tools for your specific needs
   - Automate common tasks

---

## Files You Need

**To Run:**
- `run.py` - Quick start
- `src/main.py` - Entry point

**To Setup:**
- `install.bat` (Windows)
- `install.sh` (Mac/Linux)
- `check_environment.py` - Verify setup

**To Understand:**
- `README.md` - Full setup guide
- `ARCHITECTURE.md` - How it works
- `COMMANDS.md` - Available commands

**To Extend:**
- `DEVELOPMENT.md` - Create new tools
- `src/core/tools.py` - See examples

---

## Common Questions

**Q: Why do I need Ollama?**
A: Runs the language model locally (no cloud, no account)

**Q: Can I use a different wake-word?**
A: Yes! Settings panel > Wake-word

**Q: Can I use different LLM models?**
A: Yes! Change in settings (mistral is better but slower)

**Q: Does JARVIS work offline?**
A: Fully offline except web search (which needs internet)

**Q: Can I modify commands?**
A: Yes! Read DEVELOPMENT.md for examples

---

**Ready to go!** Run `python run.py` 🚀
