const ApiClient = {
  /**
   * Send analysis request to backend
   */
  analyzePage: async (payload) => {
    const endpoint = `${CONFIG.API_BASE_URL}/api/v1/analyze`;
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        let errorMsg = 'Failed to analyze page.';
        try {
          const errData = await response.json();
          errorMsg = errData?.error?.message || errorMsg;
        } catch(e) {}
        throw new Error(`Error ${response.status}: ${errorMsg}`);
      }
      
      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Analysis request timed out. Backend might be down.');
      }
      throw error;
    }
  }
};
