const Highlighter = {
  /**
   * Attempt to find and highlight evidence in the DOM safely
   */
  highlightEvidence: (evidenceList) => {
    if (!evidenceList || evidenceList.length === 0) return;

    // We use treeWalker to find text nodes containing the evidence
    evidenceList.forEach(evidenceStr => {
      const trimmedEvidence = evidenceStr.trim();
      if (trimmedEvidence.length < 5) return; // Ignore very short generic words

      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
      let node;
      
      while (node = walker.nextNode()) {
        if (node.nodeValue.includes(trimmedEvidence)) {
          // Verify it's not inside a script/style tag
          if (['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(node.parentNode.nodeName)) continue;
          
          try {
            // Replace the text node with a highlighted span
            const span = document.createElement('span');
            span.className = 'hf-highlighted-evidence';
            span.style.backgroundColor = 'rgba(255, 193, 7, 0.4)';
            span.style.borderBottom = '2px solid #ff9800';
            span.style.cursor = 'help';
            span.title = 'Human Firewall: Potential manipulation detected here.';
            
            // Text splitting to just wrap the matched part
            const index = node.nodeValue.indexOf(trimmedEvidence);
            const before = node.nodeValue.substring(0, index);
            const after = node.nodeValue.substring(index + trimmedEvidence.length);
            
            span.textContent = trimmedEvidence;
            
            const parent = node.parentNode;
            parent.insertBefore(document.createTextNode(before), node);
            parent.insertBefore(span, node);
            parent.insertBefore(document.createTextNode(after), node);
            parent.removeChild(node);
          } catch(e) {
            console.warn("Human Firewall: Failed to highlight a node safely.");
          }
          break; // Highlight only the first occurrence to avoid messing up DOM too much
        }
      }
    });
  },
  
  injectBadge: (result) => {
    // Inject a non-intrusive badge into the corner
    let container = document.getElementById('hf-overlay-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'hf-overlay-container';
      document.body.appendChild(container);
      
      // Use Shadow DOM to protect CSS
      const shadow = container.attachShadow({mode: 'open'});
      
      const style = document.createElement('style');
      style.textContent = `
        .hf-badge {
          position: fixed;
          bottom: 20px;
          right: 20px;
          background: #1f2937;
          color: white;
          padding: 12px 16px;
          border-radius: 8px;
          font-family: system-ui, sans-serif;
          z-index: 2147483647;
          box-shadow: 0 4px 12px rgba(0,0,0,0.15);
          display: flex;
          align-items: center;
          gap: 12px;
          border-left: 4px solid #ef4444;
          font-size: 14px;
          cursor: pointer;
        }
        .hf-badge:hover {
          transform: translateY(-2px);
          transition: transform 0.2s;
        }
        .hf-icon { font-size: 18px; }
        .hf-close { margin-left: 10px; opacity: 0.7; }
        .hf-close:hover { opacity: 1; }
      `;
      shadow.appendChild(style);
      
      const badge = document.createElement('div');
      badge.className = 'hf-badge';
      
      const analysis = result.analysis;
      badge.innerHTML = `
        <span class="hf-icon">🛡️</span>
        <div>
          <strong>${analysis.technique}</strong><br>
          <span style="opacity:0.8; font-size: 12px;">Confidence: ${Math.round(analysis.confidence * 100)}%</span>
        </div>
        <span class="hf-close" title="Dismiss">✕</span>
      `;
      
      badge.querySelector('.hf-close').addEventListener('click', (e) => {
        e.stopPropagation();
        container.remove();
      });
      
      shadow.appendChild(badge);
    }
  }
};
