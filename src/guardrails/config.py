from pydantic import BaseModel
from typing import List

class GuardrailsConfig(BaseModel):
    """Configuration for guardrails system"""
    
    # Input validation settings
    max_query_length: int = 500
    min_query_length: int = 5
    
    # PII patterns
    pii_enabled: bool = True
    
    # Prompt injection settings
    injection_detection_enabled: bool = True
    
    # Output moderation settings
    toxicity_threshold: float = 0.01
    min_response_length: int = 20
    
    # Agriculture-specific settings for plant disease
    allowed_topics: List[str] = [
        "plant", "disease", "crop", "leaf", "agriculture",
        "farming", "pest", "fungus", "bacteria", "virus",
        "treatment", "pesticide", "fertilizer", "soil",
        "tomato", "potato", "corn", "wheat", "rice"
    ]
    
    # Harmful advice patterns to block
    harmful_patterns: List[str] = [
        "drink", "consume", "eat", "ingest",
        "apply to skin", "use internally"
    ]

# Global config instance
config = GuardrailsConfig()