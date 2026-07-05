from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    top_k: int = 5

    conversation_id: Optional[str] = None
    
    city: Optional[str] = None
    area: Optional[str] = None
    development: Optional[str] = None
    property_type: Optional[str] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
