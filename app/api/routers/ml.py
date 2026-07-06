from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.student import Student
from app.models.user import User
from app.ml.predictor import predict_for_student
from app.schemas.ml import PredictionOut

router = APIRouter(prefix="/ml", tags=["machine-learning"])


@router.get("/predict/{student_id}", response_model=PredictionOut)
def predict(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = predict_for_student(db, student_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Student has no grade history to predict from")

    return PredictionOut(student_id=student_id, **result)
