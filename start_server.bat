@echo off
REM Quick start script for Windows
REM Starts the API server for automatic scanning

echo ========================================
echo YouTube Scam Ad Scanner - API Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\" (
    echo Error: Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Virtual environment activated
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not installed. Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo Starting API server...
echo.
echo The server will run at: http://localhost:5000
echo.
echo Instructions:
echo 1. Keep this window open
echo 2. Install the browser extension if you haven't
echo 3. Browse YouTube - ads will be scanned automatically!
echo 4. View logs with: python view_logs.py stats
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the API server
python api_server.py

pause
