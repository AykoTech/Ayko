#!/bin/bash
set -e

echo ""
echo "========================================"
echo "JARVIS - Desktop AI Assistant Installer"
echo "========================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "macOS: brew install python3"
    echo "Linux: sudo apt install python3 python3-pip"
    exit 1
fi

echo "[1/5] Python found ✓"

# Create venv
echo "[2/5] Creating virtual environment..."
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install packages
echo "[3/5] Installing Python packages..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

# Check Ollama
echo "[4/5] Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "WARNING: Ollama not found!"
    echo "macOS: brew install ollama"
    echo "Linux: curl https://ollama.ai/install.sh | sh"
    echo ""
    read -p "Visit ollama.ai? (y/n): " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [[ "$OSTYPE" == "darwin"* ]]; then
            open https://ollama.ai/download
        else
            xdg-open https://ollama.ai/download
        fi
    fi
fi

# Download models
echo "[5/5] Downloading LLM models..."
echo "This may take 5-10 minutes..."
ollama pull tinyllama

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "To start JARVIS:"
echo "  1. source venv/bin/activate"
echo "  2. python3 src/main.py"
echo ""
