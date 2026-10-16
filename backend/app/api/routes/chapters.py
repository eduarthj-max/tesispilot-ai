from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ChapterResponse)
def create_chapter(payload: schemas.ChapterCreate, db: Session = Depends(get_db)):
    thesis = db.query(models.Thesis).filter(models.Thesis.id == str(payload.thesis_id)).first()
    if not thesis:
        raise HTTPException(status_code=404, detail="Thesis not found")
    ch = models.Chapter(**payload.dict())
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch

@router.get("/by-thesis/{thesis_id}", response_model=List[schemas.ChapterResponse])
def list_chapters(thesis_id: str, db: Session = Depends(get_db)):
    items = db.query(models.Chapter).filter(models.Chapter.thesis_id == thesis_id).order_by(models.Chapter.order_index).all()
    return items

@router.get("/{chapter_id}", response_model=schemas.ChapterResponse)
def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    c = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return c

@router.put("/{chapter_id}", response_model=schemas.ChapterResponse)
def update_chapter(chapter_id: str, payload: schemas.ChapterBase, db: Session = Depends(get_db)):
    c = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Chapter not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(c, k, v)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{chapter_id}")
def delete_chapter(chapter_id: str, db: Session = Depends(get_db)):
    c = db.query(models.Chapter).filter(models.Chapter.id == chapter_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Chapter not found")
    db.delete(c)
    db.commit()
    return {"detail": "deleted"}
