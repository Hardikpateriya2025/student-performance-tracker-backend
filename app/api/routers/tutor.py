from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.student import Student
from app.models.user import User
from app.ml.tutor import ask_tutor
from app.schemas.tutor import TutorQuestion, TutorAnswer

router = APIRouter(prefix="/tutor", tags=["genai-tutor"])


@router.post("/{student_id}", response_model=TutorAnswer)
def tutor_chat(
    student_id: int,
    payload: TutorQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        answer = ask_tutor(db, student_id, payload.question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Tutor service error: {str(e)}")

    return TutorAnswer(student_id=student_id, question=payload.question, answer=answer)
