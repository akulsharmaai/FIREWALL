from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisResult, TargetingInfo
from app.services.ml_service import ml_model
from app.core.logging import logger

def analyze_content(request: AnalysisRequest) -> AnalysisResponse:
    """
    Orchestrates the analysis pipeline:
    1. Extracts text and context
    2. Calls ML Inference
    3. Normalizes and structures the response
    """
    logger.info(f"Analyzing content of length {len(request.text)}")
    
    # Context aggregation
    context = {
        "page_url": str(request.page_url) if request.page_url else None,
        "page_title": request.page_title,
        "content_type": request.content_type,
        "user_context_signals": request.user_context_signals
    }
    
    # ML Inference
    prediction = ml_model.predict(request.text, context)
    
    # Generate User-Friendly Explanation if manipulation detected
    explanation = None
    if prediction.get("manipulation_detected"):
        cat = prediction.get("category", "")
        technique = prediction.get("technique", "Manipulative Copy")
        
        explanations_map = {
            "artificial_scarcity": "This page claims stock or seats are running out to make you rush into buying before checking other options.",
            "urgency": "This page uses urgent countdown timers or rush warnings to pressure you into making a fast purchase.",
            "social_pressure": "This page highlights recent buyers or visitor counts to create peer pressure.",
            "deceptive_choice": "This page uses guilt-tripping options (like 'No thanks, I hate saving') or misleading buttons to influence your choice.",
            "dark_pattern": "This page hides important fees or sneaks paid add-ons into your order in fine print.",
            "clickbait": "This headline uses sensationalist phrasing to trick you into clicking.",
            "emotional_manipulation": "This copy plays on fear or guilt to pressure you into taking action.",
            "general_persuasion": "This page uses pushy sales pitches or slogans to influence your purchase decision.",
            "rhetorical_persuasion": "This page uses pushy sales pitches or slogans to influence your purchase decision."
        }
        explanation = explanations_map.get(cat, f"This content uses {technique.lower() if technique else 'persuasive tactics'} to influence your choices online.")
    
    analysis_result = AnalysisResult(
        manipulation_detected=prediction.get("manipulation_detected", False),
        technique=prediction.get("technique"),
        category=prediction.get("category"),
        target=prediction.get("target"),
        confidence=prediction.get("confidence"),
        severity=prediction.get("severity"),
        evidence=prediction.get("evidence", []),
        explanation=explanation
    )
    
    # Evaluate Observable Context (Targeting)
    possible_signals = []
    if request.page_title and "offer" in request.page_title.lower():
        possible_signals.append("Page title suggests a promotional offer context.")
    if request.content_type == "ad":
        possible_signals.append("Content is explicitly marked as an advertisement.")
        
    targeting_info = TargetingInfo(
        available=True,
        possible_signals=possible_signals,
        explanation="These are observable contextual signals and do not represent confirmed proprietary targeting logic."
    )
    
    return AnalysisResponse(
        success=True,
        analysis=analysis_result,
        targeting=targeting_info
    )
