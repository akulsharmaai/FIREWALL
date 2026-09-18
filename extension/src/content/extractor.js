const Extractor = {
  /**
   * Safely extract visible text from the webpage
   */
  extractContent: () => {
    // Avoid sensitive fields
    const sensitiveSelectors = 'input[type="password"], input[name*="card"], input[name*="cvv"]';
    if (document.querySelector(sensitiveSelectors)) {
      // Exclude values explicitly, though we focus on innerText of block elements
    }

    // Collect readable text from likely content nodes
    const contentNodes = document.querySelectorAll('h1, h2, h3, h4, p, button, a, span, div.offer, div.promo, div.alert');
    let textArray = [];
    
    // Set to avoid duplicates
    const seenText = new Set();

    contentNodes.forEach(node => {
      // Filter out hidden elements
      const style = window.getComputedStyle(node);
      if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
        return;
      }

      // Simple heuristic to avoid grabbing massive layout divs
      if (node.tagName.toLowerCase() === 'div' && node.children.length > 2) {
        return;
      }

      const text = node.innerText?.trim();
      if (text && text.length > 3 && !seenText.has(text)) {
        seenText.add(text);
        textArray.push(text);
      }
    });

    let fullText = textArray.join(' \n');
    
    // Truncate to avoid overloading backend
    if (fullText.length > CONFIG.MAX_TEXT_LENGTH) {
      fullText = fullText.substring(0, CONFIG.MAX_TEXT_LENGTH);
    }

    // Determine basic content type
    let contentType = 'general';
    const title = document.title.toLowerCase();
    if (title.includes('checkout') || title.includes('cart')) {
      contentType = 'checkout';
    } else if (title.includes('book') || title.includes('flight') || title.includes('hotel')) {
      contentType = 'booking';
    } else if (document.querySelector('.price, [itemprop="price"]')) {
      contentType = 'product';
    }

    return {
      text: fullText,
      page_url: window.location.href,
      page_title: document.title,
      page_domain: window.location.hostname,
      content_type: contentType
    };
  }
};
