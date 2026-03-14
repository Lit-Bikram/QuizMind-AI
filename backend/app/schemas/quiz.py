from pydantic import BaseModel, Field # type: ignore
from typing import List, Dict, Optional

from app.schemas.mcq import MCQItem


class QuizCreateRequest(BaseModel):
    query: str
    original_filename: str
    mcqs: List[MCQItem]


class QuizCreateResponse(BaseModel):
    message: str
    session_id: str
    query: str
    original_filename: str
    total_questions: int
    mcqs: List[MCQItem]


class QuizSubmitRequest(BaseModel):
    session_id: str
    answers: Dict[str, str] = Field(
        ...,
        description="Map of question_id to selected option label, e.g. {'1': 'B', '2': 'A'}"
    )


class QuestionReview(BaseModel):
    question_id: str
    question: str
    user_answer: Optional[str]
    correct_answer: str
    is_correct: bool
    difficulty: str
    explanation: str
    confidence_score: float
    is_verified: bool


class DifficultyStats(BaseModel):
    total: int
    correct: int
    accuracy: float


class QuizSubmitResponse(BaseModel):
    message: str
    session_id: str
    total_questions: int
    correct_count: int
    incorrect_count: int
    percentage: float
    difficulty_breakdown: Dict[str, DifficultyStats]
    question_reviews: List[QuestionReview]
    weak_areas: List[str]