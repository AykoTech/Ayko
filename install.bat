@echo off
REM JARVIS Installation Script - Windows
REM v0.0.01

echo.
echo ========================================
echo JARVIS - Desktop AI Assistant Installer
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Remember to check "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/5] Python found ✓

REM Create venv
echo [2/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create venv
    pause
    exit /b 1
)

REM Activate venv and install
echo [3/5] Installing Python packages...
call venv\Scripts\activate.bat
pip install --upgrade pip setuptools wheel >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

REM Check Ollama
echo [4/5] Checking Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama not found!
    echo Download from https://ollama.ai/download
    echo.
    set /p install_ollama="Install Ollama now? (y/n): "
    if /i "!install_ollama!"=="y" (
        start https://ollama.ai/download
    )
)

REM Download models
echo [5/5] Downloading LLM models...
echo This may take 5-10 minutes...
ollama pull tinyllama
echo.
echo ========================================
echo Installation complete!
echo ========================================
echo.
echo To start JARVIS:
echo   1. Open PowerShell in this folder
echo   2. Run: .\venv\Scripts\activate.bat
echo   3. Run: python src/main.py
echo.
pause
