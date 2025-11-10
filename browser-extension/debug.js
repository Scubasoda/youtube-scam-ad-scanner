/**
 * Debug script - inject this in console to test ad detection
 * Copy and paste this entire script into the browser console on YouTube
 */

console.log('🔍 Starting YouTube Ad Scanner Debug...');

// Test 1: Check if content script is loaded
console.log('Test 1: Checking content script...');
if (typeof capturedAds !== 'undefined') {
  console.log('✅ Content script is loaded');
  console.log('Captured ads so far:', capturedAds.size);
} else {
  console.log('❌ Content script NOT loaded - extension may not be active');
}

// Test 2: Find all links on the page
console.log('\nTest 2: Scanning all links on page...');
const allLinks = document.querySelectorAll('a[href]');
console.log(`Found ${allLinks.length} total links`);

// Test 3: Find potential ad elements
console.log('\nTest 3: Looking for ad-related elements...');
const adSelectors = [
  '.ad-showing',
  '.video-ads',
  '.ytp-ad-overlay',
  '.ytp-ad-text',
  '[class*="ad-"]',
  '[class*="Ad"]',
  '[id*="ad-"]',
  '.ytp-ad-player-overlay',
  'ytd-display-ad-renderer',
  'ytd-video-masthead-ad',
  'ytd-in-feed-ad-layout-renderer'
];

adSelectors.forEach(selector => {
  const elements = document.querySelectorAll(selector);
  if (elements.length > 0) {
    console.log(`✅ Found ${elements.length} elements matching: ${selector}`);
    elements.forEach((el, i) => {
      if (i < 3) { // Show first 3
        const link = el.querySelector('a[href]') || el.closest('a[href]');
        if (link) {
          console.log(`  → Link ${i+1}:`, link.href);
        }
      }
    });
  }
});

// Test 4: Monitor next click
console.log('\nTest 4: Click monitoring setup...');
let clickMonitor = null;
clickMonitor = function(event) {
  const target = event.target;
  console.log('🖱️ CLICK DETECTED:');
  console.log('  Tag:', target.tagName);
  console.log('  Class:', target.className);
  console.log('  ID:', target.id);
  
  // Check if it's a link
  const link = target.tagName === 'A' ? target : target.closest('a');
  if (link) {
    console.log('  Link URL:', link.href);
    console.log('  Link text:', link.textContent.trim().substring(0, 50));
  }
  
  // Check parent classes
  let parent = target.parentElement;
  let depth = 0;
  while (parent && depth < 5) {
    console.log(`  Parent ${depth+1}:`, parent.tagName, parent.className);
    depth++;
    parent = parent.parentElement;
  }
};

document.addEventListener('click', clickMonitor, true);
console.log('✅ Click monitor active - click anything and watch the console!');

console.log('\n📊 Debug Complete! Now:');
console.log('1. If content script is NOT loaded, reload the page');
console.log('2. Look for any ad elements listed above');
console.log('3. Click on an ad and watch the console output');
console.log('4. Check if the URL gets captured');
