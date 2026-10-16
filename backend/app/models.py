from sqlalchemy import Column, String, Text, TIMESTAMP, func, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.db.session import Base


def gen_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255))
    university = Column(String(255))
    academic_level = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())


class Thesis(Base):
    __tablename__ = "theses"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), nullable=True)
    title = Column(String(255))
    topic = Column(String(255))
    status = Column(String(50), default="draft")
    abstract = Column(Text)
    problem_statement = Column(Text)
    justification = Column(Text)
    research_questions = Column(Text)
    objectives = Column(Text)
    hypothesis = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    chapters = relationship("Chapter", back_populates="thesis", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    thesis_id = Column(UUID(as_uuid=False), ForeignKey("theses.id"))
    title = Column(String(255))
    order_index = Column(Integer, default=0)
    chapter_type = Column(String(100))
    content = Column(Text)
    status = Column(String(50), default="draft")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    thesis = relationship("Thesis", back_populates="chapters")
