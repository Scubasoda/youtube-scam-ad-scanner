# YouTube Scam Ad Scanner

A Python tool to scan YouTube ads (landing pages and ad text) for common scam indicators.

## Overview

This scanner analyzes URLs for suspicious characteristics that commonly appear in scam advertisements, including:
- Suspicious domain patterns and TLDs
- Scam keywords and urgency language
- Too-good-to-be-true phrases
- Missing security features (HTTPS)
- Suspicious page content and scripts

## Goals

- Provide a lightweight, extensible scanner for detecting likely scam ads
- Focus on analyzing ad landing pages and ad copy using heuristics
- Enable users to quickly assess the legitimacy of advertisement URLs
- Build ML-ready features for future model training

## Quick Start

### Installation

1. **Clone the repository** (or download the source)

2. **Create a virtual environment and install dependencies:**

   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   
   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Basic Usage

**Scan a suspicious URL:**

```bash
python -m src.scanner --url "https://example.com/suspicious-offer"
```

**Get JSON output:**

```bash
python -m src.scanner --url "https://example.com" --json
```

**Set custom timeout:**

```bash
python -m src.scanner --url "https://example.com" --timeout 15
```

### Example Output

```
======================================================================
SCAM SCAN RESULTS
======================================================================

URL: http://get-rich-quick.xyz/offer
Valid URL: True
Accessible: True

Risk Level: HIGH (Score: 65)

Indicators Found (5):
  1. Suspicious TLD: .xyz
  2. No HTTPS encryption
  3. Found 3 scam keywords: get rich quick, make money fast, limited time offer
  4. High urgency language detected (4 instances)
  5. Excessive exclamation marks (15)

======================================================================

⚠️  WARNING: This URL shows multiple scam indicators. Avoid interaction.
```


## Project Structure

```
youtube-scam-ad-scanner/
├── README.md              # This file
├── LICENSE                # MIT license
├── EXAMPLES.md            # Detailed usage examples
├── requirements.txt       # Python dependencies
├── pytest.ini             # Pytest configuration
├── .gitignore            # Git ignore patterns
├── src/
│   ├── __init__.py       # Package initialization
│   └── scanner.py        # Main scanner implementation and CLI
└── tests/
    ├── __init__.py       # Test package initialization
    └── test_scanner.py   # Unit tests
```

## Features

### Detection Capabilities

**Domain Analysis:**
- Suspicious TLDs (.xyz, .top, .click, .loan, etc.)
- IP addresses instead of domain names
- Excessively long domain names
- Multiple hyphens or numbers in domains
- Missing HTTPS encryption

**Content Analysis:**
- Scam keywords (get rich quick, make money fast, etc.)
- Urgency and pressure tactics
- Too-good-to-be-true phrases
- Excessive punctuation
- Suspicious scripts (alerts, popups)
- Password input fields
- Forms with missing or suspicious actions
- Missing meta descriptions

### Risk Scoring

The scanner assigns a numerical risk score and categorizes URLs into risk levels:

- **MINIMAL** (< 10): URL appears safe
- **LOW** (10-24): Minor concerns detected
- **MEDIUM** (25-49): Multiple suspicious indicators
- **HIGH** (≥ 50): Strong scam indicators detected

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Skip slow network tests
pytest -m "not slow"

# Run specific test file
pytest tests/test_scanner.py
```

## Development

### Adding New Scam Indicators

Edit the `ScamIndicators` class in `src/scanner.py`:

```python
class ScamIndicators:
    SCAM_KEYWORDS = [
        'your keyword here',
        # ... more keywords
    ]
```

### Adjusting Risk Scores

Modify the scoring logic in the `ScamScanner` methods:
- `_analyze_domain()` - Domain-based scoring
- `_analyze_content()` - Content-based scoring
- `_calculate_risk_level()` - Risk level thresholds

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed usage examples and integration patterns.

## Limitations

- **Heuristic-based**: May have false positives or negatives
- **Cannot detect all scams**: Sophisticated scams may bypass detection
- **No authentication**: Cannot analyze content behind login walls
- **Static analysis only**: Does not execute JavaScript or analyze images
- **Context matters**: Some legitimate sites may trigger warnings

## Future Work

Planned enhancements:
- 🔌 Browser extension to capture ads automatically
- 🤖 Machine learning models trained on labeled scam ads
- 📸 Selenium-based ad capture with screenshots
- 🗄️ Database of known scam domains
- 📊 Visual analysis of landing pages
- 📤 Report submission to platforms (YouTube, etc.)
- 🌐 API service for integration with other tools

## Contributing

This is currently a private prototype. Contributions, suggestions, and bug reports are welcome through issues and pull requests.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational and research purposes. It provides heuristic-based analysis and should not be the sole method for determining if a URL is malicious. Always exercise caution when visiting unfamiliar websites and use multiple security tools for comprehensive protection.

## Contact

Project maintained by Scubasoda

---

**Note:** This scanner is designed to help identify potentially suspicious URLs but is not a replacement for comprehensive security software or human judgment. Always be cautious online and report suspicious ads to the appropriate platforms.