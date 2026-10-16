from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.services import ai_service
from pydantic import BaseModel

router = APIRouter()

class GenerateProblemRequest(BaseModel):
    topic: str | None = None
    context: str | None = ""


@router.post("/theses/{thesis_id}/generate-problem")
def generate_problem_for_thesis(thesis_id: str, payload: GenerateProblemRequest, db: Session = Depends(get_db)):
    thesis = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not thesis:
        raise HTTPException(status_code=404, detail="Thesis not found")

    topic = payload.topic or thesis.topic or ""
    context = payload.context or ""

    result = ai_service.generate_problem(topic=topic, context=context)

    # If the service returned text, save it to the thesis.problem_statement (best-effort)
    text = result.get("text") if isinstance(result, dict) else None
    if text:
        thesis.problem_statement = text
        db.add(thesis)
        db.commit()
        db.refresh(thesis)

    return {"ok": True, "ai": result, "thesis": {"id": thesis.id, "problem_statement": thesis.problem_statement}}


class ReviewRequest(BaseModel):
    text: str | None = None


@router.post("/chapters/{chapter_id}/review")
def review_chapter(chapter_id: str, payload: ReviewRequest, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    text_to_review = payload.text or chapter.content or ""
    if not text_to_review:
        raise HTTPException(status_code=400, detail="No text to review")

    result = ai_service.review_chapter_text(text_to_review)
    return {"ok": True, "ai": result}
