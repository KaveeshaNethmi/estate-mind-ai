import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str) -> str:
    value = os.getenv(name)

    if value is None:
        raise ValueError(f"{name} is missing from .env")

    return value


OPENAI_API_KEY = get_env("OPENAI_API_KEY")
CHAT_MODEL = "gpt-4.1-mini"

MONGO_URI = get_env("MONGO_URI")
DB_NAME = get_env("DB_NAME")
COLLECTION_NAME = get_env("COLLECTION_NAME")
CONVERSATION_COLLECTION_NAME = "conversations"

# Define paths od vector store
VECTOR_STORE_DIR = "vector_store"
INDEX_PATH = (
    f"{VECTOR_STORE_DIR}/properties.index"  # Where FAISS stores all the vectors
)
METADATA_PATH = (
    f"{VECTOR_STORE_DIR}/metadata.json"  # Stores information about each vetor
)

LANGCHAIN_VECTOR_STORE_PATH = (
    f"{VECTOR_STORE_DIR}/langchain_faiss_index"  # Where FAISS stores using Langchain
)

# Pinecone
PINECONE_API_KEY = get_env("PINECONE_API_KEY")
PINECONE_INDEX_NAME = get_env("PINECONE_INDEX_NAME")

PINECONE_CLOUD = get_env("PINECONE_CLOUD")
PINECONE_REGION = get_env("PINECONE_REGION")
