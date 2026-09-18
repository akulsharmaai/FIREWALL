// Listen for messages from popup or background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === MESSAGES.SCAN_CURRENT_PAGE) {
    console.log("Human Firewall: Extracting page content...");
    const payload = Extractor.extractContent();
    
    // Send to background for analysis
    MessageBus.sendToBackground(MESSAGES.ANALYZE_PAGE, payload)
      .then(response => sendResponse(response))
      .catch(err => sendResponse({ success: false, error: err.message }));
      
    return true; // Keep channel open
  }
  
  if (message.type === MESSAGES.ANALYSIS_RESULT) {
    handleAnalysisResult(message.payload);
  }
});

function handleAnalysisResult(result) {
  if (result && result.success && result.analysis && result.analysis.manipulation_detected) {
    console.log("Human Firewall: Manipulation detected!", result.analysis.technique);
    
    // Highlight evidence in DOM
    if (result.analysis.evidence && result.analysis.evidence.length > 0) {
      Highlighter.highlightEvidence(result.analysis.evidence);
    }
    
    // Show non-intrusive badge
    Highlighter.injectBadge(result);
  }
}
