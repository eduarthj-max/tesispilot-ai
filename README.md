from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
    university: Optional[str] = None
    academic_level: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str]
    university: Optional[str]
    academic_level: Optional[str]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChapterBase(BaseModel):
    title: str
    chapter_type: Optional[str] = "section"
    order_index: Optional[int] = 0
    content: Optional[str] = ""


class ChapterCreate(ChapterBase):
    thesis_id: UUID


class ChapterResponse(ChapterBase):
    id: UUID
    thesis_id: UUID

    class Config:
        orm_mode = True


class ThesisBase(BaseModel):
    title: str
    topic: Optional[str] = None
    abstract: Optional[str] = None


class ThesisCreate(ThesisBase):
    pass


class ThesisUpdate(BaseModel):
    title: Optional[str]
    topic: Optional[str]
    abstract: Optional[str]
    problem_statement: Optional[str]
    justification: Optional[str]
    research_questions: Optional[str]
    objectives: Optional[str]
    hypothesis: Optional[str]


class ThesisResponse(ThesisBase):
    id: UUID
    status: Optional[str] = "draft"
    chapters: List[ChapterResponse] = []

    class Config:
        orm_mode = True


class ZoteroAuthor(BaseModel):
    name: str
    type: Optional[str] = None


class ZoteroReference(BaseModel):
    key: Optional[str] = None
    title: str
    item_type: Optional[str] = None
    publication_year: Optional[int] = None
    authors: List[ZoteroAuthor] = []
    url: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    source: Optional[str] = None


# Version schemas
class VersionCreate(BaseModel):
    content: str


class VersionResponse(BaseModel):
    id: UUID
    chapter_id: UUID
    content: str
    created_at: Optional[str]

    class Config:
        orm_mode = True


path":"backend/app/schemas.py