from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models, schemas
from app.services import ai_service
from pydantic import BaseModel

router = APIRouter()

class VersionCreate(BaseModel):
    content: str

@router.post("/chapters/{chapter_id}/versions")
def create_version(chapter_id: str, payload: VersionCreate, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    ver = models.Version(chapter_id=chapter_id, content=payload.content)
    db.add(ver)
    db.commit()
    db.refresh(ver)
    return {"ok": True, "version": {"id": ver.id, "created_at": ver.created_at, "content": ver.content}}

@router.get("/chapters/{chapter_id}/versions")
def list_versions(chapter_id: str, db: Session = Depends(get_db)):
    items = db.query(models.Version).filter(models.Version.chapter_id == chapter_id).order_by(models.Version.created_at.desc()).all()
    return [{"id": v.id, "created_at": v.created_at, "content": v.content} for v in items]

@router.post("/chapters/{chapter_id}/summarize")
def summarize_chapter(chapter_id: str, payload: VersionCreate, db: Session = Depends(get_db)):
    chapter = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    text = payload.content or chapter.content or ""
    result = ai_service.summarize_text(text)
    return {"ok": True, "ai": result}

@router.get("/theses/{thesis_id}/progress")
def thesis_progress(thesis_id: str, db: Session = Depends(get_db)):
    thesis = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not thesis:
        raise HTTPException(status_code=404, detail="Thesis not found")
    chapters = db.query(models.Chapter).filter(models.Chapter.thesis_id == thesis_id).all()
    if len(chapters) == 0:
        return {"percent": 0, "chapters_total": 0, "chapters_filled": 0}
    total = len(chapters)
    filled = sum(1 for c in chapters if c.content and c.content.strip())
    percent = int((filled / total) * 100)
    return {"percent": percent, "chapters_total": total, "chapters_filled": filled}
