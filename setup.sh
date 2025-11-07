#!/bin/bash

# AI Resume-Job Matcher Setup Script
# This script sets up the application on Ubuntu

echo "========================================"
echo "AI Resume-Job Matcher - Setup"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}✗ Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher:"
    echo "sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Check if pip is installed
echo -e "${YELLOW}Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${RED}✗ pip3 is not installed!${NC}"
    echo "Installing pip3..."
    sudo apt install python3-pip
fi

# Create virtual environment
echo ""
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install requirements
echo ""
echo -e "${YELLOW}Installing Python dependencies...${NC}"
echo "This may take several minutes..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Download NLTK data
echo ""
echo -e "${YELLOW}Downloading NLTK data...${NC}"
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('punkt_tab', quiet=True)"
echo -e "${GREEN}✓ NLTK data downloaded${NC}"

# Download AI model
echo ""
echo -e "${YELLOW}Downloading AI model...${NC}"
echo "This will download ~90MB of data. Please wait..."
python3 models/download_model.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ AI model downloaded successfully${NC}"
else
    echo -e "${RED}✗ Failed to download AI model${NC}"
    exit 1
fi

# Setup complete
echo ""
echo "========================================"
echo -e "${GREEN}✓ Setup completed successfully!${NC}"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Start the backend:  ./run_backend.sh"
echo "  2. Start the frontend: ./run_frontend.sh"
echo ""
echo "Or use: ./run.sh (to run both)"
echo ""
echo "The app will be available at:"
echo "  - Frontend: http://localhost:8501"
echo "  - Backend API: http://localhost:8000"
echo ""
echo "Happy matching! 🎯"
