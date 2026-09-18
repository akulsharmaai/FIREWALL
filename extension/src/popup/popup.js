document.addEventListener('DOMContentLoaded', () => {
  const scanBtn = document.getElementById('scan-btn');
  const statusText = document.getElementById('status-text');
  
  // UI Containers
  const resultContainer = document.getElementById('result-container');
  const errorContainer = document.getElementById('error-container');
  const errorText = document.getElementById('error-text');
  
  // Elements
  const banner = document.getElementById('manipulation-banner');
  const techniqueEl = document.getElementById('res-technique');
  const confidenceEl = document.getElementById('res-confidence');
  const severityEl = document.getElementById('res-severity');
  const evidenceEl = document.getElementById('res-evidence');
  const explanationEl = document.getElementById('res-explanation');
  const targetingSection = document.getElementById('targeting-section');
  const targetingSignalsEl = document.getElementById('res-targeting-signals');

  // Initial Check for cached results
  MessageBus.sendToBackground(MESSAGES.GET_CURRENT_RESULT)
    .then(result => {
      if (result && result.success) {
        displayResult(result);
      }
    });

  // Test Lab UI Logic
  const testLabToggle = document.getElementById('test-lab-toggle');
  const testLabMenu = document.getElementById('test-lab-menu');
  
  if (testLabToggle && testLabMenu) {
    testLabToggle.addEventListener('click', () => {
      testLabMenu.classList.toggle('hidden');
    });

    document.querySelectorAll('.test-btn').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const targetId = e.target.getAttribute('data-target');
        
        // Execute a small script in the active tab to scroll to the element
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (tab) {
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: (id) => {
              const el = document.getElementById(id);
              if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
              }
            },
            args: [targetId]
          });
        }
      });
    });
  }

  scanBtn.addEventListener('click', async () => {
    setLoadingState();
    
    try {
      const response = await MessageBus.sendToBackground(MESSAGES.SCAN_CURRENT_PAGE);
      if (response && response.success === false) {
        throw new Error(response.error);
      }
      
      displayResult(response);
    } catch (error) {
      showError(error.message || 'An unexpected error occurred.');
    }
  });

  function setLoadingState() {
    scanBtn.disabled = true;
    scanBtn.textContent = 'Scanning...';
    statusText.textContent = 'Analyzing webpage...';
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
  }

  function displayResult(result) {
    scanBtn.disabled = false;
    scanBtn.textContent = 'Scan Current Page';
    statusText.textContent = 'Analysis complete.';
    resultContainer.classList.remove('hidden');
    errorContainer.classList.add('hidden');

    if (!result || !result.analysis) {
      showError('Invalid response from backend.');
      return;
    }

    const { analysis, targeting } = result;

    if (analysis.manipulation_detected) {
      banner.textContent = 'Potential manipulation detected';
      banner.className = 'banner';
      
      techniqueEl.textContent = analysis.technique || 'Unknown';
      confidenceEl.textContent = analysis.confidence ? `${Math.round(analysis.confidence * 100)}%` : 'N/A';
      severityEl.textContent = analysis.severity || 'Medium';
      
      evidenceEl.innerHTML = '';
      if (analysis.evidence && analysis.evidence.length > 0) {
        analysis.evidence.forEach(ev => {
          const p = document.createElement('div');
          p.textContent = `"${ev}"`;
          evidenceEl.appendChild(p);
        });
      } else {
        evidenceEl.textContent = 'No explicit evidence extracted.';
      }
      
      explanationEl.textContent = analysis.explanation || 'No explanation provided.';

      if (targeting && targeting.available && targeting.possible_signals.length > 0) {
        targetingSection.classList.remove('hidden');
        targetingSignalsEl.innerHTML = targeting.possible_signals.map(s => `<li>${s}</li>`).join('');
      } else {
        targetingSection.classList.add('hidden');
      }
    } else {
      // Safe page
      banner.textContent = 'No manipulation detected';
      banner.className = 'banner safe';
      techniqueEl.textContent = '-';
      confidenceEl.textContent = '-';
      severityEl.textContent = '-';
      evidenceEl.textContent = '-';
      explanationEl.textContent = 'The content appears to be straightforward and non-manipulative.';
      targetingSection.classList.add('hidden');
    }
  }

  function showError(message) {
    scanBtn.disabled = false;
    scanBtn.textContent = 'Scan Current Page';
    statusText.textContent = 'Scan failed.';
    resultContainer.classList.add('hidden');
    errorContainer.classList.remove('hidden');
    errorText.textContent = message;
  }
});
