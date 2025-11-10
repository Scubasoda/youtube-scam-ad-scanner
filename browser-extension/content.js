/**
 * Content script that runs on YouTube pages
 * Captures ad URLs when users interact with ads
 */

console.log('YouTube Scam Ad Scanner - Content script loaded');

// Track captured ad URLs
const capturedAds = new Set();

/**
 * Extract URL from YouTube ad elements
 */
function extractAdUrl(element) {
  // YouTube ads have various structures, check multiple possibilities
  
  // 1. Check for direct href in anchor tags
  if (element.tagName === 'A' && element.href) {
    return element.href;
  }
  
  // 2. Check parent anchor tags
  const parentAnchor = element.closest('a');
  if (parentAnchor && parentAnchor.href) {
    return parentAnchor.href;
  }
  
  // 3. Check data attributes
  const dataUrl = element.getAttribute('data-url') || 
                  element.getAttribute('href') ||
                  element.getAttribute('data-navigate-to');
  if (dataUrl) {
    return dataUrl;
  }
  
  return null;
}

/**
 * Check if element is likely an ad
 */
function isAdElement(element) {
  // Check for common ad indicators
  const adIndicators = [
    'ad-showing',
    'video-ads',
    'ytp-ad',
    'ad-container',
    'ad-text',
    'visit-advertiser',
    'videoAdUi'
  ];
  
  // Check element and parent classes
  const elementClasses = element.className || '';
  const parentClasses = element.parentElement?.className || '';
  
  return adIndicators.some(indicator => 
    elementClasses.includes(indicator) || 
    parentClasses.includes(indicator)
  );
}

/**
 * Capture ad URL and send to background script
 */
function captureAdUrl(url) {
  if (!url || capturedAds.has(url)) {
    return; // Already captured or invalid
  }
  
  // Filter out YouTube internal URLs
  if (url.includes('youtube.com') || url.includes('googlevideo.com')) {
    return;
  }
  
  console.log('Captured ad URL:', url);
  capturedAds.add(url);
  
  // Send to background script
  chrome.runtime.sendMessage({
    type: 'AD_URL_CAPTURED',
    url: url,
    timestamp: Date.now(),
    pageUrl: window.location.href
  });
  
  // Also store locally
  chrome.storage.local.get(['capturedAds'], (result) => {
    const ads = result.capturedAds || [];
    ads.push({
      url: url,
      timestamp: Date.now(),
      pageUrl: window.location.href,
      scanned: false
    });
    
    chrome.storage.local.set({ capturedAds: ads });
  });
}

/**
 * Monitor clicks on potential ad elements
 */
function setupClickMonitoring() {
  document.addEventListener('click', (event) => {
    const target = event.target;
    
    // Check if clicked element is or contains an ad
    if (isAdElement(target)) {
      const url = extractAdUrl(target);
      if (url) {
        captureAdUrl(url);
      }
    }
  }, true); // Use capture phase to catch before navigation
}

/**
 * Monitor for "Skip Ad" buttons and ad overlays
 */
function monitorAdElements() {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) { // Element node
          // Look for ad-related elements
          if (isAdElement(node)) {
            // Try to extract URL from any links within
            const links = node.querySelectorAll('a[href]');
            links.forEach((link) => {
              const url = link.href;
              if (url && !url.includes('youtube.com')) {
                captureAdUrl(url);
              }
            });
          }
        }
      });
    });
  });
  
  // Observe the entire document for ad insertions
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}

/**
 * Monitor video player for ad indicators
 */
function monitorVideoPlayer() {
  // Look for the video player
  const videoPlayer = document.querySelector('.html5-video-player');
  
  if (videoPlayer) {
    // Monitor for ad-specific UI elements
    const adObserver = new MutationObserver(() => {
      // Check if ad is currently playing
      const adShowing = videoPlayer.classList.contains('ad-showing') ||
                       videoPlayer.classList.contains('ad-interrupting');
      
      if (adShowing) {
        // Look for "Visit Advertiser" or similar links
        const adLinks = videoPlayer.querySelectorAll('.ytp-ad-visit-advertiser-button, .ytp-ad-button');
        adLinks.forEach((link) => {
          const url = link.getAttribute('href') || link.getAttribute('data-url');
          if (url) {
            captureAdUrl(url);
          }
        });
      }
    });
    
    adObserver.observe(videoPlayer, {
      attributes: true,
      attributeFilter: ['class'],
      subtree: true
    });
  }
}

// Initialize monitoring
setupClickMonitoring();
monitorAdElements();

// Wait for page to load, then monitor video player
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', monitorVideoPlayer);
} else {
  monitorVideoPlayer();
}

// Retry monitoring video player after a delay (in case it loads late)
setTimeout(monitorVideoPlayer, 2000);

console.log('YouTube Scam Ad Scanner - Monitoring started');
