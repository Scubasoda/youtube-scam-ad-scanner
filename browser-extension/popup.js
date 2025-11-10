/**
 * Popup UI logic
 */

// Load and display captured ads
function loadCapturedAds() {
  chrome.storage.local.get(['capturedAds'], (result) => {
    const ads = result.capturedAds || [];
    
    // Update stats
    document.getElementById('totalCount').textContent = ads.length;
    document.getElementById('unscannedCount').textContent = 
      ads.filter(ad => !ad.scanned).length;
    document.getElementById('highRiskCount').textContent = 
      ads.filter(ad => ad.scanResult?.risk_level === 'HIGH').length;
    
    // Display ad list
    const adList = document.getElementById('adList');
    
    if (ads.length === 0) {
      adList.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">📭</div>
          <p>No ad URLs captured yet.</p>
          <p style="font-size: 12px;">Browse YouTube and the extension will automatically capture ad URLs.</p>
        </div>
      `;
      return;
    }
    
    // Sort by timestamp (newest first)
    ads.sort((a, b) => b.timestamp - a.timestamp);
    
    adList.innerHTML = ads.map(ad => {
      const date = new Date(ad.timestamp).toLocaleString();
      const riskLevel = ad.scanResult?.risk_level || 'unknown';
      const riskClass = `risk-${riskLevel.toLowerCase()}`;
      const riskText = ad.scanned ? riskLevel : 'NOT SCANNED';
      
      return `
        <div class="ad-item">
          <div class="ad-url">${escapeHtml(ad.url)}</div>
          <div class="ad-meta">
            ${date}
            <span class="risk-badge ${riskClass}">${riskText}</span>
          </div>
        </div>
      `;
    }).join('');
  });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Export URLs to text file
function exportUrls() {
  chrome.storage.local.get(['capturedAds'], (result) => {
    const ads = result.capturedAds || [];
    
    if (ads.length === 0) {
      alert('No URLs to export');
      return;
    }
    
    // Create text content
    const content = ads.map(ad => {
      const date = new Date(ad.timestamp).toLocaleString();
      const risk = ad.scanResult ? ` (${ad.scanResult.risk_level})` : ' (UNSCANNED)';
      return `${ad.url}${risk} - ${date}`;
    }).join('\n');
    
    // Download as file
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `youtube-ad-urls-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  });
}

// Clear all captured ads
function clearAll() {
  if (confirm('Are you sure you want to clear all captured ad URLs?')) {
    chrome.storage.local.set({ capturedAds: [] }, () => {
      loadCapturedAds();
      chrome.action.setBadgeText({ text: '' });
    });
  }
}

// Scan all unscanned URLs
function scanAll() {
  chrome.storage.local.get(['capturedAds'], (result) => {
    const ads = result.capturedAds || [];
    const unscanned = ads.filter(ad => !ad.scanned);
    
    if (unscanned.length === 0) {
      alert('No unscanned URLs');
      return;
    }
    
    // Create text with URLs for manual scanning
    const urls = unscanned.map(ad => ad.url).join('\n');
    
    // Copy to clipboard
    navigator.clipboard.writeText(urls).then(() => {
      alert(`${unscanned.length} URLs copied to clipboard!\n\nYou can now scan them with:\npython test_batch.py\n\nOr scan individually:\npython -m src.scanner --url "URL"`);
    });
  });
}

// Event listeners
document.getElementById('exportBtn').addEventListener('click', exportUrls);
document.getElementById('clearBtn').addEventListener('click', clearAll);
document.getElementById('scanAllBtn').addEventListener('click', scanAll);

// Load ads on popup open
loadCapturedAds();

// Refresh every 2 seconds while popup is open
setInterval(loadCapturedAds, 2000);
