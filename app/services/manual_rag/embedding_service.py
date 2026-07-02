from turtle import mode

from openai import OpenAI

from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)

    return response.data[0].embedding


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )

    return [item.embedding for item in response.data]
