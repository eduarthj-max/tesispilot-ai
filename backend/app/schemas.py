from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


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
