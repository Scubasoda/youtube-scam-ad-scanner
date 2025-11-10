#!/bin/bash
# Quick start script for macOS/Linux
# Starts the API server for automatic scanning

echo "========================================"
echo "YouTube Scam Ad Scanner - API Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "Virtual environment activated"
echo ""

# Check if Flask is installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Flask not installed. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "Starting API server..."
echo ""
echo "The server will run at: http://localhost:5000"
echo ""
echo "Instructions:"
echo "1. Keep this terminal open"
echo "2. Install the browser extension if you haven't"
echo "3. Browse YouTube - ads will be scanned automatically!"
echo "4. View logs with: python view_logs.py stats"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Start the API server
python api_server.py
