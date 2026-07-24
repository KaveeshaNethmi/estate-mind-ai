from pydantic import BaseModel, Field


class RerankingProperty(BaseModel):
    candidate_id: str

    relevance_score: float = Field(
        ge=0, le=1, description="Relevance of the property to the user's question."
    )

    reason: str


class RerankingResponse(BaseModel):
    results: list[RerankingProperty]
