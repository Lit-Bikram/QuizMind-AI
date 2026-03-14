from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks by words.

    Args:
        text: Full input text
        chunk_size: Number of words per chunk
        overlap: Overlapping words between chunks

    Returns:
        List of text chunks
    """
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks