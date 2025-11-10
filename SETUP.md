# Setup Guide - YouTube Scam Ad Scanner

This guide will walk you through setting up the YouTube Scam Ad Scanner on your system.

## Prerequisites

- **Python 3.8 or higher** installed on your system
- **pip** (Python package installer)
- **Git** (optional, for cloning the repository)
- **Virtual environment support** (recommended)

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher.

## Installation Steps

### Step 1: Get the Code

**Option A: Clone with Git**
```bash
git clone https://github.com/Scubasoda/youtube-scam-ad-scanner.git
cd youtube-scam-ad-scanner
```

**Option B: Download as ZIP**
- Download the repository as a ZIP file
- Extract to a folder of your choice
- Open terminal/command prompt in that folder

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

You should see `(.venv)` appear in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- requests - HTTP library
- beautifulsoup4 - HTML parsing
- lxml - XML/HTML parser
- validators - URL validation
- tldextract - Domain extraction
- nltk - Natural language toolkit
- click - CLI framework
- colorama - Colored terminal output
- pytest - Testing framework
- pytest-cov - Coverage reporting

### Step 4: Verify Installation

Test that everything is working:

```bash
python -m src.scanner --url "https://www.wikipedia.org"
```

You should see output showing the scan results.

## Quick Start Examples

### Scan a Single URL

```bash
python -m src.scanner --url "https://example.com"
```

### Get JSON Output

```bash
python -m src.scanner --url "https://example.com" --json
```

### Scan with Custom Timeout

```bash
python -m src.scanner --url "https://example.com" --timeout 15
```

## Running Tests

Make sure you're in the project directory with the virtual environment activated:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Open coverage report (after running above)
# Windows:
start htmlcov\index.html
# macOS:
open htmlcov/index.html
# Linux:
xdg-open htmlcov/index.html

# Run only fast tests (skip network tests)
pytest -m "not slow"
```

## Batch Testing

Use the provided batch testing script:

```bash
python test_batch.py
```

This will scan multiple URLs and provide a summary report.

## Troubleshooting

### Issue: "Python not found"

**Solution:**
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python`
- On Windows, try installing from Microsoft Store or python.org

### Issue: "pip not found"

**Solution:**
```bash
python -m ensurepip --upgrade
```

### Issue: "Permission denied" when activating virtual environment (Windows)

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Import errors when running scanner

**Solution:**
- Make sure virtual environment is activated (you should see `(.venv)`)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:**
Make sure you're running the command from the project root directory:
```bash
# Should be in: youtube-scam-ad-scanner/
pwd  # or cd on Windows
```

### Issue: Network/timeout errors when scanning

**Solution:**
- Increase timeout: `--timeout 30`
- Check your internet connection
- Some sites may block automated requests
- Try a different URL to verify scanner is working

### Issue: SSL certificate errors

**Solution:**
```bash
pip install --upgrade certifi
```

## Development Setup

If you plan to contribute or modify the code:

### Install Development Tools

```bash
pip install -r requirements.txt
pip install black flake8 mypy  # Optional: code formatting and linting
```

### Setup Git Hooks (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/sh
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed, commit aborted"
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Updating the Scanner

### Pull Latest Changes

```bash
git pull origin main
```

### Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

## Uninstalling

### Deactivate Virtual Environment

```bash
deactivate
```

### Remove Project

Simply delete the project folder:
```bash
# Make sure you're in the parent directory
rm -rf youtube-scam-ad-scanner  # Linux/macOS
# or
rmdir /s youtube-scam-ad-scanner  # Windows
```

## Platform-Specific Notes

### Windows

- Use PowerShell or Command Prompt
- Backslashes (`\`) in paths
- May need to adjust execution policy for scripts

### macOS

- May need to use `python3` and `pip3` instead of `python` and `pip`
- Use Terminal app
- Forward slashes (`/`) in paths

### Linux

- Most distributions come with Python pre-installed
- May need to install python3-venv: `sudo apt install python3-venv`
- Use your preferred terminal
- Forward slashes (`/`) in paths

## Getting Help

- **Documentation**: See README.md and EXAMPLES.md
- **Issues**: Check existing issues or create a new one
- **Contributing**: See CONTRIBUTING.md for guidelines

## Next Steps

1. ✅ Scanner is installed and working
2. 📖 Read [EXAMPLES.md](EXAMPLES.md) for usage examples
3. 🧪 Try scanning some URLs
4. 🔧 Customize indicators in `src/scanner.py`
5. 🤝 Consider contributing (see CONTRIBUTING.md)

---

**Congratulations!** You're ready to start using the YouTube Scam Ad Scanner.
