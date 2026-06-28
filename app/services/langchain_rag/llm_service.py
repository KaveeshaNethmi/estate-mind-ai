from click import prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.services.langchain_rag.retrieval_service import retrieve_properties_with_langchain



def build_langchain_context(results: list[dict]) -> str:
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


def generate_langchain_answer(
    question: str,
    top_k: int = 5,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
):
    retrieved_results = retrieve_properties_with_langchain(
        query=question,
        top_k=top_k,
        city=city,
        area=area,
        development=development,
        property_type=property_type,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
    )

    context = build_langchain_context(retrieved_results)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpgul real estate AI coilot. Answer only using the provided context.",
            ),
            (
                "human",
                """
Property Context:
{context}

User Question:
{question}

If the answer is not available in the context, say you do not have enough information.
""",
            ),
        ]
    )

    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)

    chain = prompt | llm

    response = chain.invoke({"context": context, "question": question})

    return {"answer": response.content, "sources": retrieved_results}
