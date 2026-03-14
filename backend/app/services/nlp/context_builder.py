from typing import List, Dict


def build_focused_context(
    query: str,
    keyphrases: List[Dict],
    retrieved_chunks: List[Dict],
    max_context_chars: int = 2500
) -> str:
    """
    Build a focused context string using:
    - user query
    - top extracted keyphrases
    - top retrieved chunks
    """
    lines = []

    lines.append(f"User Query: {query}")
    lines.append("")

    if keyphrases:
        top_keywords = [item["keyword"] for item in keyphrases[:8]]
        lines.append("Top Document Keyphrases:")
        lines.append(", ".join(top_keywords))
        lines.append("")

    if retrieved_chunks:
        lines.append("Relevant Context:")
        for idx, item in enumerate(retrieved_chunks, start=1):
            chunk_text = item.get("chunk_text", "").strip()
            if chunk_text:
                lines.append(f"[Chunk {idx}] {chunk_text}")
                lines.append("")

    context = "\n".join(lines).strip()

    if len(context) > max_context_chars:
        context = context[:max_context_chars].rsplit(" ", 1)[0] + "..."

    return context