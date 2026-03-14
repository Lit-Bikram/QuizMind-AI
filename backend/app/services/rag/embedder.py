from sentence_transformers import SentenceTransformer

# Load model once at module level for efficiency
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]):
    """
    Generate embeddings for a list of text chunks.
    """
    return embedding_model.encode(texts, convert_to_numpy=True)


def embed_query(query: str):
    """
    Generate embedding for a single query string.
    """
    return embedding_model.encode([query], convert_to_numpy=True)