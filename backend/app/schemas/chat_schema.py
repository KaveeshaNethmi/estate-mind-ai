from typing import Any, Optional

from pydantic import BaseModel, Field


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


class PreparedChatResponse(BaseModel):
    conversation_id: str
    question: str
    rewritten_query: str
    chat_history: str
    search_state: dict[str, Any] = Field(default_factory=dict)
    retrieved_results: list[dict[str, Any]] = Field(default_factory=list)
    context: str
    reference_detected: bool = False
    reused_previous_results: bool = False
    entity_reference: dict[str, Any] = Field(default_factory=dict)
