from decimal import Decimal
import os
import sys
from typing import Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_properties_collection
from app.services.property_formatter import convert_property_to_text
from app.services.manual_rag.embedding_service import generate_embeddings_batch
from app.services.pinecone_rag.vector_store_service import (
    create_pinecone_index_if_not_exists,
    upsert_property_vectors,
)

BATCH_SIZE = 50


def safe_metadata_value(value: Any):
    if value is None:
        return ""

    if isinstance(value, (str, int, float, bool)):
        return value

    return str(value)


def to_numeric(value: Any) -> float | None:
    if value is None or value == "":
        return None

    if isinstance(value, Decimal):
        return float(value)

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_metadata(property_data, semantic_text: str):
    property_id = str(property_data.get("_id"))

    raw_rental_yield = to_numeric(property_data.get("rental_yield"))
    rental_yield_percent = (
        raw_rental_yield * 100 if raw_rental_yield is not None else None
    )

    return {
        "property_id": property_id,
        "property_name": safe_metadata_value(property_data.get("property_name")),
        "city": safe_metadata_value(property_data.get("city_name")),
        "area": safe_metadata_value(property_data.get("area")),
        "development": safe_metadata_value(property_data.get("development")),
        "property_type": safe_metadata_value(property_data.get("property_type")),
        "price": safe_metadata_value(property_data.get("asking_price")),
        "bedrooms": safe_metadata_value(property_data.get("bedrooms_total")),
        "bathrooms": safe_metadata_value(property_data.get("bathrooms_total")),
        "rental_yield": rental_yield_percent or 0,
        "roi_15": to_numeric(property_data.get("roi_15")) or 0,
        "semantic_text": semantic_text,
    }


def main():
    create_pinecone_index_if_not_exists()

    collection = get_properties_collection()
    properties = list(collection.find({"status": "available"}))

    print(f"Found {len(properties)} properties")

    for start in range(0, len(properties), BATCH_SIZE):
        batch = properties[start : start + BATCH_SIZE]

        semantic_texts = [
            convert_property_to_text(property_data) for property_data in batch
        ]

        embeddings = generate_embeddings_batch(semantic_texts)

        vectors = []

        for property_data, semantic_text, embedding in zip(
            batch, semantic_texts, embeddings
        ):
            property_id = str(property_data.get("_id"))

            vectors.append(
                {
                    "id": property_id,
                    "values": embedding,
                    "metadata": build_metadata(property_data, semantic_text),
                }
            )

        upsert_property_vectors(vectors)

        print(f"Uploaded {start + len(batch)} / {len(properties)} properties")

    print("Pinecone index build completed.")


if __name__ == "__main__":
    main()
