import re


def is_reference_heavy_chunk(chunk_text: str) -> bool:
    """
    Heuristic to detect bibliography/reference-heavy chunks.
    Returns True if the chunk looks like references rather than real content.
    """
    if not chunk_text or not chunk_text.strip():
        return True

    text = chunk_text.strip()

    # Too many DOI mentions
    doi_count = len(re.findall(r"10\.\d{4,9}/\S+", text))

    # Too many year-like patterns (e.g. 2013, 2020)
    year_count = len(re.findall(r"\b(19|20)\d{2}\b", text))

    # Many numbered citations / reference-style numbering
    numbered_ref_count = len(re.findall(r"\b\d{1,2}\.\s[A-Z]", text))

    # Journal-style patterns
    journal_markers = [
        "doi:",
        "clin neurophysiol",
        "neurobiol aging",
        "alzheimer dement",
        "j neural transm",
        "electroencephalogr",
        "acta neurol scand"
    ]
    marker_hits = sum(1 for marker in journal_markers if marker.lower() in text.lower())

    # Heuristic threshold
    score = doi_count + year_count + numbered_ref_count + marker_hits

    return score >= 6