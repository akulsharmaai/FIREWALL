# Human Firewall - Browser Extension

This is the browser extension layer for the **Human Firewall** hackathon project. It is built using Manifest V3 and pure JavaScript to remain lightweight and easy to integrate.

## What it does
1. Extracts text from the active webpage, filtering out hidden or sensitive elements (like passwords).
2. Truncates and forwards the extracted text to the Backend API.
3. Receives analysis results indicating if manipulation patterns (like Fake Scarcity or Urgency) exist.
4. Displays the results in a user-friendly popup.
5. Injects a non-intrusive badge and highlights explicit manipulation evidence directly on the webpage.

## Directory Structure
```
extension/
├── manifest.json              # Extension configuration & permissions
├── src/
│   ├── background/
│   │   └── service-worker.js  # Coordinates messages and API calls
│   ├── content/
│   │   ├── content.js         # Entry point for page interaction
│   │   ├── extractor.js       # Safely extracts visible text from the DOM
│   │   ├── highlighter.js     # Safely highlights text & injects shadow DOM badge
│   │   └── content.css        # Styles for highlights
│   ├── popup/
│   │   ├── popup.html         # Main UI structure
│   │   ├── popup.js           # UI logic (Scan button, displaying results)
│   │   └── popup.css          # Styling for the UI
│   ├── api/
│   │   └── api-client.js      # Handles backend fetch() with timeouts
│   └── utils/
│       ├── constants.js       # Configuration (API URL) and message types
│       └── messaging.js       # Helper for chrome.runtime messaging
└── README.md
```

## How to Install and Run Locally
1. Start the FastAPI backend server first (refer to `backend/README.md` or `run.py`).
2. Open Google Chrome and go to `chrome://extensions/`.
3. Enable **Developer mode** in the top right corner.
4. Click **Load unpacked** and select this `extension/` directory.
5. Navigate to any webpage (e.g., an airline booking site or an e-commerce store).
6. Click the **Human Firewall** extension icon in your toolbar and press **Scan Current Page**.

## Configuration
The base URL for the backend API is defined in `src/utils/constants.js`.
If your backend is running on a different port, update the `API_BASE_URL` variable in that file:
```javascript
API_BASE_URL: 'http://localhost:8000',
```

## Permissions Used
- `activeTab`: To read the current webpage's content only when the user explicitly triggers a scan.
- `scripting`: To execute the content scripts dynamically when needed.
- `storage`: Available for caching or saving user preferences.

## Testing End-to-End
1. Ensure the backend `.env` is set to `MODEL_MODE=mock`.
2. Open a page and inject some mock text (e.g., "Only 2 seats left! Book now!").
3. Click **Scan Current Page** in the extension.
4. The extension will highlight "Only 2 seats left" on the page and show a red badge.
