// Configuration constants
const CONFIG = {
  // Base URL for the Backend API
  API_BASE_URL: 'http://localhost:8000',
  
  // Extraction limits
  MAX_TEXT_LENGTH: 5000,
  
  // Storage Keys
  STORAGE_KEYS: {
    API_URL: 'hf_api_url',
    RESULTS_CACHE: 'hf_results_cache'
  }
};

// Message Types
const MESSAGES = {
  SCAN_CURRENT_PAGE: 'SCAN_CURRENT_PAGE',
  GET_CURRENT_RESULT: 'GET_CURRENT_RESULT',
  ANALYZE_PAGE: 'ANALYZE_PAGE',
  ANALYSIS_RESULT: 'ANALYSIS_RESULT',
  CURRENT_RESULT: 'CURRENT_RESULT',
  HIGHLIGHT_EVIDENCE: 'HIGHLIGHT_EVIDENCE'
};
