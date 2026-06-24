from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest
from app.services.llm_service import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
def chat(request: ChatRequest):
    response = generate_answer(question=request.question, top_k=request.top_k)

    return response
