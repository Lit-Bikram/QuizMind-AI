import requests # type: ignore
from app.core.config import settings


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def generate_mcqs_with_groq(prompt: str) -> str:
    """
    Sends prompt to Groq and returns raw text response.
    Uses OpenAI-compatible Groq chat completions endpoint.
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "temperature": 0.3,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert educational assessment generator. "
                    "Always return ONLY valid JSON with no markdown, no extra text."
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
    return data["choices"][0]["message"]["content"].strip()