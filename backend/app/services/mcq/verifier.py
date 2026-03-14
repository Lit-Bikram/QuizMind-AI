from typing import Dict, List
import re


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _tokenize_meaningful(text: str) -> List[str]:
    """
    Extract meaningful alphabetic tokens (length >= 4)
    """
    return re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())


def _jaccard_overlap(tokens_a: List[str], tokens_b: List[str]) -> float:
    set_a = set(tokens_a)
    set_b = set(tokens_b)

    if not set_a or not set_b:
        return 0.0

    return len(set_a & set_b) / len(set_a | set_b)


def _option_text_for_label(options: List[Dict], label: str) -> str:
    for opt in options:
        if opt.get("label") == label:
            return str(opt.get("text", "")).strip()
    return ""


def _has_duplicate_options(options: List[Dict]) -> bool:
    texts = [str(opt.get("text", "")).strip().lower() for opt in options]
    return len(texts) != len(set(texts))


def _extract_named_terms(text: str) -> List[str]:
    """
    Heuristic for important terms / abbreviations / proper-like entities.
    """
    terms = set()

    # Common medical/academic abbreviations or uppercase tokens
    for match in re.findall(r"\b[A-Z]{2,6}\b", text):
        terms.add(match)

    # Capitalized multi-word terms (simple heuristic)
    for match in re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\b", text):
        terms.add(match)

    return list(terms)


def verify_mcq(mcq: Dict, focused_context: str) -> Dict:
    """
    Returns:
    {
      ...original fields,
      "confidence_score": float,
      "is_verified": bool,
      "verification_notes": [...]
    }
    """
    notes = []
    score = 1.0

    question = str(mcq.get("question", "")).strip()
    explanation = str(mcq.get("explanation", "")).strip()
    options = mcq.get("options", [])
    correct_answer = str(mcq.get("correct_answer", "")).strip().upper()

    # Basic structure checks
    if len(question) < 12:
        score -= 0.20
        notes.append("Question is too short.")

    if len(explanation) < 10:
        score -= 0.15
        notes.append("Explanation is too short.")

    if not isinstance(options, list) or len(options) != 4:
        score -= 0.40
        notes.append("Options are malformed or not exactly 4.")

    if _has_duplicate_options(options):
        score -= 0.25
        notes.append("Duplicate option texts detected.")

    correct_option_text = _option_text_for_label(options, correct_answer)
    if not correct_option_text:
        score -= 0.40
        notes.append("Correct answer label does not map to an option.")

    # Context grounding
    context_tokens = _tokenize_meaningful(focused_context)
    answer_tokens = _tokenize_meaningful(correct_option_text)
    explanation_tokens = _tokenize_meaningful(explanation)
    question_tokens = _tokenize_meaningful(question)

    answer_overlap = _jaccard_overlap(answer_tokens, context_tokens)
    explanation_overlap = _jaccard_overlap(explanation_tokens, context_tokens)
    question_overlap = _jaccard_overlap(question_tokens, context_tokens)

    if answer_overlap == 0:
        score -= 0.20
        notes.append("Correct answer has no token overlap with context.")

    elif answer_overlap < 0.05:
        score -= 0.10
        notes.append("Correct answer has weak overlap with context.")

    if explanation_overlap == 0:
        score -= 0.15
        notes.append("Explanation has no token overlap with context.")

    elif explanation_overlap < 0.03:
        score -= 0.08
        notes.append("Explanation has weak overlap with context.")

    if question_overlap == 0:
        score -= 0.10
        notes.append("Question has no token overlap with context.")

    # Internal consistency heuristic:
    # If explanation mentions many named terms not present in correct option,
    # the answer may be incomplete or mismatched.
    answer_named = set(_extract_named_terms(correct_option_text))
    explanation_named = set(_extract_named_terms(explanation))

    extra_named_terms = explanation_named - answer_named

    # Example: explanation says LBD, PDD, FTD, VaD but option has only 3
    if len(extra_named_terms) >= 2:
        score -= 0.15
        notes.append(
            "Explanation mentions additional named terms not reflected in the correct option."
        )

    # Clamp score
    score = max(0.0, min(1.0, round(score, 2)))

    # Threshold
    is_verified = score >= 0.65

    return {
        **mcq,
        "confidence_score": score,
        "is_verified": is_verified,
        "verification_notes": notes
    }


def verify_mcqs(mcqs: List[Dict], focused_context: str) -> List[Dict]:
    return [verify_mcq(mcq, focused_context) for mcq in mcqs]