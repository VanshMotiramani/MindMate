from pydantic import BaseModel
from typing import Optional

class SentimentRequest(BaseModel):
    user_id: int
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float
    
