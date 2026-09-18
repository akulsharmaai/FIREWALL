from fastapi.testclient import TestClient
from app.main import app

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model_mode" in data

def test_analyze_empty_text():
    with TestClient(app) as client:
        response = client.post("/api/v1/analyze", json={"text": ""})
        assert response.status_code == 422

def test_analyze_mock_scarcity():
    with TestClient(app) as client:
        payload = {
            "text": "Only 2 seats left! Book now before you miss out!",
            "page_title": "Special Offer"
        }
        response = client.post("/api/v1/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        analysis = data["analysis"]
        assert analysis["manipulation_detected"] is True
        assert analysis["technique"] == "Artificial Scarcity"
        assert "confidence" in analysis
        
        targeting = data["targeting"]
        assert targeting["available"] is True
        assert len(targeting["possible_signals"]) > 0

def test_analyze_mock_safe():
    with TestClient(app) as client:
        payload = {
            "text": "This is a normal sentence about flights.",
            "page_title": "Blog"
        }
        response = client.post("/api/v1/analyze", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        analysis = data["analysis"]
        assert analysis["manipulation_detected"] is False
