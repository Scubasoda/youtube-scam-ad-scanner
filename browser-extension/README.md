# YouTube Scam Ad Scanner - Browser Extension

This Chrome/Edge extension automatically captures ad URLs from YouTube and integrates with the Python scanner.

## ⚠️ Important Legal Notice

**This extension is for personal security research and educational purposes only.**

- ✅ Use for analyzing ads you personally encounter
- ✅ Keep data private and secure
- ✅ Report scams through official YouTube channels
- ❌ Do NOT use for mass data collection or commercial purposes
- ❌ Do NOT violate YouTube's Terms of Service

**You are responsible for ensuring your use complies with all applicable terms and laws.**

See [../LEGAL.md](../LEGAL.md) for complete disclaimer.

## Features

- ✅ Automatically captures ad URLs when you browse YouTube
- ✅ Monitors clicks on ads and ad elements
- ✅ Tracks ad redirects and destination URLs
- ✅ Badge shows count of unscanned URLs
- ✅ Export captured URLs for batch scanning
- ✅ Clean, simple interface

## Installation

### Chrome/Edge

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `browser-extension` folder
5. The extension icon should appear in your toolbar

### Firefox (requires manifest v2 conversion)

Firefox support coming soon - requires converting manifest.json to v2 format.

## Usage

### Automatic Capture

1. **Browse YouTube normally**
   - The extension runs in the background
   - When you see an ad, the extension monitors it
   - Clicking on an ad captures the destination URL

2. **View Captured URLs**
   - Click the extension icon to open the popup
   - See all captured ad URLs with timestamps
   - Check the count in the badge

3. **Export and Scan**
   - Click "Scan All" to copy unscanned URLs to clipboard
   - Run the Python scanner:
     ```bash
     python -m src.scanner --url "PASTE_URL_HERE"
     ```
   - Or use batch scanning (see below)

### Batch Scanning Captured URLs

**Method 1: Via Popup**
1. Click extension icon
2. Click "Scan All" button
3. URLs are copied to clipboard
4. Paste into a file or scan directly

**Method 2: Export to File**
1. Click "Export URLs" button
2. File is downloaded with all URLs
3. Create a Python script to scan them:

```python
from src.scanner import ScamScanner

# Read exported file
with open('youtube-ad-urls-*.txt', 'r') as f:
    urls = [line.split(' (')[0] for line in f.readlines()]

scanner = ScamScanner()
for url in urls:
    result = scanner.scan_url(url)
    print(f"{url}: {result['risk_level']}")
```

## How It Works

### Content Script (`content.js`)
- Runs on all YouTube pages
- Monitors DOM for ad elements
- Captures clicks on ads
- Extracts destination URLs
- Sends to background script

### Background Script (`background.js`)
- Receives captured URLs
- Stores in Chrome storage
- Updates badge count
- Can integrate with local API (optional)

### Popup (`popup.html/js`)
- Displays captured URLs
- Shows statistics
- Export/clear functionality
- Scan trigger

## Storage

URLs are stored locally in Chrome's storage with:
- `url` - The captured ad destination URL
- `timestamp` - When it was captured
- `pageUrl` - YouTube page where ad appeared
- `scanned` - Whether it's been analyzed
- `scanResult` - Scan results (if scanned)

## Integration with Python Scanner

### Option 1: Manual (Current)
1. Extension captures URLs
2. User exports or copies URLs
3. User runs Python scanner manually
4. Results are shown in terminal

### Option 2: Local API (Advanced)
Set up a local Flask server to enable automatic scanning:

```python
# api_server.py
from flask import Flask, request, jsonify
from src.scanner import ScamScanner

app = Flask(__name__)
scanner = ScamScanner()

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url')
    result = scanner.scan_url(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
```

Then the extension can call this API automatically!

## Permissions Explained

- **webRequest** - Monitor ad-related network requests
- **storage** - Save captured URLs locally
- **tabs** - Access current tab information
- **host_permissions** - Access YouTube and ad domains

## Privacy

- All data stays local on your computer
- No data sent to external servers
- URLs only stored in browser storage
- You control what gets scanned and when

## Troubleshooting

**Extension not capturing ads:**
- Make sure you're on youtube.com
- Try refreshing the YouTube page
- Check browser console for errors (F12)
- Some ads may not be captured due to YouTube's ad system

**Badge not updating:**
- Click extension icon to refresh
- Reload the extension in chrome://extensions

**Can't load extension:**
- Make sure you selected the `browser-extension` folder
- Check that all files are present
- Enable Developer Mode

## Future Enhancements

- [ ] Real-time scanning via local API
- [ ] Risk indicators shown directly on YouTube
- [ ] Block high-risk ads automatically
- [ ] Firefox support
- [ ] Safari support
- [ ] Cloud sync of captured URLs
- [ ] Reporting directly to YouTube

## Development

To modify the extension:

1. Edit the source files
2. Go to `chrome://extensions/`
3. Click reload icon on the extension
4. Test on YouTube

Files you might want to customize:
- `content.js` - Ad detection logic
- `popup.html/js` - UI customization
- `background.js` - Storage and API integration
