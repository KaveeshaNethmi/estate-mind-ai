from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from app.core.config import LANGCHAIN_VECTOR_STORE_PATH, OPENAI_API_KEY


def get_langchain_embedding_model():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
    )

def load_langchain_vector_store():
    embeddings = get_langchain_embedding_model()

    return FAISS.load_local(
        LANGCHAIN_VECTOR_STORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )