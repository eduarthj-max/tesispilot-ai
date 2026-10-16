from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app import models
from app.core import security
from app.schemas import UserCreate, UserResponse, Token

router = APIRouter()

@router.post('/register', response_model=UserResponse)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = models.User(
        email=payload.email,
        full_name=payload.full_name,
        university=payload.university,
        academic_level=payload.academic_level,
    )
    user.password_hash = security.get_password_hash(payload.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post('/login', response_model=Token)
def login_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not security.verify_password(payload.password, user.password_hash or ''):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    access_token = security.create_access_token({'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/me', response_model=UserResponse)
def get_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user
