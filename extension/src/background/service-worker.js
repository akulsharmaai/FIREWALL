importScripts('../utils/constants.js', '../utils/messaging.js', '../api/api-client.js');

// Simple cache to prevent duplicate requests on the same URL
const resultCache = new Map();

// Service Worker Message Listener
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === MESSAGES.SCAN_CURRENT_PAGE) {
    handleManualScan(sendResponse);
    return true; // Keep channel open for async response
  } 
  
  if (message.type === MESSAGES.ANALYZE_PAGE) {
    handlePageAnalysis(message.payload, sender.tab.id)
      .then(result => sendResponse(result))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (message.type === MESSAGES.GET_CURRENT_RESULT) {
    handleGetCurrentResult(sendResponse);
    return true;
  }
});

async function handleManualScan(sendResponse) {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab) {
      sendResponse({ success: false, error: 'No active tab found.' });
      return;
    }

    if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://')) {
      sendResponse({ success: false, error: 'Human Firewall cannot analyze browser internal pages.' });
      return;
    }

    // Trigger extraction in the content script
    const result = await MessageBus.sendToTab(tab.id, MESSAGES.SCAN_CURRENT_PAGE);
    sendResponse(result);
  } catch (error) {
    console.error('Scan error:', error);
    sendResponse({ success: false, error: 'Failed to communicate with the page. Try refreshing.' });
  }
}

async function handlePageAnalysis(payload, tabId) {
  const url = payload.page_url;
  
  // Deduplication check
  if (resultCache.has(url)) {
    const cached = resultCache.get(url);
    if (Date.now() - cached.timestamp < 5 * 60 * 1000) { // 5 minutes cache
      return cached.data;
    }
  }

  try {
    const result = await ApiClient.analyzePage(payload);
    
    // Cache the result
    resultCache.set(url, { timestamp: Date.now(), data: result });
    
    // Broadcast result back to the specific tab
    MessageBus.sendToTab(tabId, MESSAGES.ANALYSIS_RESULT, result).catch(e => console.log('Tab closed or unavailable', e));
    
    return result;
  } catch (error) {
    console.error("API Error:", error);
    return { 
      success: false, 
      error: error.message || 'Failed to connect to backend.'
    };
  }
}

async function handleGetCurrentResult(sendResponse) {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!tab) return sendResponse({ success: false });

    if (resultCache.has(tab.url)) {
      sendResponse(resultCache.get(tab.url).data);
    } else {
      sendResponse({ success: false, message: 'No cached result for this page.' });
    }
  } catch (e) {
    sendResponse({ success: false });
  }
}
