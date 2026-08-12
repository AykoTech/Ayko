#!/bin/bash
# Advanced JARVIS Setup Script

set -e

echo "🚀 JARVIS v0.0.01 - Advanced Setup"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3 --version

required_version="3.10"
current_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

if [ "$(printf '%s\n' "$required_version" "$current_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo -e "${GREEN}✓ Python $current_version OK${NC}"
else
    echo -e "${RED}✗ Python 3.10+ required${NC}"
    exit 1
fi

echo ""

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created${NC}"

echo ""

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""

# Create directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p ~/.jarvis/logs
mkdir -p ~/.jarvis/config
mkdir -p ~/.jarvis/data
echo -e "${GREEN}✓ Directories created${NC}"

echo ""

# Run setup script
echo -e "${BLUE}Running setup...${NC}"
python setup.py
echo -e "${GREEN}✓ Setup completed${NC}"

echo ""

# Test import
echo -e "${BLUE}Testing imports...${NC}"
python -c "from src.core.core import JARVISCore; print('✓ Core imports OK')"

echo ""

echo -e "${GREEN}════════════════════════════════════════════════════"
echo -e "✓ JARVIS Setup Complete!"
echo -e "════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run JARVIS: python run.py"
echo ""
