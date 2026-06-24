import numpy as np

from app.services.embedding_service import generate_embedding
from app.services.vector_store_service import load_faiss_index


def retrieve_similar_properties(query: str, top_k: int = 5):
    index, metadata = load_faiss_index()

    query_embedding = generate_embedding(query)
    query_vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []

    for i, property_index in enumerate(indices[0]):
        if property_index == -1:
            continue

        results.append(
            {
                "rank": i + 1,
                "score": float(distances[0][i]),
                "property": metadata[property_index],
            }
        )

    return results
