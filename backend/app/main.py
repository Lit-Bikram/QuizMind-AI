from fastapi import FastAPI #type: ignore
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware #type: ignore
import os
from dotenv import load_dotenv #type: ignore


load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI(
    title="AI Quiz Generator Backend",
    description="RAG-based MCQ generation backend using FastAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "AI Quiz Generator Backend is running"
    }