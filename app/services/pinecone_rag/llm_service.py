from openai import OpenAI

from app.core.config import OPENAI_API_KEY
from app.services.pinecone_rag.retrieval_service import (
    retrieve_properties_with_pinecone,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def build_pinecone_context(results: list[dict]) -> str:
    context_parts = []

    for result in results:
        property_data = result["property"]

        context_parts.append(f"""
Property {result["rank"]}:
Name: {property_data.get("property_name")}
City: {property_data.get("city")}
Area: {property_data.get("area")}
Development: {property_data.get("development")}
Type: {property_data.get("property_type")}
Price: {property_data.get("price")}
Bedrooms: {property_data.get("bedrooms")}
Bathrooms: {property_data.get("bathrooms")}

Details:
{property_data.get("semantic_text")}
""")

    return "\n\n".join(context_parts)


def generate_pinecone_answer(
    question: str,
    top_k: int = 5,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
):
    retrieved_results = retrieve_properties_with_pinecone(
        query=question,
        top_k=top_k,
        city=city,
        area=area,
        development=development,
        property_type=property_type,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
    )

    context = build_pinecone_context(retrieved_results)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful real estate AI copilot. Answer only using the provided property context.",
            },
            {
                "role": "user",
                "content": f"""
Property Context:
{context}

User Question:
{question}

If the answer is not available in the context, say you do not have enough information.
""",
            },
        ],
        temperature=0.2,
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": retrieved_results,
    }
