#!/bin/bash
# Phi3 Autonomous Agent - Quick Start Launcher
# Linux/Mac shell script to run quickstart.py

echo ""
echo "======================================================================"
echo "  PHI3 AUTONOMOUS AGENT - LAUNCHER"
echo "======================================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found!"
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
pip show requests &>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Run the quickstart script
echo ""
echo "Starting Phi3 Quickstart..."
echo ""
python3 quickstart.py

# Keep terminal open on exit
echo ""
echo ""
read -p "Press Enter to exit..."
