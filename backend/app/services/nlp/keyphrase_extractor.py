from keybert import KeyBERT # type: ignore

# Load once at module level
keyword_model = KeyBERT(model="all-MiniLM-L6-v2")


def extract_keyphrases(
    text: str,
    top_n: int = 10,
    keyphrase_ngram_range: tuple = (1, 2)
):
    """
    Extract top keyphrases from text using KeyBERT.
    Returns a list of dicts with keyword and score.
    """
    if not text or not text.strip():
        return []

    keywords = keyword_model.extract_keywords(
        text,
        keyphrase_ngram_range=keyphrase_ngram_range,
        stop_words="english",
        top_n=top_n
    )

    return [
        {
            "keyword": kw,
            "score": float(score)
        }
        for kw, score in keywords
    ]