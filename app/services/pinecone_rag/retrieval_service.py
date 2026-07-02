from app.services.manual_rag.embedding_service import generate_embedding
from app.services.pinecone_rag.vector_store_service import get_pinecone_index


def retrieve_properties_with_pinecone(
    query: str,
    top_k: int = 5,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
):
    index = get_pinecone_index()
    query_embedding = generate_embedding(query)

    filter_query = {}

    if city:
        filter_query["city"] = {"$eq": city}

    if area:
        filter_query["area"] = {"$eq": area}

    if development:
        filter_query["development"] = {"$eq": development}

    if property_type:
        filter_query["property_type"] = {"$eq": property_type}

    if max_price:
        filter_query["price"] = {"$lte": max_price}

    if min_bedrooms:
        filter_query["bedrooms"] = {"$gte": min_bedrooms}

    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        namespace="properties",
        include_metadata=True,
        filter=filter_query if filter_query else None,
    )

    results = []

    for i, match in enumerate(response["matches"]):
        results.append(
            {"rank": i + 1, "score": match["score"], "property": match["metadata"]}
        )

    return results
