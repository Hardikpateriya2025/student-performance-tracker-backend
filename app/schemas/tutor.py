from pydantic import BaseModel


class TutorQuestion(BaseModel):
    question: str


class TutorAnswer(BaseModel):
    student_id: int
    question: str
    answer: str
