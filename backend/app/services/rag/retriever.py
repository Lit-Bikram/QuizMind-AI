from app.services.rag.embedder import embed_query
from app.services.rag.chunk_quality import is_reference_heavy_chunk


def retrieve_top_k_chunks(query: str, index, chunks: list[str], k: int = 3):
    """
    Retrieve top-k most relevant chunks for a query.
    Automatically adjusts k if there are fewer chunks available.
    Filters out reference-heavy / low-quality chunks.
    """
    if not chunks:
        return []

    # Ask FAISS for more than needed so we can filter bad chunks
    search_k = min(max(k * 3, 6), len(chunks))

    query_embedding = embed_query(query)
    distances, indices = index.search(query_embedding, search_k)

    results = []

    for rank_idx, idx in enumerate(indices[0]):
        if idx == -1 or idx >= len(chunks):
            continue

        chunk_text = chunks[idx]

        # Skip reference-heavy chunks
        if is_reference_heavy_chunk(chunk_text):
            continue

        results.append({
            "rank": len(results) + 1,
            "chunk_index": int(idx),
            "distance": float(distances[0][rank_idx]),
            "chunk_text": chunk_text
        })

        if len(results) >= k:
            break

    return results