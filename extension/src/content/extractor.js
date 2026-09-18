const Extractor = {
  /**
   * Safely extract visible, high-relevance text chunks while filtering out navigation headers/footers
   */
  extractContent: () => {
    // Selectors to explicitly ignore (headers, navbars, menus, footers, scripts)
    const ignoredContainers = [
      'nav', 'header', 'footer', 'aside', 'noscript', 'script', 'style', 'svg',
      '.nav', '.navbar', '.header', '.footer', '.menu', '.breadcrumb', '.breadcrumbs',
      '.pagination', '.site-nav', '.navigation', '#header', '#footer', '#nav', '.desktop-nav',
      '.mobile-nav', '.header-nav'
    ].join(',');

    // Target elements that typically carry promotions, urgency, discounts, product details, alerts, and buttons
    const targetSelectors = [
      'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'button',
      '[role="alert"]', '[role="dialog"]', '.modal', '.popup', '.banner',
      '.offer', '.promo', '.discount', '.deal', '.timer', '.countdown',
      '.badge', '.alert', '.urgency', '.price-container', '.product-discount',
      '[class*="discount"]', '[class*="offer"]', '[class*="promo"]',
      '[class*="deal"]', '[class*="urgency"]', '[class*="timer"]', '[class*="banner"]',
      '[class*="badge"]', '[class*="coupon"]', '[class*="sale"]', '[class*="saving"]',
      'div.product-card', 'div.product-base', 'li.product-base', 'div[class*="product"]',
      'span', 'a'
    ].join(',');

    const candidateNodes = document.querySelectorAll(targetSelectors);
    const seenText = new Set();
    const candidateChunks = [];

    // Standalone menu & navigation terms to filter out
    const commonNavWords = new Set([
      'men', 'women', 'kids', 'home', 'beauty', 'studio', 'genz', 'profile', 'wishlist', 'bag',
      'cart', 'login', 'register', 'help', 'contact us', 'track orders', 'gift card',
      'myntra insider', 'all categories', 'terms of use', 'privacy policy', 'faq',
      'about us', 'careers', 'shipping', 'returns', 'cancellation', 'filter', 'sort by',
      'recommended', 'customer care', 'site map', 'search', 'search for products, brands and more'
    ]);

    candidateNodes.forEach(node => {
      // Ignore if inside navigation / footer / header
      if (node.closest(ignoredContainers)) {
        return;
      }

      // Filter hidden elements
      const style = window.getComputedStyle(node);
      if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
        return;
      }

      // Avoid large layout wrapper containers with many child elements
      if (node.children.length > 3 && !node.classList.contains('banner') && !node.classList.contains('offer')) {
        return;
      }

      const text = (node.innerText || node.textContent || '').trim();
      if (!text || text.length < 4 || text.length > 400) return;

      const lower = text.toLowerCase();
      const sanitized = lower.replace(/[^a-z0-9 ]/g, '').trim();

      // Skip standalone navigation items
      if (commonNavWords.has(lower) || commonNavWords.has(sanitized)) {
        return;
      }

      if (!seenText.has(lower)) {
        seenText.add(lower);
        candidateChunks.push(text);
      }
    });

    // Also look specifically for discount & urgency regex patterns in the body text
    const discountRegex = /\b(\d+%\s*off|save\s*(?:rs\.?|\$|₹)?\s*\d+|only\s*\d+\s*left|sale\s*ends|hurry|limited\s*time|exclusive\s*deal|expires\s*in|claim\s*now)\b/gi;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let textNode;
    while ((textNode = walker.nextNode()) && candidateChunks.length < 100) {
      if (textNode.parentNode && textNode.parentNode.closest(ignoredContainers)) continue;
      const val = textNode.nodeValue?.trim();
      if (val && discountRegex.test(val) && val.length > 3 && val.length < 200) {
        const valLower = val.toLowerCase();
        if (!seenText.has(valLower)) {
          seenText.add(valLower);
          candidateChunks.push(val);
        }
      }
    }

    let fullText = candidateChunks.join('\n');
    
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
    } else if (document.querySelector('.price, [itemprop="price"], [class*="price"], [class*="discount"]')) {
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
