from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.grade import Grade
from app.models.student import Student
from app.models.course import Course
from app.models.user import User
from app.schemas.analytics import (
    StudentAverage,
    CoursePerformance,
    ClassOverview,
    StudentTrendPoint,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

PASS_THRESHOLD = 40.0


@router.get("/student-averages", response_model=List[StudentAverage])
def student_averages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = (
        db.query(
            Student.id.label("student_id"),
            Student.roll_number.label("roll_number"),
            func.avg(Grade.score).label("average_score"),
            func.avg(Grade.attendance_percent).label("average_attendance"),
        )
        .join(Grade, Grade.student_id == Student.id)
        .group_by(Student.id)
        .all()
    )
    return [
        StudentAverage(
            student_id=r.student_id,
            roll_number=r.roll_number,
            average_score=round(r.average_score, 2),
            average_attendance=round(r.average_attendance, 2) if r.average_attendance is not None else None,
        )
        for r in results
    ]


@router.get("/course-performance", response_model=List[CoursePerformance])
def course_performance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = (
        db.query(
            Course.id.label("course_id"),
            Course.name.label("course_name"),
            func.avg(Grade.score).label("average_score"),
            func.max(Grade.score).label("highest_score"),
            func.min(Grade.score).label("lowest_score"),
            func.count(Grade.id).label("total_submissions"),
        )
        .join(Grade, Grade.course_id == Course.id)
        .group_by(Course.id)
        .all()
    )
    return [
        CoursePerformance(
            course_id=r.course_id,
            course_name=r.course_name,
            average_score=round(r.average_score, 2),
            highest_score=r.highest_score,
            lowest_score=r.lowest_score,
            total_submissions=r.total_submissions,
        )
        for r in results
    ]


@router.get("/class-overview", response_model=List[ClassOverview])
def class_overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    classes = db.query(Student.class_name).distinct().all()
    overview = []

    for (class_name,) in classes:
        students_in_class = db.query(Student).filter(Student.class_name == class_name).all()
        student_ids = [s.id for s in students_in_class]

        grades = db.query(Grade).filter(Grade.student_id.in_(student_ids)).all()
        if not grades:
            continue

        avg_score = sum(g.score for g in grades) / len(grades)
        passing = sum(1 for g in grades if g.score >= PASS_THRESHOLD)
        pass_rate = (passing / len(grades)) * 100

        overview.append(
            ClassOverview(
                class_name=class_name,
                student_count=len(students_in_class),
                average_score=round(avg_score, 2),
                pass_rate=round(pass_rate, 2),
            )
        )

    return overview


@router.get("/student-trend/{student_id}", response_model=List[StudentTrendPoint])
def student_trend(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    grades = (
        db.query(Grade, Course.name)
        .join(Course, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .order_by(Grade.date)
        .all()
    )

    return [
        StudentTrendPoint(
            date=str(g.Grade.date),
            score=g.Grade.score,
            exam_type=g.Grade.exam_type,
            course_name=g.name,
        )
        for g in grades
    ]
