from fastapi import APIRouter # type: ignore
from sqlalchemy import text # type: ignore

from app.core.config import settings
from app.core.database import engine

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Backend is healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


@router.get("/health/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "details": str(e)
        }