import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_properties_collection
from app.services.property_formatter import convert_property_to_text
from app.services.embedding_service import generate_embedding
from app.services.vector_store_service import add_embeddings_to_index, save_faiss_index

load_dotenv()


def main():
    collection = get_properties_collection()

    properties = list(
        collection.find({"status": "available", "city_name": "Dubai"}).limit(50)
    )

    embeddings = []
    metadata = []

    for property_data in properties:
        semantic_text = convert_property_to_text(property_data)

        embedding = generate_embedding(semantic_text)

        embeddings.append(embedding)

        metadata.append(
            {
                "property_id": str(property_data.get("_id")),
                "property_name": property_data.get("property_name"),
                "city": property_data.get("city_name"),
                "area": property_data.get("area"),
                "development": property_data.get("development"),
                "property_type": property_data.get("property_type"),
                "price": property_data.get("asking_price"),
                "bedrooms": property_data.get("bedrooms_total"),
                "bathrooms": property_data.get("bathrooms_total"),
                "semantic_text": semantic_text,
            }
        )

    index = add_embeddings_to_index(embeddings)

    save_faiss_index(index, metadata)

    print(f"FAISS index built for {len(properties)} properties.")


if __name__ == "__main__":
    main()
