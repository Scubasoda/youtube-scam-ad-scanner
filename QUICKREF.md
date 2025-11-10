# Quick Reference - YouTube Scam Ad Scanner

## Installation
```bash
python -m venv .venv
.\.venv\Scripts\activate          # Windows
source .venv/bin/activate         # macOS/Linux
pip install -r requirements.txt
```

## Basic Commands

### Start Automatic Scanning
```bash
python api_server.py              # Start API server
start_server.bat                  # Windows quick start
./start_server.sh                 # macOS/Linux quick start
```

### Scan a URL
```bash
python -m src.scanner --url "https://example.com"
```

### View Logs
```bash
python view_logs.py view          # Recent scans
python view_logs.py stats         # Statistics
python view_logs.py report        # HTML report
python view_logs.py find "url"    # Find specific URL
```

### JSON Output
```bash
python -m src.scanner --url "https://example.com" --json
```

### Custom Timeout
```bash
python -m src.scanner --url "https://example.com" --timeout 15
```

### Help
```bash
python -m src.scanner --help
python view_logs.py --help
```

## Testing

```bash
pytest                              # Run all tests
pytest -v                          # Verbose output
pytest --cov=src                   # With coverage
pytest -m "not slow"               # Skip slow tests
pytest tests/test_scanner.py       # Specific file
```

## Risk Levels

| Level   | Score Range | Meaning                          |
|---------|-------------|----------------------------------|
| MINIMAL | < 10        | URL appears safe                 |
| LOW     | 10-24       | Minor concerns detected          |
| MEDIUM  | 25-49       | Multiple suspicious indicators   |
| HIGH    | ≥ 50        | Strong scam indicators detected  |

## Common Indicators

### Domain-Based
- ❌ Suspicious TLD (.xyz, .top, .click, .loan, .work)
- ❌ No HTTPS encryption
- ❌ IP address instead of domain
- ❌ Excessively long domain name (>20 chars)
- ❌ Multiple hyphens or numbers in domain

### Content-Based
- ❌ Scam keywords (get rich quick, make money fast, etc.)
- ❌ Urgency language (act now, limited time, etc.)
- ❌ Too-good-to-be-true phrases
- ❌ Excessive exclamation marks
- ❌ Popup/alert scripts
- ❌ Password input fields
- ❌ Suspicious forms

## Exit Codes

- `0` - Scan completed, risk level below HIGH
- `1` - Scan completed, HIGH risk detected

## Python API

```python
from src.scanner import ScamScanner

# Create scanner
scanner = ScamScanner(timeout=10)

# Scan URL
results = scanner.scan_url("https://example.com")

# Access results
print(results['risk_level'])     # MINIMAL, LOW, MEDIUM, or HIGH
print(results['risk_score'])     # Numerical score
print(results['indicators'])     # List of detected indicators
print(results['valid_url'])      # Boolean
print(results['accessible'])     # Boolean
```

## File Structure

```
youtube-scam-ad-scanner/
├── src/
│   ├── scanner.py       # Main scanner code
│   └── config.py        # Configuration settings
├── tests/
│   └── test_scanner.py  # Unit tests
├── README.md            # Project overview
├── SETUP.md             # Installation guide
├── EXAMPLES.md          # Usage examples
└── requirements.txt     # Dependencies
```

## Customization

### Add Keywords
Edit `src/scanner.py`:
```python
class ScamIndicators:
    SCAM_KEYWORDS = [
        'new keyword',
        # ...
    ]
```

### Adjust Scores
Edit `src/config.py`:
```python
SCORE_SUSPICIOUS_TLD = 15  # Change this value
```

### Modify Risk Thresholds
Edit `src/config.py`:
```python
RISK_THRESHOLD_MINIMAL = 10
RISK_THRESHOLD_LOW = 25
RISK_THRESHOLD_MEDIUM = 50
```

## Batch Scanning

```bash
python test_batch.py
```

Or create your own:
```python
from src.scanner import ScamScanner

urls = ['https://url1.com', 'https://url2.com']
scanner = ScamScanner()

for url in urls:
    results = scanner.scan_url(url)
    print(f"{url}: {results['risk_level']}")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Activate virtual environment |
| Timeout errors | Increase `--timeout` value |
| SSL errors | `pip install --upgrade certifi` |
| Permission denied | `Set-ExecutionPolicy RemoteSigned` (Windows) |

## Links

- 📖 Full documentation: README.md
- 🔧 Setup guide: SETUP.md
- 💡 Examples: EXAMPLES.md
- � Auto-scan guide: AUTOSCAN.md
- �🤝 Contributing: CONTRIBUTING.md
- 📋 Changelog: CHANGELOG.md

## Tips

✅ Always include http:// or https:// in URLs
✅ Test with legitimate sites first to understand output
✅ Review all indicators, not just the risk score
✅ Use batch scanning for multiple URLs
✅ Report actual scam ads to YouTube

⚠️ This tool uses heuristics and may have false positives
⚠️ Not a replacement for comprehensive security tools
⚠️ Always exercise caution with unfamiliar websites
