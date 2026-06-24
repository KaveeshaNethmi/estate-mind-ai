from fastapi import FastAPI

from app.api.routes.chat_routes import router as chat_router

app = FastAPI(
    title="EstateMind AI",
    description="Real Estate AI Copilot powered by RAG, FAISS, and OpenAI",
    version="1.0.0",
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "EstateMind AI is running"}
