from fastapi import APIRouter

from app.schemas.chat_schema import ChatRequest
from app.services.langchain_rag.llm_service import generate_langchain_answer
from app.services.manual_rag.llm_service import generate_answer

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/manual")
def chat(request: ChatRequest):
    response = generate_answer(question=request.question, top_k=request.top_k)

    return response

@router.post("/langchain")
def chat_with_langchain(request: ChatRequest):
    response = generate_langchain_answer(
        question=request.question,
        top_k=request.top_k,
        city=request.city,
        area=request.area,
        development=request.development,
        property_type=request.property_type,
        max_price=request.max_price,
        min_bedrooms=request.min_bedrooms,
    )

    return response