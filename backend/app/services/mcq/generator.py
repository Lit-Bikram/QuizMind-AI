from typing import List, Dict, Any
import json
import re
from app.services.mcq.verifier import verify_mcqs
from app.services.llm.client import generate_mcqs_with_groq


VALID_LABELS = {"A", "B", "C", "D"}
VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def _build_mcq_prompt(
    topic: str,
    query: str,
    focused_context: str,
    num_questions: int = 5
) -> str:
    return f"""
Generate exactly {num_questions} high-quality multiple-choice questions (MCQs) based ONLY on the provided document context.

TOPIC FOCUS:
{topic}

QUESTION INSTRUCTION:
{query}

DOCUMENT CONTEXT:
{focused_context}

IMPORTANT RULES:
1. Questions must be grounded ONLY in the provided context.
2. Do NOT invent facts that are not explicitly supported by the context.
3. Use the TOPIC FOCUS to decide what part of the document the questions should be about.
4. Use the QUESTION INSTRUCTION to control question style, difficulty, and type (e.g. conceptual, application-based, easy, medium, hard).
5. If the QUESTION INSTRUCTION requests content not supported by the DOCUMENT CONTEXT, prioritize correctness and grounding over strict instruction compliance.
6. Each question must have exactly 4 options.
7. Only one option must be correct.
8. The correct answer MUST exactly match one of the option labels: A, B, C, or D.
9. Difficulty MUST be one of: easy, medium, hard.
10. Include:
   - question
   - options (list of 4 objects with label and text)
   - correct_answer (A/B/C/D)
   - difficulty (easy/medium/hard)
   - explanation
11. Avoid generic questions about the pipeline or the system.
12. Focus on the document topic and educational usefulness.
13. Make distractors plausible but clearly incorrect based on the context.
14. Return ONLY valid JSON.
15. Do NOT use markdown fences.

Return JSON in this exact format:
{{
  "mcqs": [
    {{
      "question": "string",
      "options": [
        {{"label": "A", "text": "string"}},
        {{"label": "B", "text": "string"}},
        {{"label": "C", "text": "string"}},
        {{"label": "D", "text": "string"}}
      ],
      "correct_answer": "A",
      "difficulty": "easy",
      "explanation": "string"
    }}
  ]
}}
""".strip()


def _extract_json_block(raw_text: str) -> Dict[str, Any]:
    """
    Safely extract JSON object from model output.
    Handles markdown fences or accidental extra text.
    """
    cleaned = raw_text.strip()

    # Remove markdown fences if any
    cleaned = re.sub(r"^```json", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^```", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Fallback: first JSON object block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError("Could not parse valid JSON from LLM response.")


def _normalize_difficulty(value: str) -> str:
    if not value:
        return "medium"

    value = value.strip().lower()

    mapping = {
        "easy": "easy",
        "beginner": "easy",
        "basic": "easy",

        "medium": "medium",
        "moderate": "medium",
        "intermediate": "medium",

        "hard": "hard",
        "advanced": "hard",
        "difficult": "hard"
    }

    return mapping.get(value, "medium")


def _normalize_options(options: Any) -> List[Dict[str, str]]:
    """
    Ensure options are exactly 4 items labeled A/B/C/D.
    """
    if not isinstance(options, list) or len(options) != 4:
        return []

    normalized = []
    expected_labels = ["A", "B", "C", "D"]

    for idx, opt in enumerate(options):
        if not isinstance(opt, dict):
            return []

        text = str(opt.get("text", "")).strip()
        if not text:
            return []

        normalized.append({
            "label": expected_labels[idx],
            "text": text
        })

    # Reject duplicate option texts
    option_texts = [opt["text"].lower() for opt in normalized]
    if len(set(option_texts)) != 4:
        return []

    return normalized


def _is_question_quality_ok(question: str, explanation: str) -> bool:
    """
    Basic quality filter.
    """
    if not question or len(question.strip()) < 12:
        return False

    if not explanation or len(explanation.strip()) < 10:
        return False

    return True


def _option_text_for_label(options: List[Dict[str, str]], label: str) -> str:
    for opt in options:
        if opt["label"] == label:
            return opt["text"]
    return ""


def _has_context_overlap(answer_text: str, focused_context: str) -> bool:
    """
    Lightweight grounding heuristic:
    if at least one meaningful token from answer appears in focused context,
    treat it as somewhat grounded.
    """
    if not answer_text or not focused_context:
        return False

    answer_tokens = re.findall(r"\b[a-zA-Z]{4,}\b", answer_text.lower())
    context_lower = focused_context.lower()

    for token in answer_tokens:
        if token in context_lower:
            return True

    return False


def _validate_and_clean_mcqs(
    raw_mcqs: Any,
    focused_context: str,
    num_questions: int
) -> List[Dict]:
    """
    Validate and clean MCQs from the LLM.
    Filters bad ones instead of crashing the whole request.
    """
    if not isinstance(raw_mcqs, list):
        return []

    cleaned_mcqs = []

    for item in raw_mcqs:
        if not isinstance(item, dict):
            continue

        question = str(item.get("question", "")).strip()
        explanation = str(item.get("explanation", "")).strip()
        difficulty = _normalize_difficulty(str(item.get("difficulty", "medium")))

        if not _is_question_quality_ok(question, explanation):
            continue

        options = _normalize_options(item.get("options", []))
        if not options:
            continue

        correct_answer = str(item.get("correct_answer", "")).strip().upper()
        if correct_answer not in VALID_LABELS:
            continue

        correct_answer_text = _option_text_for_label(options, correct_answer)
        if not correct_answer_text:
            continue

        # Optional grounding heuristic:
        # If the correct answer doesn't overlap with context at all,
        # skip the question as likely hallucinated / weak.
        if not _has_context_overlap(correct_answer_text, focused_context):
            continue

        cleaned_mcqs.append({
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "difficulty": difficulty,
            "explanation": explanation
        })

        if len(cleaned_mcqs) >= num_questions:
            break

    return cleaned_mcqs


def _fallback_mcq(topic: str) -> Dict:
    """
    Safe fallback if the LLM output is malformed or too weak.
    """
    return {
        "question": f"What is the main focus of the topic '{topic}' in the provided document?",
        "options": [
            {"label": "A", "text": "It is discussed directly in the retrieved context"},
            {"label": "B", "text": "It is unrelated to the document"},
            {"label": "C", "text": "It is only mentioned in file metadata"},
            {"label": "D", "text": "It is excluded from the document entirely"}
        ],
        "correct_answer": "A",
        "difficulty": "easy",
        "explanation": "This fallback question is returned when the LLM output is malformed or insufficiently reliable.",
        "confidence_score": 0.50,
        "is_verified": False,
        "verification_notes": ["Fallback MCQ used due to invalid or low-quality LLM output."]
    }


def generate_mcqs(
    topic: str,
    query: str,
    focused_context: str,
    num_questions: int = 5
) -> List[Dict]:
    """
    Generate MCQs using Groq LLM with:
    - strict prompt
    - JSON extraction
    - validation
    - filtering
    - retry on malformed output
    """
    # Ask the LLM for a few extra questions so filtering/verification
    # can still leave us with the requested final count.
    llm_target = min(num_questions + 3, 25)

    prompt = _build_mcq_prompt(
        topic=topic,
        query=query,
        focused_context=focused_context,
        num_questions=llm_target
    )

    # Try twice max
    attempts = 2
    last_error = None

    for _ in range(attempts):
        try:
            raw_response = generate_mcqs_with_groq(prompt)
            parsed = _extract_json_block(raw_response)

            raw_mcqs = parsed.get("mcqs", [])
            cleaned_mcqs = _validate_and_clean_mcqs(
                raw_mcqs=raw_mcqs,
                focused_context=focused_context,
                num_questions=num_questions
            )

            if cleaned_mcqs:
                verified_mcqs = verify_mcqs(
                    mcqs=cleaned_mcqs,
                    focused_context=focused_context
                )

                # Keep only verified or reasonably confident MCQs
                filtered_mcqs = [
                    mcq for mcq in verified_mcqs
                    if mcq["is_verified"] or mcq["confidence_score"] >= 0.60
                ]

                if filtered_mcqs:
                    return filtered_mcqs[:num_questions]

                # If all fail strict filtering, return verified list anyway
                return verified_mcqs[:num_questions]

            last_error = ValueError("LLM returned no valid MCQs after validation.")

        except Exception as e:
            last_error = e

    # If everything fails, return a safe fallback instead of crashing
    return [_fallback_mcq(topic) for _ in range(num_questions)]