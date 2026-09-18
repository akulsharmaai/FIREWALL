# Human Firewall Backend API

This document details the primary endpoints exposed by the Human Firewall API for the browser extension.

## 1. Health Check

Used to verify the API is running and check the model status.

- **Endpoint:** `GET /health` or `GET /api/v1/health`
- **Response Format:**
```json
{
  "status": "healthy",
  "model_mode": "mock",
  "model_loaded": true
}
```

## 2. Analyze Content

The core endpoint for detecting manipulation patterns.

- **Endpoint:** `POST /api/v1/analyze`
- **Content-Type:** `application/json`

### Request Example
```json
{
  "text": "ONLY 2 SEATS LEFT! 97% OF PEOPLE HAVE ALREADY BOOKED! BOOK NOW BEFORE IT'S TOO LATE!",
  "page_url": "https://example.com/booking",
  "page_title": "Flight Booking - Example",
  "content_type": "offer",
  "user_context_signals": {
    "is_checkout_page": true
  }
}
```

**Fields:**
- `text` (string, required, max length 10000): The extracted text to analyze.
- `page_url` (string, optional): URL where the content was found.
- `page_title` (string, optional): Title of the page.
- `content_type` (string, optional): Contextual content type (e.g. ad, offer).
- `user_context_signals` (object, optional): Additional observable context from the browser.

### Success Response Example (200 OK)
```json
{
  "success": true,
  "analysis": {
    "manipulation_detected": true,
    "technique": "Artificial Scarcity",
    "category": "scarcity",
    "target": "Fear of Missing Out",
    "confidence": 0.89,
    "severity": "high",
    "evidence": [
      "ONLY 2 SEATS LEFT!"
    ],
    "explanation": "The content creates pressure by suggesting that availability is rapidly decreasing."
  },
  "targeting": {
    "available": true,
    "possible_signals": [
      "Page title suggests a promotional offer context."
    ],
    "explanation": "These are observable contextual signals and do not represent confirmed proprietary targeting logic."
  }
}
```

### Error Response Example (400 / 422 / 500)
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "String should have at least 1 character"
  }
}
```
