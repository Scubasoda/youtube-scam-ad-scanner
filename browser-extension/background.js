/**
 * Background service worker
 * Handles captured ad URLs and coordinates scanning
 */

console.log('YouTube Scam Ad Scanner - Background service worker loaded');

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'AD_URL_CAPTURED') {
    console.log('Background: Ad URL captured:', message.url);
    
    // Store the URL
    storeAdUrl(message.url, message.timestamp, message.pageUrl);
    
    // Show notification (optional)
    showNotification('Ad URL Captured', `Captured: ${message.url}`);
    
    // Update badge
    updateBadgeCount();
    
    sendResponse({ success: true });
  }
  
  if (message.type === 'SCAN_URL') {
    // This would trigger scanning via the Python backend
    scanUrl(message.url).then(result => {
      sendResponse(result);
    });
    return true; // Keep channel open for async response
  }
  
  if (message.type === 'GET_CAPTURED_ADS') {
    chrome.storage.local.get(['capturedAds'], (result) => {
      sendResponse({ ads: result.capturedAds || [] });
    });
    return true;
  }
});

/**
 * Store captured ad URL and optionally auto-scan
 */
function storeAdUrl(url, timestamp, pageUrl) {
  chrome.storage.local.get(['capturedAds'], (result) => {
    const ads = result.capturedAds || [];
    
    // Check if URL already exists
    const exists = ads.some(ad => ad.url === url);
    if (!exists) {
      const newAd = {
        url: url,
        timestamp: timestamp,
        pageUrl: pageUrl,
        scanned: false,
        scanResult: null
      };
      
      ads.push(newAd);
      chrome.storage.local.set({ capturedAds: ads });
      console.log('Stored ad URL:', url);
      
      // Auto-scan if enabled
      autoScanIfEnabled(url, { pageUrl: pageUrl, capturedAt: timestamp });
    }
  });
}

/**
 * Update extension badge with count of captured ads
 */
function updateBadgeCount() {
  chrome.storage.local.get(['capturedAds'], (result) => {
    const ads = result.capturedAds || [];
    const unscannedCount = ads.filter(ad => !ad.scanned).length;
    
    if (unscannedCount > 0) {
      chrome.action.setBadgeText({ text: unscannedCount.toString() });
      chrome.action.setBadgeBackgroundColor({ color: '#FF0000' });
    } else {
      chrome.action.setBadgeText({ text: '' });
    }
  });
}

/**
 * Show notification to user
 */
function showNotification(title, message) {
  // Only show if user has enabled notifications
  chrome.storage.sync.get(['showNotifications'], (result) => {
    if (result.showNotifications !== false) {
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: title,
        message: message,
        priority: 1
      });
    }
  });
}

/**
 * Scan URL using local Python scanner API
 * Requires api_server.py to be running
 */
async function scanUrl(url, metadata = {}) {
  try {
    // Call local API server
    const response = await fetch('http://localhost:5000/scan', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        url: url,
        source: 'browser-extension',
        metadata: metadata
      })
    });
    
    if (response.ok) {
      const result = await response.json();
      
      // Update the stored ad with scan results
      chrome.storage.local.get(['capturedAds'], (data) => {
        const ads = data.capturedAds || [];
        const adIndex = ads.findIndex(ad => ad.url === url);
        
        if (adIndex !== -1) {
          ads[adIndex].scanned = true;
          ads[adIndex].scanResult = result;
          ads[adIndex].scannedAt = new Date().toISOString();
          chrome.storage.local.set({ capturedAds: ads });
          updateBadgeCount();
        }
      });
      
      // Show notification for high risk
      if (result.risk_level === 'HIGH') {
        showNotification(
          '⚠️ HIGH RISK AD DETECTED',
          `Scam indicators found in: ${url.substring(0, 50)}...`
        );
      }
      
      return result;
    } else {
      throw new Error(`API returned ${response.status}`);
    }
  } catch (error) {
    console.error('Error scanning URL:', error);
    
    // Return error with instructions
    return {
      error: 'Local scanner API not running',
      message: 'Start the API server with: python api_server.py',
      url: url,
      instructions: [
        '1. Open terminal in project directory',
        '2. Run: python api_server.py',
        '3. Keep it running while browsing YouTube'
      ]
    };
  }
}

/**
 * Auto-scan URL if API is available
 */
async function autoScanIfEnabled(url, metadata) {
  chrome.storage.sync.get(['autoScan'], async (result) => {
    if (result.autoScan !== false) {  // Default to true
      try {
        await scanUrl(url, metadata);
      } catch (error) {
        console.log('Auto-scan failed, URL will remain unscanned');
      }
    }
  });
}

// Monitor web requests for ad URLs
chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    // Capture ad-related requests
    if (details.url.includes('doubleclick.net') || 
        details.url.includes('googleadservices.com')) {
      
      console.log('Ad request detected:', details.url);
      
      // Try to extract the destination URL from parameters
      const urlParams = new URL(details.url).searchParams;
      const adUrl = urlParams.get('adurl') || urlParams.get('url');
      
      if (adUrl) {
        storeAdUrl(decodeURIComponent(adUrl), Date.now(), details.url);
        updateBadgeCount();
      }
    }
  },
  { urls: ["<all_urls>"] }
);

// Initialize badge count on startup
updateBadgeCount();
