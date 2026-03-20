import faiss # type: ignore
import numpy as np # type: ignore


def create_faiss_index(embeddings: np.ndarray):
    """
    Create a FAISS index from embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index