from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    exam_type = Column(String, nullable=False)       # "quiz", "midterm", "final"
    score = Column(Float, nullable=False)             # 0-100
    attendance_percent = Column(Float, nullable=True) # feature for ML later
    date = Column(Date, nullable=False)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
