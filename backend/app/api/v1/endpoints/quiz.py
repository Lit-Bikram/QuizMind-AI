from fastapi import APIRouter, HTTPException  # type: ignore
from app.schemas.quiz import (
    QuizCreateRequest,
    QuizCreateResponse,
    QuizSubmitRequest,
    QuizSubmitResponse,
)
from app.services.quiz.session_store import create_quiz_session, get_quiz_session
from app.services.quiz.scorer import score_quiz

router = APIRouter()


@router.post("/create", response_model=QuizCreateResponse)
def create_quiz(request: QuizCreateRequest):
    session = create_quiz_session(
        query=request.query,
        original_filename=request.original_filename,
        mcqs=[mcq.model_dump() for mcq in request.mcqs],
    )

    return {
        "message": "Quiz session created successfully",
        "session_id": session["session_id"],
        "query": session["query"],
        "original_filename": session["original_filename"],
        "total_questions": len(session["mcqs"]),
        "mcqs": session["mcqs"],
    }


@router.post("/submit", response_model=QuizSubmitResponse)
def submit_quiz(request: QuizSubmitRequest):
    session = get_quiz_session(request.session_id)

    if not session:
        raise HTTPException(status_code=404, detail="Quiz session not found")

    results = score_quiz(
        mcqs=session["mcqs"],
        user_answers=request.answers,
    )

    return {
        "message": "Quiz submitted and scored successfully",
        "session_id": request.session_id,
        **results,
    }