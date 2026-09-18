import abc
import os
import sys
import time
from typing import Dict, Any, Tuple
from app.core.logging import logger
from app.core.config import settings

# Dynamically add project root directory to sys.path so ml.src.predict is always importable
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from ml.src.predict import HumanFirewallPredictor
except Exception as e:
    logger.error(f"Error importing HumanFirewallPredictor: {e}")
    HumanFirewallPredictor = None

class MLInferenceBase(abc.ABC):
    @abc.abstractmethod
    def load_model(self):
        pass
        
    @abc.abstractmethod
    def predict(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        pass

class RealMLInference(MLInferenceBase):
    def __init__(self, model_dir: str = None):
        if model_dir is None:
            model_dir = os.path.join(PROJECT_ROOT, "ml", "models")
        self.model_dir = model_dir
        self.predictor = None
        self.is_loaded = False
        
    def load_model(self):
        logger.info(f"Loading trained ML model artifacts from {self.model_dir}...")
        try:
            if HumanFirewallPredictor is None:
                raise ImportError("HumanFirewallPredictor could not be imported from ml.src.predict")
            self.predictor = HumanFirewallPredictor(model_dir=self.model_dir)
            self.is_loaded = True
            logger.info("Trained ML model successfully loaded into memory!")
        except Exception as e:
            logger.error(f"Failed to load trained ML model: {e}")
            raise e
            
    def predict(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.is_loaded or self.predictor is None:
            raise RuntimeError("ML model is not loaded in memory.")
            
        t_start = time.time()
        
        tech_map = {
            "artificial_scarcity": "Fake Limited Stock",
            "urgency": "Urgent Countdown / Rush Tactic",
            "social_pressure": "Peer Pressure & Hype",
            "deceptive_choice": "Guilt-Trip Choice",
            "dark_pattern": "Hidden Traps & Fine Print",
            "clickbait": "Clickbait / Attention Trap",
            "emotional_manipulation": "Emotional Pressure",
            "general_persuasion": "Pushy Sales Language",
            "rhetorical_persuasion": "Pushy Sales Language"
        }
        
        if not text or not isinstance(text, str) or not text.strip():
            return {
                "manipulation_detected": False,
                "technique": "None",
                "category": "none",
                "target": "user_behavior",
                "confidence": 0.99,
                "severity": "none",
                "evidence": [],
                "latency_ms": round((time.time() - t_start) * 1000, 2)
            }
            
        # Split text into candidate lines / snippets
        raw_chunks = [c.strip() for c in text.splitlines() if c.strip()]
        if len(raw_chunks) <= 1 and ("." in text or "!" in text or "?" in text):
            import re
            raw_chunks = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
            
        # Deduplicate and sanitize chunks
        chunks = []
        seen = set()
        for c in raw_chunks:
            c_clean = c.strip()
            if len(c_clean) >= 4 and c_clean.lower() not in seen:
                seen.add(c_clean.lower())
                chunks.append(c_clean)
                
        if not chunks:
            chunks = [text.strip()]

        detected_items = []
        
        # Evaluate each candidate snippet with the ML predictor
        for chunk in chunks[:100]:
            res = self.predictor.predict(chunk)
            if res.get("manipulation_detected", False):
                detected_items.append({
                    "text": chunk,
                    "confidence": res.get("confidence", 0.0),
                    "manipulation_type": res.get("manipulation_type", "none")
                })
                
        latency_ms = round((time.time() - t_start) * 1000, 2)
        
        if detected_items:
            # Sort by confidence descending
            detected_items.sort(key=lambda x: x["confidence"], reverse=True)
            top_item = detected_items[0]
            m_type = top_item["manipulation_type"]
            conf = top_item["confidence"]
            
            # Severity mapping
            severity = "medium"
            if conf >= 0.85 or m_type in ["artificial_scarcity", "deceptive_choice"]:
                severity = "high"
            elif conf <= 0.70:
                severity = "low"
                
            # Collect unique offending snippets as evidence (up to 3)
            evidence = []
            ev_seen = set()
            for item in detected_items:
                ev_text = item["text"]
                if ev_text not in ev_seen:
                    ev_seen.add(ev_text)
                    evidence.append(ev_text)
                if len(evidence) >= 3:
                    break
                    
            return {
                "manipulation_detected": True,
                "technique": tech_map.get(m_type, m_type.replace("_", " ").title()),
                "category": m_type,
                "target": "user_behavior",
                "confidence": round(conf, 4),
                "severity": severity,
                "evidence": evidence,
                "latency_ms": latency_ms
            }
        else:
            # Fallback for single concise inputs under 250 characters
            if len(text.strip()) <= 250:
                res = self.predictor.predict(text.strip())
                if res.get("manipulation_detected", False):
                    m_type = res.get("manipulation_type", "none")
                    conf = res.get("confidence", 0.0)
                    severity = "high" if conf >= 0.85 else "medium"
                    return {
                        "manipulation_detected": True,
                        "technique": tech_map.get(m_type, m_type.replace("_", " ").title()),
                        "category": m_type,
                        "target": "user_behavior",
                        "confidence": round(conf, 4),
                        "severity": severity,
                        "evidence": [text.strip()],
                        "latency_ms": latency_ms
                    }
                    
            return {
                "manipulation_detected": False,
                "technique": "None",
                "category": "none",
                "target": "user_behavior",
                "confidence": 0.95,
                "severity": "none",
                "evidence": [],
                "latency_ms": latency_ms
            }

# Instantiate Singleton with real ML model
ml_model = RealMLInference()
