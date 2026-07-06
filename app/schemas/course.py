from pydantic import BaseModel
from typing import Optional


class CourseCreate(BaseModel):
    name: str
    teacher_id: Optional[int] = None


class CourseOut(BaseModel):
    id: int
    name: str
    teacher_id: Optional[int]

    class Config:
        from_attributes = True
