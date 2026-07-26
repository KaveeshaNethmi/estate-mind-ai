from openai import OpenAI

from app.core.config import CHAT_MODEL, OPENAI_API_KEY
from app.schemas.reranking_schema import RerankingResponse
from app.utils.number_utils import clamp_score

client = OpenAI(api_key=OPENAI_API_KEY)


def rerank_properties(
    question: str, results: list[dict], top_n: int = 5
) -> list[dict]:
    """
    Rerank Pinecone candidates according to their relevance to the
    original user question.

    The original Pinecone score is preserved as `score`.
    The reranker adds `rerank_score` and `rerank_reason`.
    """

    if not results:
        return []

    if len(results) == 1:
        single_result = results[0].copy()
        single_result["rerank_score"] = 1.0
        single_result["rerank_reason"] = "Only one candidate was available."
        single_result["rank"] = 1

        return [single_result]

    candidates_text = build_reranking_candidates(results)

    completion = client.beta.chat.completions.parse(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a real-estate serach reranker. "
                    "Evaluate how well each candidtae satisfies the user's "
                    "actual question. Consider location, property type, "
                    "peice bedrooms, development, investement metrics, and "
                    "all explicit requirements. Do not answer the question."
                ),
            },
            {
                "role": "user",
                "content": f"""
User question:
{question}

Property candidates"
{candidates_text}

Instructions:
- Return every candidate exactly once.
- Use the supplied candidate_id values.
- Give each candidate a relevance score from 0 to 1.
- 1 means the candidate strongly satisfies the question.
- 0 means it is irrelevant or contradicts the requirements.
- Do not invent property information.
- Score based only on the supplied candidate data.
""",
            },
        ],
        response_format=RerankingResponse,
        temperature=0,
    )

    parsed = completion.choices[0].message.parsed

    if parsed is None:
        return fallback_rerank(results, top_n)

    result_by_candidate_id = {
        create_candidate_id(index): result for index, result in enumerate(results)
    }

    reranked_results: list[dict] = []

    for reranked_item in parsed.results:
        original_result = result_by_candidate_id.get(reranked_item.candidate_id)

        if original_result is None:
            continue

        updated_result = original_result.copy()
        updated_result["rerank_score"] = reranked_item.relevance_score
        updated_result["rerank_reason"] = reranked_item.reason

        reranked_results.append(updated_result)

    # In case the model accidentally omitted candidates, add them using
    # their original Pinecone scores.
    returned_candidate_ids = {item.candidate_id for item in parsed.results}

    for index, original_result in enumerate(results):
        candidate_id = create_candidate_id(index)

        if candidate_id in returned_candidate_ids:
            continue

        updated_result = original_result.copy()
        updated_result["rerank_score"] = clamp_score(original_result.get("score"))
        updated_result["rerank_reason"] = "Fallback score based on Pinecone similarity."

        reranked_results.append(updated_result)

    reranked_results.sort(
        key=lambda result: result.get("rerank_score", 0),
        reverse=True,
    )

    selected_results = reranked_results[:top_n]

    # Reassign display ranks after reranking.
    for index, result in enumerate(selected_results, start=1):
        result["rank"] = index

    return selected_results


def build_reranking_candidates(
    results: list[dict],
) -> str:
    candidate_parts: list[str] = []

    for index, result in enumerate(results):
        property_data = result.get("property", {})
        candidate_id = create_candidate_id(index)

        candidate_parts.append(f"""
Candidate ID: {candidate_id}
Property ID: {property_data.get("property_id")}
Name: {property_data.get("property_name")}
City: {property_data.get("city")}
Area: {property_data.get("area")}
Development: {property_data.get("development")}
Property Type: {property_data.get("property_type")}
Price: {property_data.get("price")}
Bedrooms: {property_data.get("bedrooms")}
Bathrooms: {property_data.get("bathrooms")}
Rental Yield: {property_data.get("rental_yield")}
ROI: {property_data.get("roi_15")}
Description: {property_data.get("semantic_text")}
""".strip())

    return "\n\n".join(candidate_parts)


def fallback_rerank(
    results: list[dict],
    top_n: int,
) -> list[dict]:
    """
    Fall back to Pinecone similarity ordering if the LLM reranker fails.
    """

    fallback_results: list[dict] = []

    for result in results:
        updated_result = result.copy()
        updated_result["rerank_score"] = clamp_score(result.get("score"))
        updated_result["rerank_reason"] = "Fallback score based on Pinecone similarity."

        fallback_results.append(updated_result)

    fallback_results.sort(
        key=lambda result: result.get("rerank_score", 0),
        reverse=True,
    )

    selected_results = fallback_results[:top_n]

    for index, result in enumerate(selected_results, start=1):
        result["rank"] = index

    return selected_results

def create_candidate_id(index: int) -> str:
    return f"candidate-{index + 1}"
