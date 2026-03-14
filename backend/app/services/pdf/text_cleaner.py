import re


def clean_pdf_text(text: str) -> str:
    """
    Clean noisy PDF text before chunking:
    - remove common ResearchGate header noise
    - remove repeated DOI / page metadata patterns
    - truncate references section if detected
    - normalize whitespace
    """
    if not text or not text.strip():
        return ""

    cleaned = text

    # Remove common noisy lines / phrases
    noisy_patterns = [
        r"See discussions, stats, and author profiles for this publication at:.*",
        r"All content following this page was uploaded by.*",
        r"The user has requested enhancement of the downloaded file\..*",
        r"Article reuse guidelines:.*",
        r"journals\.sagepub\.com/home/\w+.*",
        r"DOI:\s*10\.\S+",
        r"READS\s+\d+",
        r"CITATIONS\s+\d+",
        r"SEE PROFILE",
        r"View publication stats",
    ]

    for pattern in noisy_patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Truncate at References section (common for academic PDFs)
    reference_markers = [
        r"\nReferences\n",
        r"\nREFERENCES\n",
        r"\nReferences\s",
        r"\nREFERENCES\s"
    ]

    for marker in reference_markers:
        match = re.search(marker, cleaned)
        if match:
            cleaned = cleaned[:match.start()]
            break

    # Remove excessive whitespace/newlines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[ \t]{2,}", " ", cleaned)

    return cleaned.strip()