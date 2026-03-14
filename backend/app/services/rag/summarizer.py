from typing import List, Dict


def build_extractive_summary(
    chunks: List[str],
    retrieved_chunks: List[Dict],
    max_summary_chars: int = 1800
) -> str:
    """
    Build a lightweight extractive summary from:
    - first chunk (intro bias)
    - last chunk (conclusion bias)
    - top retrieved chunks

    Deduplicates repeated chunks and returns a concise summary.
    """
    selected_chunks = []

    # Add first chunk (often title/abstract/introduction)
    if chunks:
        selected_chunks.append(chunks[0])

    # Add retrieved chunks
    for item in retrieved_chunks:
        chunk_text = item.get("chunk_text", "").strip()
        if chunk_text:
            selected_chunks.append(chunk_text)

    # Add last chunk (often conclusion/references area)
    if len(chunks) > 1:
        selected_chunks.append(chunks[-1])

    # Deduplicate while preserving order
    seen = set()
    unique_chunks = []
    for chunk in selected_chunks:
        normalized = " ".join(chunk.split())
        if normalized not in seen:
            seen.add(normalized)
            unique_chunks.append(chunk)

    # Build summary text
    summary = "\n\n".join(unique_chunks).strip()

    # Trim if too long
    if len(summary) > max_summary_chars:
        summary = summary[:max_summary_chars].rsplit(" ", 1)[0] + "..."

    return summary