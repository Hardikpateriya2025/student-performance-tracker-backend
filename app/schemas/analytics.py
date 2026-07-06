from pydantic import BaseModel
from typing import List, Optional


class StudentAverage(BaseModel):
    student_id: int
    roll_number: str
    average_score: float
    average_attendance: Optional[float]


class CoursePerformance(BaseModel):
    course_id: int
    course_name: str
    average_score: float
    highest_score: float
    lowest_score: float
    total_submissions: int


class ClassOverview(BaseModel):
    class_name: str
    student_count: int
    average_score: float
    pass_rate: float   # percentage scoring >= 40


class StudentTrendPoint(BaseModel):
    date: str
    score: float
    exam_type: str
    course_name: str
