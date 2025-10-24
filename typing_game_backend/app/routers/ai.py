from fastapi import APIRouter, Query
from ..services.ai_text import generate_text

router = APIRouter(prefix="/ai")

@router.get("/generate_text")
def get_text(level: str = Query("beginner"), topic: str = Query(None)):
    text = generate_text(level, topic)
    return {"text": text}