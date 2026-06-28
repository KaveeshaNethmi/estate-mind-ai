from openai import OpenAI

from app.core.config import OPENAI_API_KEY
from app.services.manual_rag.retrieval_service import retrieve_similar_properties

client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(results: list[dict]) -> str:
    context_parts = []

    for result in results:
        property_data = result["property"]

        context_parts.append(f"""
Property {result["rank"]}:
Name: {property_data.get("property_name")}
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


def generate_answer(question: str, top_k: int = 5) -> dict:
    retrieved_results = retrieve_similar_properties(question, top_k=top_k)

    context = build_context(retrieved_results)

    prompt = f"""
You are a real estate AI copilot.

Answer the user's question using ONLY the property context below.

If the answer is not available in the context, say that you don't have enough information.

Be helpful, clear, and practical.

Property Context:
{context}

User Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful real estate AI copilot."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return {"answer": response.choices[0].message.content, "sources": retrieved_results}
