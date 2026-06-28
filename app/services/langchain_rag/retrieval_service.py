

from app.services.langchain_rag.vector_store_service import load_langchain_vector_store


def retrieve_properties_with_langchain(
    query: str,
    top_k=5,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
):
    vector_store = load_langchain_vector_store()

    docs_with_scores = vector_store.similarity_search_with_score(query, k=top_k * 3)

    results = []

    for doc, score in docs_with_scores:
        metadata = doc.metadata

        city_value = metadata.get("city")
        area_value = metadata.get("area")
        development_value = metadata.get("development")
        property_type_value = metadata.get("property_type")
        price = metadata.get("price")
        bedrooms = metadata.get("bedrooms")

        if city and city_value != city:
            continue

        if area and area_value != area:
            continue

        if development and development_value != development:
            continue

        if property_type and property_type_value != property_type:
            continue

        if max_price is not None and price is not None and price > max_price:
            continue

        if (
            min_bedrooms is not None
            and bedrooms is not None
            and bedrooms < min_bedrooms
        ):
            continue

        results.append(
            {
                "rank": len(results) + 1,
                "score": float(score),
                "property": {
                    **metadata,
                    "semantic_text": doc.page_content,
                },
            }
        )

        if len(results) >= top_k:
            break

    return results
