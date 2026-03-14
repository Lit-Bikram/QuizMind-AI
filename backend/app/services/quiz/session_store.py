from typing import Dict, Any
import uuid


# In-memory store for MVP
QUIZ_SESSIONS: Dict[str, Dict[str, Any]] = {}


def create_quiz_session(
    query: str,
    original_filename: str,
    mcqs: list
) -> Dict[str, Any]:
    session_id = str(uuid.uuid4())

    QUIZ_SESSIONS[session_id] = {
        "session_id": session_id,
        "query": query,
        "original_filename": original_filename,
        "mcqs": mcqs
    }

    return QUIZ_SESSIONS[session_id]


def get_quiz_session(session_id: str) -> Dict[str, Any] | None:
    return QUIZ_SESSIONS.get(session_id)