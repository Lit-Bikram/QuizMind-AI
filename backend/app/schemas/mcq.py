from pydantic import BaseModel, Field # type: ignore
from typing import List



class MCQOption(BaseModel):
    label: str = Field(..., description="Option label, e.g., A, B, C, D")
    text: str = Field(..., description="Option text")


class MCQItem(BaseModel):
    question: str
    options: List[MCQOption]
    correct_answer: str = Field(..., description="Correct option label, e.g., A")
    difficulty: str = Field(..., description="easy | medium | hard")
    explanation: str
    confidence_score: float
    is_verified: bool
    verification_notes: List[str]


class MCQGenerationResponse(BaseModel):
    message: str
    original_filename: str
    saved_path: str
    num_pages: int
    text_length: int
    query: str
    chunks_created: int
    keyphrases: list
    focused_context: str
    mcqs: List[MCQItem]