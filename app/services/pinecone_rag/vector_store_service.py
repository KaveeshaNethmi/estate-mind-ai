from pinecone import Pinecone, ServerlessSpec

from app.core.config import (
    PINECONE_API_KEY,
    PINECONE_CLOUD,
    PINECONE_INDEX_NAME,
    PINECONE_REGION,
)

EMBEDDING_DIMENSION = 1536


def get_pinecone_client():
    return Pinecone(api_key=PINECONE_API_KEY)


def create_pinecone_index_if_not_exists():
    pc = get_pinecone_client()

    existing_indexes = [index["name"] for index in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION),
        )

    return pc.Index(PINECONE_INDEX_NAME)


def get_pinecone_index():
    pc = get_pinecone_client()

    return pc.Index(PINECONE_INDEX_NAME)


def upsert_property_vectors(vectors: list[dict], namespace: str = "properties"):
    index = get_pinecone_index()

    index.upsert(vectors=vectors, namespace=namespace)
