import os
import sys
import json
import joblib

class HumanFirewallPredictor:
    """
    Production inference engine for Human Firewall.
    Loads vectorizers, classifiers, and threshold config to output structured JSON responses.
    """
    def __init__(self, model_dir="ml/models"):
        self.model_dir = model_dir
        
        # Paths
        binary_clf_path = os.path.join(model_dir, "binary_classifier.pkl")
        binary_vec_path = os.path.join(model_dir, "binary_vectorizer.pkl")
        sec_clf_path = os.path.join(model_dir, "secondary_classifier.pkl")
        sec_vec_path = os.path.join(model_dir, "secondary_vectorizer.pkl")
        config_path = os.path.join(model_dir, "config.json")
        
        if not os.path.exists(binary_clf_path):
            raise FileNotFoundError(f"Model artifacts not found in {model_dir}")
            
        self.binary_clf = joblib.load(binary_clf_path)
        self.binary_vec = joblib.load(binary_vec_path)
        self.sec_clf = joblib.load(sec_clf_path)
        self.sec_vec = joblib.load(sec_vec_path)
        
        with open(config_path, "r") as f:
            self.config = json.load(f)
            
        self.threshold = self.config.get("threshold", 0.62)

    def predict(self, text: str) -> dict:
        """
        Runs full inference pipeline on input text.
        """
        if not text or not isinstance(text, str) or not text.strip():
            return {
                "manipulation_detected": False,
                "confidence": 0.99,
                "manipulation_type": "none"
            }
            
        clean_text = text.strip()
        
        # 1. Binary Detection
        X_vec = self.binary_vec.transform([clean_text])
        prob_pos = float(self.binary_clf.predict_proba(X_vec)[0, 1])
        
        is_manipulative = prob_pos >= self.threshold
        
        if not is_manipulative:
            return {
                "manipulation_detected": False,
                "confidence": round(1.0 - prob_pos, 4),
                "manipulation_type": "none"
            }
            
        # 2. Secondary Manipulation Type Classification
        X_sec = self.sec_vec.transform([clean_text])
        predicted_type = str(self.sec_clf.predict(X_sec)[0])
        
        return {
            "manipulation_detected": True,
            "confidence": round(prob_pos, 4),
            "manipulation_type": predicted_type
        }

# Global singleton for backend fast loading
_predictor_instance = None

def predict(text: str) -> dict:
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = HumanFirewallPredictor()
    return _predictor_instance.predict(text)

if __name__ == "__main__":
    predictor = HumanFirewallPredictor()
    
    test_samples = [
        "Hurry! Only 2 left in stock!",
        "13 people have this item in their cart right now.",
        "You won't believe what happened to this celebrity!",
        "Please read our updated privacy policy.",
        "No thanks, I hate saving money"
    ]
    
    print("=== SAMPLE INFERENCE TESTS ===")
    for sample in test_samples:
        res = predictor.predict(sample)
        print(f"Text: '{sample}'\n -> Output: {res}\n")
