from pydantic import BaseModel
from datetime import date as date_type
from typing import Optional


class GradeCreate(BaseModel):
    student_id: int
    course_id: int
    exam_type: str
    score: float
    attendance_percent: Optional[float] = None
    date: date_type


class GradeOut(BaseModel):
    id: int
    student_id: int
    course_id: int
    exam_type: str
    score: float
    attendance_percent: Optional[float]
    date: date_type

    class Config:
        from_attributes = True
