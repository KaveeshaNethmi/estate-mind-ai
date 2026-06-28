import os
import sys

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_properties_collection
from app.services.property_formatter import convert_property_to_text

LANGCHAIN_VECTOR_STORE_PATH = "vector_store/langchain_faiss_index"


def main():
    print("Starting LangChain FAISS build...")

    collection = get_properties_collection()
    properties = list(collection.find({"status": "available"}).limit(100))

    print(f"Loaded {len(properties)} properties from MongoDB")

    documents = []

    for property_data in properties:
        semantic_text = convert_property_to_text(property_data)
        documents.append(
            Document(
                page_content=semantic_text,
                metadata={
                    "property_id": str(property_data.get("_id")),
                    "property_name": property_data.get("property_name"),
                    "city": property_data.get("city_name"),
                    "area": property_data.get("area"),
                    "development": property_data.get("development"),
                    "property_type": property_data.get("property_type"),
                    "price": property_data.get("asking_price"),
                    "bedrooms": property_data.get("bedrooms_total"),
                    "bathrooms": property_data.get("bathrooms_total"),
                },
            )
        )

    print(f"Prepared {len(documents)} LangChain documents")
    print("Generating embeddings and building FAISS index...")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings,
    )

    print("Saving FAISS index...")

    vector_store.save_local(LANGCHAIN_VECTOR_STORE_PATH)

    print(f"LangChain FAISS index built for {len(documents)} properties.")


if __name__ == "__main__":
    main()
