# Automatic Scanning & Logging Guide

This guide explains how to enable automatic scanning and view scan logs.

## 🚀 Quick Start: Automatic Scanning

### Step 1: Install API Dependencies

```bash
# Make sure virtual environment is activated
.\.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux

# Install Flask for API server
pip install -r requirements.txt
```

### Step 2: Start the API Server

```bash
python api_server.py
```

You should see:
```
Starting YouTube Scam Ad Scanner API Server
Logs will be saved to: C:\...\scan_logs
API available at: http://localhost:5000
```

**Keep this running in the background!**

### Step 3: Install Browser Extension

If you haven't already:
1. Open `chrome://extensions/`
2. Enable Developer Mode
3. Load the `browser-extension` folder

### Step 4: Browse YouTube!

- The extension captures ad URLs automatically
- The API server scans them in real-time
- All scans are logged automatically
- You get notified if HIGH risk ads are detected

## 📊 How It Works

```
┌─────────────┐
│   YouTube   │ 
│  (You watch │ 
│   videos)   │
└──────┬──────┘
       │ Ad appears
       ▼
┌──────────────┐
│   Browser    │ ← Captures URL
│  Extension   │
└──────┬───────┘
       │ Sends to API
       ▼
┌──────────────┐
│ API Server   │ ← Scans URL
│ (Flask API)  │ ← Logs result
└──────┬───────┘
       │ Returns risk level
       ▼
┌──────────────┐
│  scan_logs/  │ ← All scans saved
│   Directory  │
└──────────────┘
```

## 📝 Viewing Logs

### Method 1: Command Line Tool

```bash
# View recent scans
python view_logs.py view

# View only high-risk scans
python view_logs.py view --risk-level HIGH

# Show statistics
python view_logs.py stats

# Find scans for specific URL
python view_logs.py find "example.com"

# Generate HTML report
python view_logs.py report
```

### Method 2: API Endpoints

While the API server is running:

```bash
# View logs via browser
http://localhost:5000/logs

# Get statistics
http://localhost:5000/stats

# Check status
http://localhost:5000/status
```

### Method 3: Direct File Access

Log files are stored in `scan_logs/`:

- `scans.jsonl` - All scans (JSONL format)
- `scans_2025-11-10.jsonl` - Daily logs
- `api_server.log` - Server activity log

## 📁 Log Format

Each scan is saved as JSON:

```json
{
  "timestamp": "2025-11-10T14:30:00.123456",
  "url": "https://suspicious-site.com",
  "risk_level": "HIGH",
  "risk_score": 65,
  "indicator_count": 5,
  "indicators": [
    "Suspicious TLD: .xyz",
    "No HTTPS encryption",
    "Found 3 scam keywords"
  ],
  "source": "browser-extension",
  "valid_url": true,
  "accessible": true,
  "metadata": {
    "pageUrl": "https://youtube.com/watch?v=...",
    "capturedAt": 1699624200000
  }
}
```

## 🔍 Log Viewer Commands

### View Recent Scans

```bash
# Last 20 scans (default)
python view_logs.py view

# Last 50 scans
python view_logs.py view --limit 50

# Only HIGH risk
python view_logs.py view --risk-level HIGH

# Detailed format
python view_logs.py view --format detailed

# JSON output
python view_logs.py view --format json
```

### Statistics

```bash
python view_logs.py stats
```

Output:
```
======================================================================
SCAN STATISTICS
======================================================================

Total Scans: 150
Unique URLs: 120

Risk Level Distribution:
  HIGH    :   15 ( 10.0%) ███████
  MEDIUM  :   30 ( 20.0%) ██████████████
  LOW     :   45 ( 30.0%) █████████████████████
  MINIMAL :   60 ( 40.0%) ████████████████████████████

Sources:
  browser-extension: 145
  api: 5

⚠️  HIGH RISK URLs (15):
  - http://scam-site.xyz/offer
  - http://fake-deal.top/limited
  ...
```

### HTML Report

```bash
# Generate report
python view_logs.py report

# Custom output file
python view_logs.py report --output my_report.html
```

Opens a beautiful HTML report with:
- Summary statistics
- Charts and graphs
- All scan details
- Filterable tables

## ⚙️ Configuration

### Enable/Disable Auto-Scan

The extension auto-scans by default. To disable:

1. Click extension icon
2. Go to Settings (future feature)
3. Toggle "Auto-scan captured URLs"

Or manually in extension's storage:
```javascript
chrome.storage.sync.set({ autoScan: false });
```

### Change API Port

Edit `api_server.py`:
```python
app.run(
    host='127.0.0.1',
    port=5001,  # Change this
    debug=True
)
```

Then update `browser-extension/background.js`:
```javascript
const response = await fetch('http://localhost:5001/scan', {
    // ...
});
```

## 📊 Log Analysis Examples

### Find All Scam Ads from Specific Domain

```bash
python view_logs.py find "xyz"
```

### Export High-Risk URLs

```python
import json

with open('scan_logs/scans.jsonl', 'r') as f:
    high_risk = [
        json.loads(line)['url'] 
        for line in f 
        if json.loads(line).get('risk_level') == 'HIGH'
    ]

with open('high_risk_urls.txt', 'w') as f:
    f.write('\n'.join(high_risk))
```

### Daily Summary

```python
from collections import Counter
import json
from datetime import date

today = date.today().strftime('%Y-%m-%d')
log_file = f'scan_logs/scans_{today}.jsonl'

with open(log_file, 'r') as f:
    logs = [json.loads(line) for line in f]

print(f"Today's scans: {len(logs)}")
print(f"High risk: {sum(1 for log in logs if log['risk_level'] == 'HIGH')}")
```

## 🔧 Troubleshooting

### "Connection refused" in extension

**Problem:** Extension can't reach API server

**Solution:**
```bash
# Make sure API server is running
python api_server.py

# Check if port 5000 is in use
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # macOS/Linux
```

### Scans not being logged

**Problem:** Logs directory not created

**Solution:**
The API server creates it automatically, but you can manually:
```bash
mkdir scan_logs
```

### View logs: "No scan logs found"

**Problem:** No scans have been performed yet

**Solution:**
1. Make sure API server is running
2. Browse YouTube and click on an ad
3. Check browser console for errors
4. Try manual scan: `python -m src.scanner --url "https://example.com"`

### High memory usage

**Problem:** Too many logs accumulating

**Solution:**
Archive or delete old logs:
```bash
# Archive
mkdir scan_logs/archive
move scan_logs/scans_2025-*.jsonl scan_logs/archive/

# Or delete old daily logs
del scan_logs/scans_2025-10-*.jsonl
```

## 💡 Tips

1. **Keep API server running** in a dedicated terminal window
2. **Check logs regularly** to see what ads you've encountered
3. **Generate weekly reports** to track trends
4. **Export high-risk URLs** to report to YouTube
5. **Use logs for research** to understand scam patterns

## 🚀 Advanced: API Integration

### Scan URL Programmatically

```python
import requests

url_to_scan = "https://suspicious-site.com"

response = requests.post('http://localhost:5000/scan', json={
    'url': url_to_scan,
    'source': 'my-script',
    'metadata': {'custom': 'data'}
})

result = response.json()
print(f"Risk: {result['risk_level']}")
```

### Batch Scan

```python
import requests

urls = ["https://url1.com", "https://url2.com", "https://url3.com"]

response = requests.post('http://localhost:5000/batch-scan', json={
    'urls': urls,
    'source': 'batch-script'
})

results = response.json()
for result in results['results']:
    print(f"{result['url']}: {result['risk_level']}")
```

### Monitor Logs in Real-Time

```bash
# Windows (PowerShell)
Get-Content scan_logs/scans.jsonl -Wait -Tail 10

# macOS/Linux
tail -f scan_logs/scans.jsonl
```

## 📚 See Also

- [API Server Documentation](api_server.py) - Full API reference
- [Browser Extension README](browser-extension/README.md) - Extension details
- [Main README](README.md) - Project overview
