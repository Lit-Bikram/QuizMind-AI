import requests  # type: ignore
from app.core.config import settings


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def generate_topic_study_content(topic: str) -> str:
    """
    Generate a study-ready synthetic content block for a topic when no PDF is provided.

    This content acts like a pseudo-document and is later passed through the same
    retrieval + MCQ generation pipeline as PDF-extracted text.
    """
    clean_topic = topic.strip()

    if not clean_topic:
        raise ValueError("Topic cannot be empty for topic-only content generation.")

    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert educational content writer.

Create a high-quality, study-ready knowledge summary for the topic: "{clean_topic}"

Your output will be used as source material for a quiz generation system.

Requirements:
- Write clear, accurate, educational content
- Cover the core concepts, important subtopics, and essential terminology
- Include key definitions, comparisons, and practical applications where relevant
- Use concise but informative paragraphs
- Avoid fluff, repetition, and unsupported speculation
- Do NOT generate quiz questions
- Do NOT use bullet-point answer choices
- Do NOT include any MCQ format
- Aim for approximately 1200 to 2000 words
- Make the content rich enough to support multiple conceptual and application-based MCQs

Return only the educational content.
""".strip()

    payload = {
        "model": GROQ_MODEL,
        "temperature": 0.4,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You generate high-quality educational study material for topic-based learning. "
                    "Return only the educational content with no markdown wrappers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        GROQ_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()
    content = data["choices"][0]["message"]["content"].strip()

    if not content:
        raise ValueError(f"Failed to generate topic study content for topic: {clean_topic}")

    return content