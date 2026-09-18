import abc
import time
from typing import Dict, Any, Tuple
from app.core.logging import logger
from app.core.config import settings

class MLInferenceBase(abc.ABC):
    """
    Abstract base class for the ML Inference Service.
    The real ML model should implement this interface.
    """
    
    @abc.abstractmethod
    def load_model(self):
        """Load the model weights into memory."""
        pass
        
    @abc.abstractmethod
    def predict(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run inference on the text.
        
        Returns a dictionary representing the prediction:
        {
            "manipulation_detected": bool,
            "technique": str (optional),
            "category": str (optional),
            "target": str (optional),
            "confidence": float (optional),
            "severity": str (optional),
            "evidence": list[str] (optional)
        }
        """
        pass

class MockMLInference(MLInferenceBase):
    """
    Mock ML Inference for local development and hackathon testing.
    Uses basic keyword matching to simulate a model response.
    """
    def __init__(self):
        self.is_loaded = False
        
    def load_model(self):
        logger.info("Loading Mock ML Model (deterministic rules)...")
        time.sleep(0.5)  # Simulate loading delay
        self.is_loaded = True
        logger.info("Mock ML Model loaded.")
        
    def predict(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded.")
            
        text_lower = text.lower()
        
        # Simple mock rules
        if "only" in text_lower and "left" in text_lower:
            return {
                "manipulation_detected": True,
                "technique": "Artificial Scarcity",
                "category": "scarcity",
                "target": "Fear of Missing Out",
                "confidence": 0.89,
                "severity": "high",
                "evidence": [text[:50]]
            }
        elif "hurry" in text_lower or "ends soon" in text_lower:
            return {
                "manipulation_detected": True,
                "technique": "Urgency",
                "category": "urgency",
                "target": "Pressure to act fast",
                "confidence": 0.75,
                "severity": "medium",
                "evidence": [text[:50]]
            }
            
        return {
            "manipulation_detected": False,
            "confidence": 0.95
        }

class RealMLInference(MLInferenceBase):
    """
    Adapter for the real ML Model.
    The ML Engineer will implement the specific loading and inference logic here.
    """
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.is_loaded = False
        self.model = None
        
    def load_model(self):
        logger.info(f"Loading Real ML Model from {self.model_path}...")
        # TODO: ML Engineer to implement actual model loading
        # e.g., self.model = joblib.load(self.model_path)
        self.is_loaded = True
        logger.warning("Real model logic not yet implemented. Please complete RealMLInference.load_model()")
        
    def predict(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded.")
            
        logger.info("Running inference on real model...")
        # TODO: ML Engineer to implement actual inference logic
        # e.g., pred = self.model.predict(text)
        # return map_prediction_to_dict(pred)
        
        # Fallback for now
        return {
            "manipulation_detected": False,
            "confidence": 0.0,
            "evidence": []
        }

# Singleton instantiation based on configuration
if settings.model_mode == "mock":
    ml_model = MockMLInference()
else:
    ml_model = RealMLInference(settings.model_path)
