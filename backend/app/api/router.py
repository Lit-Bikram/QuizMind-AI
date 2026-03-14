from fastapi import APIRouter # type: ignore
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.documents import router as documents_router
from app.api.v1.endpoints.quiz import router as quiz_router
from app.api.v1.endpoints.results import router as results_router
from app.api.v1.endpoints.quiz import router as quiz_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(documents_router, prefix="/documents", tags=["Documents"])
api_router.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])
api_router.include_router(results_router, prefix="/results", tags=["Results"])
