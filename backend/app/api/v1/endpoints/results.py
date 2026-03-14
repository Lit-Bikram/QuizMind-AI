from fastapi import APIRouter # type: ignore

router = APIRouter()


@router.get("/")
def results_placeholder():
    return {
        "message": "Results endpoint placeholder"
    }