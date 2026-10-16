from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app import models, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ThesisResponse)
def create_thesis(payload: schemas.ThesisCreate, db: Session = Depends(get_db)):
    db_thesis = models.Thesis(**payload.dict())
    db.add(db_thesis)
    db.commit()
    db.refresh(db_thesis)
    return db_thesis

@router.get("/", response_model=List[schemas.ThesisResponse])
def list_theses(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    items = db.query(models.Thesis).offset(skip).limit(limit).all()
    return items

@router.get("/{thesis_id}", response_model=schemas.ThesisResponse)
def get_thesis(thesis_id: str, db: Session = Depends(get_db)):
    t = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Thesis not found")
    return t

@router.put("/{thesis_id}", response_model=schemas.ThesisResponse)
def update_thesis(thesis_id: str, payload: schemas.ThesisUpdate, db: Session = Depends(get_db)):
    t = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Thesis not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(t, k, v)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.delete("/{thesis_id}")
def delete_thesis(thesis_id: str, db: Session = Depends(get_db)):
    t = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Thesis not found")
    db.delete(t)
    db.commit()
    return {"detail": "deleted"}
