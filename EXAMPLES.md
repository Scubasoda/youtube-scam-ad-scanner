# YouTube Scam Ad Scanner - Examples

This document provides usage examples for the YouTube Scam Ad Scanner.

## Installation

First, set up the environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Scan a single URL

```bash
python -m src.scanner --url "https://example.com/suspicious-offer"
```

### Scan with custom timeout

```bash
python -m src.scanner --url "https://example.com" --timeout 15
```

### Get JSON output

```bash
python -m src.scanner --url "https://example.com" --json
```

## Example Scans

### Example 1: Legitimate Website

```bash
python -m src.scanner --url "https://www.wikipedia.org"
```

Expected result: Low or minimal risk

### Example 2: Testing Suspicious Indicators

```bash
python -m src.scanner --url "http://get-rich-quick.xyz/offer"
```

This URL would trigger multiple indicators:
- Suspicious TLD (.xyz)
- No HTTPS
- Scam keywords in domain

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run only fast tests (skip slow network tests)
pytest -m "not slow"

# Run specific test file
pytest tests/test_scanner.py

# Run specific test
pytest tests/test_scanner.py::TestScamScanner::test_invalid_url_detection
```

## Understanding Results

### Risk Levels

- **MINIMAL** (score < 10): URL appears safe
- **LOW** (score 10-24): Some minor concerns
- **MEDIUM** (score 25-49): Multiple suspicious indicators
- **HIGH** (score ≥ 50): Strong scam indicators detected

### Common Indicators

1. **Domain-based**:
   - Suspicious TLD (.xyz, .top, .click, etc.)
   - No HTTPS encryption
   - IP address instead of domain
   - Excessive hyphens or numbers
   - Unusually long domain name

2. **Content-based**:
   - Scam keywords (get rich quick, make money fast, etc.)
   - Urgency language (act now, limited time, etc.)
   - Too-good-to-be-true phrases
   - Excessive exclamation marks
   - Popup/alert scripts
   - Password input fields
   - Missing meta description

## Integration Examples

### Using as a Python Module

```python
from src.scanner import ScamScanner

# Create scanner instance
scanner = ScamScanner(timeout=10)

# Scan a URL
results = scanner.scan_url("https://example.com")

# Access results
print(f"Risk Level: {results['risk_level']}")
print(f"Risk Score: {results['risk_score']}")
print(f"Indicators: {results['indicators']}")

# Check if high risk
if results['risk_level'] == 'HIGH':
    print("⚠️ Warning: High risk detected!")
```

### Batch Scanning

```python
from src.scanner import ScamScanner

urls = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
]

scanner = ScamScanner()

for url in urls:
    results = scanner.scan_url(url)
    print(f"{url}: {results['risk_level']} ({results['risk_score']})")
```

## Tips for Best Results

1. **Always include the protocol** (http:// or https://)
2. **Test the actual landing page URL** from the ad, not the ad platform URL
3. **Review all indicators** - some legitimate sites may trigger false positives
4. **Use context** - combine automated scanning with human judgment
5. **Report suspicious ads** to the platform (YouTube, etc.)

## Limitations

- This is a heuristic-based scanner and may have false positives/negatives
- Cannot detect all types of scams
- Cannot access content behind login walls or CAPTCHAs
- Some legitimate sites may trigger warnings (e.g., promotional language)
- Does not analyze video content or images

## Future Enhancements

Planned features:
- Browser extension for automatic ad capture
- Machine learning models for better detection
- Database of known scam domains
- Screenshot capture and visual analysis
- Integration with platform reporting APIs
