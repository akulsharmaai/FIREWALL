/**
 * Wrapper for sending messages safely between extension components
 */

const MessageBus = {
  // Send message from Popup/Content to Service Worker
  sendToBackground: (type, payload = {}) => {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage({ type, payload }, (response) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve(response);
        }
      });
    });
  },

  // Send message from Service Worker to specific Content Script
  sendToTab: (tabId, type, payload = {}) => {
    return new Promise((resolve, reject) => {
      chrome.tabs.sendMessage(tabId, { type, payload }, (response) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve(response);
        }
      });
    });
  }
};
