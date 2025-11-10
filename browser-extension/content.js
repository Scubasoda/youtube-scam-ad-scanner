/**
 * Content script that runs on YouTube pages
 * Captures ad URLs when users interact with ads
 */

console.log('YouTube Scam Ad Scanner - Content script loaded');

// Track captured ad URLs
const capturedAds = new Set();

// Debug mode - log everything
const DEBUG = true;

function debugLog(...args) {
  if (DEBUG) {
    console.log('[YT Scam Scanner]', ...args);
  }
}

/**
 * Extract URL from YouTube ad elements
 */
function extractAdUrl(element) {
  if (!element) return null;
  
  // YouTube ads have various structures, check multiple possibilities
  
  // 1. Check for direct href in anchor tags
  if (element.tagName === 'A' && element.href) {
    return cleanUrl(element.href);
  }
  
  // 2. Check parent and child anchor tags
  const parentAnchor = element.closest('a[href]');
  if (parentAnchor && parentAnchor.href) {
    return cleanUrl(parentAnchor.href);
  }
  
  const childAnchor = element.querySelector('a[href]');
  if (childAnchor && childAnchor.href) {
    return cleanUrl(childAnchor.href);
  }
  
  // 3. Check data attributes
  const dataUrl = element.getAttribute('data-url') || 
                  element.getAttribute('href') ||
                  element.getAttribute('data-navigate-to') ||
                  element.getAttribute('data-navigation-url');
  if (dataUrl) {
    return cleanUrl(dataUrl);
  }
  
  // 4. Look for URLs in onclick attributes
  const onclick = element.getAttribute('onclick');
  if (onclick) {
    const urlMatch = onclick.match(/https?:\/\/[^\s"']+/);
    if (urlMatch) {
      return cleanUrl(urlMatch[0]);
    }
  }
  
  return null;
}

/**
 * Clean and validate URL
 */
function cleanUrl(url) {
  if (!url) return null;
  
  // Remove Google redirect wrappers
  if (url.includes('googleadservices.com') || url.includes('doubleclick.net')) {
    try {
      const urlObj = new URL(url);
      const adurl = urlObj.searchParams.get('adurl');
      if (adurl) {
        return decodeURIComponent(adurl);
      }
    } catch (e) {
      // Invalid URL, continue
    }
  }
  
  // Clean the URL
  try {
    const urlObj = new URL(url);
    // Remove tracking parameters
    urlObj.searchParams.delete('utm_source');
    urlObj.searchParams.delete('utm_medium');
    urlObj.searchParams.delete('utm_campaign');
    return urlObj.toString();
  } catch (e) {
    return url; // Return as-is if can't parse
  }
}

/**
 * Check if element is likely an ad
 */
function isAdElement(element) {
  if (!element) return false;
  
  // Check for common ad indicators in class names
  const adIndicators = [
    'ad-showing',
    'video-ads',
    'ytp-ad',
    'ad-container',
    'ad-text',
    'visit-advertiser',
    'videoAdUi',
    'ytp-ad-overlay',
    'ytp-ad-text',
    'ytp-ad-image',
    'ytp-ad-player-overlay',
    'video-ads',
    'companion-ad'
  ];
  
  // Get all classes from element and parents
  let currentElement = element;
  let depth = 0;
  
  while (currentElement && depth < 5) {
    const elementClasses = currentElement.className || '';
    const elementId = currentElement.id || '';
    
    // Check classes
    if (adIndicators.some(indicator => 
      elementClasses.toString().includes(indicator) || 
      elementId.toString().includes(indicator)
    )) {
      return true;
    }
    
    // Check for data attributes
    const dataAttrs = Array.from(currentElement.attributes || [])
      .filter(attr => attr.name.startsWith('data-'))
      .map(attr => attr.value.toLowerCase())
      .join(' ');
    
    if (dataAttrs.includes('ad') || dataAttrs.includes('advertis')) {
      return true;
    }
    
    currentElement = currentElement.parentElement;
    depth++;
  }
  
  return false;
}

/**
 * Capture ad URL and send to background script
 */
function captureAdUrl(url) {
  if (!url) {
    debugLog('No URL to capture');
    return;
  }
  
  if (capturedAds.has(url)) {
    debugLog('URL already captured:', url);
    return; // Already captured
  }
  
  // Filter out YouTube internal URLs
  if (url.includes('youtube.com') || url.includes('googlevideo.com')) {
    debugLog('Skipping YouTube internal URL:', url);
    return;
  }
  
  debugLog('✅ Captured ad URL:', url);
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
    
    debugLog('Click detected on:', target.tagName, target.className);
    
    // Check if clicked element is or contains an ad
    if (isAdElement(target)) {
      debugLog('Ad element clicked!');
      const url = extractAdUrl(target);
      if (url) {
        captureAdUrl(url);
      } else {
        debugLog('Could not extract URL from ad element');
      }
    }
    
    // Also check all links clicked (catch-all)
    if (target.tagName === 'A' || target.closest('a')) {
      const link = target.tagName === 'A' ? target : target.closest('a');
      if (link.href && !link.href.includes('youtube.com') && !link.href.includes('googlevideo.com')) {
        debugLog('External link clicked:', link.href);
        // Check if it might be an ad
        const text = link.textContent.toLowerCase();
        if (text.includes('ad') || text.includes('sponsor') || isAdElement(link)) {
          captureAdUrl(cleanUrl(link.href));
        }
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
