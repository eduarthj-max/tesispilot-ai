from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app import models, schemas
from app.core.security import get_current_user_optional

router = APIRouter()

@router.post("/", response_model=schemas.ThesisResponse)
def create_thesis(payload: schemas.ThesisCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_optional)):
    data = payload.dict()
    db_thesis = models.Thesis(**data)
    if current_user:
        db_thesis.user_id = current_user.id
    db.add(db_thesis)
    db.commit()
    db.refresh(db_thesis)
    return db_thesis

@router.get("/", response_model=List[schemas.ThesisResponse])
def list_theses(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_optional)):
    query = db.query(models.Thesis)
    if current_user:
        query = query.filter(models.Thesis.user_id == current_user.id)
    items = query.offset(skip).limit(limit).all()
    return items

@router.get("/{thesis_id}", response_model=schemas.ThesisResponse)
def get_thesis(thesis_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_optional)):
    t = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Thesis not found")
    if current_user and t.user_id and t.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return t

@router.put("/{thesis_id}", response_model=schemas.ThesisResponse)
def update_thesis(thesis_id: str, payload: schemas.ThesisUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_optional)):
    t = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Thesis not found")
    if current_user and t.user_id and t.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(t, k, v)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.delete("/{thesis_id}")
def delete_thesis(thesis_id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user_optional)):
    t = db.query(models.Thesis).filter(models.Thesis.id == thesis_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Thesis not found")
    if current_user and t.user_id and t.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(t)
    db.commit()
    return {"detail": "deleted"}
