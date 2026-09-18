from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="The content text to analyze")
    page_url: Optional[HttpUrl] = Field(None, description="The URL where the content was found")
    page_title: Optional[str] = Field(None, description="The title of the page")
    content_type: Optional[str] = Field(None, description="Contextual type of content (e.g., offer, ad, post)")
    user_context_signals: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Any observable context signals from the browser (e.g., user is on checkout page)"
    )

class AnalysisResult(BaseModel):
    manipulation_detected: bool = Field(..., description="Whether a manipulation pattern was detected")
    technique: Optional[str] = Field(None, description="The specific technique detected (e.g., Artificial Scarcity)")
    category: Optional[str] = Field(None, description="The broad category of the technique")
    target: Optional[str] = Field(None, description="The psychological target (e.g., Fear of Missing Out)")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score from the ML model")
    severity: Optional[str] = Field(None, description="Severity of the manipulation (low, medium, high)")
    evidence: Optional[List[str]] = Field(default_factory=list, description="Specific snippets from the text that triggered the detection")
    explanation: Optional[str] = Field(None, description="Human-readable explanation of why this is manipulative")

class TargetingInfo(BaseModel):
    available: bool = Field(..., description="Whether targeting analysis is available for this context")
    possible_signals: List[str] = Field(default_factory=list, description="Possible observable targeting signals")
    explanation: str = Field(..., description="Disclaimer regarding proprietary targeting logic vs observable signals")

class AnalysisResponse(BaseModel):
    success: bool = Field(default=True, description="Indicates if the request was processed successfully")
    analysis: AnalysisResult
    targeting: TargetingInfo
