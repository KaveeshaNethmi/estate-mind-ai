from encodings import utf_8
from importlib import metadata

import faiss
import numpy as np
import json
import os

from app.core.config import INDEX_PATH, METADATA_PATH, VECTOR_STORE_DIR


# Create FAISS index
def create_faiss_index(dimension: int):
    return faiss.IndexFlatL2(dimension)


# Adding vectors to the created store
def add_embeddings_to_index(embeddings: list[list[float]]):
    vectors = np.array(embeddings).astype("float32")

    if vectors.ndim != 2:
        raise ValueError("Embeddings must be a 2D array")

    """
    Get the vector dimension -> 
    If there are 100 properties and 1536 dimension (the numbers that OpenAI returns)
    vector looks like 100 * 1536.
    Then the shape would be (100, 1536)
    shape[1] = dimension = 1536 (Number of dimensions per vector)
    """
    dimension = vectors.shape[1]

    """
    create FAISS
    """
    index = create_faiss_index(dimension)

    """
    After storing vectors FAISS would be like,
    vector 0 -> [0.12,...]
    vector 1 -> [0.34,...]
    vector 2 -> [0.56,...]
    """
    index.add(vectors)  # Store vectors

    return index  # return all the vectors


def save_faiss_index(index, metadata: list[dict]):
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)  # Saving metadata


def load_faiss_index():
    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata
