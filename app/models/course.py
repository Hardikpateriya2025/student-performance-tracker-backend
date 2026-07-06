from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)          # e.g. "Mathematics"
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    grades = relationship("Grade", back_populates="course")
