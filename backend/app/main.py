from fastapi import FastAPI #type: ignore
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware #type: ignore

app = FastAPI(
    title="AI Quiz Generator Backend",
    description="RAG-based MCQ generation backend using FastAPI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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