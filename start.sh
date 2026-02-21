#!/bin/bash
# Quick start script for Linux/macOS

echo "========================================"
echo "  Mood Detection System - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo ""

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo ""

# Start the application
echo "========================================"
echo "  Starting Mood Detection System..."
echo "========================================"
echo ""
echo "Open your browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python web_mood_app.py
