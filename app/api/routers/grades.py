from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, require_role, get_current_user
from app.models.grade import Grade
from app.models.user import User, RoleEnum
from app.schemas.grade import GradeCreate, GradeOut

router = APIRouter(prefix="/grades", tags=["grades"])


@router.post("/", response_model=GradeOut)
def create_grade(
    payload: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin, RoleEnum.teacher)),
):
    grade = Grade(**payload.model_dump())
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade


@router.get("/", response_model=List[GradeOut])
def list_grades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Grade).all()


@router.get("/student/{student_id}", response_model=List[GradeOut])
def get_grades_for_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Grade).filter(Grade.student_id == student_id).all()


@router.delete("/{grade_id}")
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(RoleEnum.admin, RoleEnum.teacher)),
):
    grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    db.delete(grade)
    db.commit()
    return {"detail": "Grade deleted"}
