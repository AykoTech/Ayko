#!/usr/bin/env python3
"""
JARVIS Quick Start - Run this to start JARVIS
"""

import sys
from pathlib import Path

# Ensure we can import from src/
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║              JARVIS v0.0.01 - Starting                    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    
    # Pre-flight checks
    print("[1] Environment check...")
    try:
        from PyQt6.QtWidgets import QApplication
        from src.core import LLMEngine
        print("✓ Imports OK")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return 1
    
    # Check Ollama
    print("[2] Checking Ollama...")
    llm = LLMEngine()
    if not llm.is_ready:
        print("⚠ Warning: Ollama not responding")
        print("Start Ollama: ollama serve")
        print("Press ENTER to continue anyway...")
        input()
    else:
        print("✓ Ollama OK")
    
    print("[3] Starting JARVIS...")
    print("")
    
    # Start application
    try:
        from src.main import JARVISApplication
        
        app = QApplication(sys.argv)
        window = JARVISApplication()
        window.show()
        
        sys.exit(app.exec())
    
    except Exception as e:
        print(f"✗ Error starting JARVIS: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
