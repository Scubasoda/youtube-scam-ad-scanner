// YouTube Scam Ad Scanner - Content Scriptconsole.log("SIMPLE TEST - Content script loaded");

(function() {alert("Content script working!");

  'use strict';
  
  console.log('YouTube Scam Ad Scanner - Content script loaded!');
  
  const capturedAds = new Set();
  const DEBUG = true;

  function debugLog(...args) {
    if (DEBUG) {
      console.log('[YT Scam Scanner]', ...args);
    }
  }
  
  debugLog('Initializing scanner...');

  function cleanUrl(url) {
    if (!url) return null;
    
    if (url.includes('googleadservices.com') || url.includes('doubleclick.net')) {
      try {
        const urlObj = new URL(url);
        const adurl = urlObj.searchParams.get('adurl');
        if (adurl) return decodeURIComponent(adurl);
      } catch (e) {}
    }
    
    try {
      const urlObj = new URL(url);
      urlObj.searchParams.delete('utm_source');
      urlObj.searchParams.delete('utm_medium');
      urlObj.searchParams.delete('utm_campaign');
      return urlObj.toString();
    } catch (e) {
      return url;
    }
  }

  function extractAdUrl(element) {
    if (!element) return null;
    
    if (element.tagName === 'A' && element.href) {
      return cleanUrl(element.href);
    }
    
    const parentAnchor = element.closest('a[href]');
    if (parentAnchor && parentAnchor.href) {
      return cleanUrl(parentAnchor.href);
    }
    
    const childAnchor = element.querySelector('a[href]');
    if (childAnchor && childAnchor.href) {
      return cleanUrl(childAnchor.href);
    }
    
    const dataUrl = element.getAttribute('data-url') || 
                    element.getAttribute('href') ||
                    element.getAttribute('data-navigate-to') ||
                    element.getAttribute('data-navigation-url');
    if (dataUrl) return cleanUrl(dataUrl);
    
    return null;
  }

  function isAdElement(element) {
    if (!element) return false;
    
    const adIndicators = [
      'ad-showing', 'video-ads', 'ytp-ad', 'ad-container',
      'ad-text', 'visit-advertiser', 'videoAdUi',
      'ytp-ad-overlay', 'ytp-ad-text', 'ytp-ad-image',
      'ytp-ad-player-overlay', 'companion-ad'
    ];
    
    let currentElement = element;
    let depth = 0;
    
    while (currentElement && depth < 5) {
      const elementClasses = currentElement.className || '';
      const elementId = currentElement.id || '';
      
      if (adIndicators.some(indicator => 
        elementClasses.toString().includes(indicator) || 
        elementId.toString().includes(indicator)
      )) {
        return true;
      }
      
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

  function captureAdUrl(url) {
    if (!url) {
      debugLog('No URL to capture');
      return;
    }
    
    if (capturedAds.has(url)) {
      debugLog('URL already captured:', url);
      return;
    }
    
    if (url.includes('youtube.com') || url.includes('googlevideo.com')) {
      debugLog('Skipping YouTube internal URL:', url);
      return;
    }
    
    debugLog('CAPTURED AD URL:', url);
    capturedAds.add(url);
    
    // Send to background script for scanning
    chrome.runtime.sendMessage({
      type: 'AD_URL_CAPTURED',
      url: url,
      timestamp: Date.now()
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('Error sending message:', chrome.runtime.lastError);
      } else {
        debugLog('Message sent successfully:', response);
      }
    });
  }

  function setupClickMonitoring() {
    document.addEventListener('click', (event) => {
      const target = event.target;
      
      debugLog('Click detected on:', target.tagName, target.className);
      
      if (isAdElement(target)) {
        debugLog('Ad element clicked!');
        const url = extractAdUrl(target);
        if (url) {
          captureAdUrl(url);
        } else {
          debugLog('Could not extract URL from ad element');
        }
      }
      
      if (target.tagName === 'A' || target.closest('a')) {
        const link = target.tagName === 'A' ? target : target.closest('a');
        if (link.href && !link.href.includes('youtube.com') && !link.href.includes('googlevideo.com')) {
          debugLog('External link clicked:', link.href);
          const text = link.textContent.toLowerCase();
          if (text.includes('ad') || text.includes('sponsor') || isAdElement(link)) {
            captureAdUrl(cleanUrl(link.href));
          }
        }
      }
    }, true);
  }

  function monitorAdElements() {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (isAdElement(node)) {
              const url = extractAdUrl(node);
              if (url) {
                debugLog('Ad element detected in DOM:', url);
              }
            }
          }
        });
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  function monitorVideoPlayer() {
    const videoPlayer = document.querySelector('.html5-video-player');
    if (videoPlayer) {
      debugLog('Found video player, monitoring for ads...');
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          mutation.addedNodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE && isAdElement(node)) {
              const url = extractAdUrl(node);
              if (url) {
                debugLog('Video ad detected:', url);
                captureAdUrl(url);
              }
            }
          });
        });
      });
      
      observer.observe(videoPlayer, {
        childList: true,
        subtree: true
      });
    }
  }

  setupClickMonitoring();
  monitorAdElements();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', monitorVideoPlayer);
  } else {
    monitorVideoPlayer();
  }

  setTimeout(monitorVideoPlayer, 2000);

  debugLog('Monitoring started - click on ads to capture URLs!');

})();
