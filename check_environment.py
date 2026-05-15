#!/usr/bin/env python3
"""Check JARVIS environment and dependencies."""

import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check Python version >= 3.10"""
    if sys.version_info < (3, 10):
        print(f"✗ Python 3.10+ required. You have {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_module(module_name, package_name=None):
    """Check if Python module is installed."""
    spec = importlib.util.find_spec(module_name)
    installed = spec is not None
    status = "✓" if installed else "✗"
    pkg = package_name or module_name
    print(f"{status} {pkg}")
    return installed

def check_ollama():
    """Check if Ollama is installed and running."""
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, timeout=2)
        if result.returncode == 0:
            version = result.stdout.decode().strip()
            print(f"✓ Ollama: {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    print("✗ Ollama not found. Install from https://ollama.ai")
    return False

def check_model(model_name="tinyllama"):
    """Check if LLM model is available."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            models = result.stdout.decode()
            if model_name in models:
                print(f"✓ Model {model_name} available")
                return True
            else:
                print(f"⚠ Model {model_name} not found. Run: ollama pull {model_name}")
                return False
    except:
        pass
    return False

def check_vosk_model():
    """Check if Vosk model directory exists."""
    model_path = Path("model")
    if model_path.exists() and model_path.is_dir():
        print("✓ Vosk model directory found")
        return True
    else:
        print("⚠ Vosk model directory not found. Download from https://alphacephei.com/vosk/models")
        return False

def main():
    print("")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         JARVIS v0.0.01 - Environment Check                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    
    results = {}
    
    # Check Python
    print("[1] Python Version")
    results["python"] = check_python_version()
    print()
    
    # Check Python modules
    print("[2] Python Modules")
    modules = [
        ("PyQt6", "PyQt6"),
        ("PyQt6.QtWebEngineWidgets", "PyQtWebEngine"),
        ("sounddevice", "sounddevice"),
        ("vosk", "vosk"),
        ("pyttsx3", "pyttsx3"),
        ("requests", "requests"),
        ("psutil", "psutil"),
    ]
    
    all_modules_ok = True
    for module, name in modules:
        if not check_module(module, name):
            all_modules_ok = False
    results["modules"] = all_modules_ok
    print()
    
    # Check external dependencies
    print("[3] External Dependencies")
    results["ollama"] = check_ollama()
    print()
    
    # Check models
    print("[4] Models")
    results["vosk_model"] = check_vosk_model()
    results["ollama_model"] = check_model("tinyllama")
    print()
    
    # Summary
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                      SUMMARY                              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    critical_pass = results["python"] and results["modules"]
    all_pass = all(results.values())
    
    if critical_pass:
        print("✓ Critical dependencies: OK")
    else:
        print("✗ Critical dependencies: MISSING")
        print("  → Run: pip install -r requirements.txt")
        return 1
    
    if results["ollama"]:
        print("✓ Ollama: READY")
    else:
        print("⚠ Ollama: NOT FOUND")
        print("  → Install from https://ollama.ai")
    
    if results["vosk_model"]:
        print("✓ Vosk model: READY")
    else:
        print("⚠ Vosk model: MISSING")
        print("  → Download from https://alphacephei.com/vosk/models")
    
    if results["ollama_model"]:
        print("✓ LLM model: READY")
    else:
        print("⚠ LLM model: MISSING")
        print("  → Run: ollama pull tinyllama")
    
    print()
    
    if all_pass:
        print("✓✓✓ ENVIRONMENT READY FOR JARVIS ✓✓✓")
        return 0
    elif critical_pass:
        print("⚠ Download models to use JARVIS:")
        print("  1. ollama pull tinyllama")
        print("  2. Download Vosk model to 'model/' directory")
        return 0
    else:
        print("✗ Environment check failed. Fix issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
