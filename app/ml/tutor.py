"""
GenAI Tutor: builds a context-aware prompt from a student's REAL data
(grades, attendance, ML prediction) and asks Groq's LLM to answer
questions about that specific student.
"""
from groq import Groq
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.grade import Grade
from app.models.course import Course
from app.ml.predictor import predict_for_student

_client = Groq(api_key=settings.GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"


def build_student_context(db: Session, student_id: int) -> str:
    """
    Builds a plain-text summary of a student's real grade history +
    ML prediction, to be injected into the LLM prompt as context.
    """
    grades = (
        db.query(Grade, Course.name)
        .join(Course, Grade.course_id == Course.id)
        .filter(Grade.student_id == student_id)
        .order_by(Grade.date)
        .all()
    )

    if not grades:
        return "This student has no recorded grades yet."

    lines = ["Grade history:"]
    for g, course_name in grades:
        attendance_str = f"{g.attendance_percent}%" if g.attendance_percent is not None else "N/A"
        lines.append(
            f"- {g.date} | {course_name} | {g.exam_type} | Score: {g.score}/100 | Attendance: {attendance_str}"
        )

    prediction = predict_for_student(db, student_id)
    if prediction:
        lines.append("\nAI Prediction:")
        lines.append(f"- Predicted next score: {prediction['predicted_next_score']}/100")
        lines.append(f"- At risk of failing: {'Yes' if prediction['at_risk'] else 'No'}")
        lines.append(f"- Risk probability: {prediction['at_risk_probability'] * 100:.1f}%")

    return "\n".join(lines)


def ask_tutor(db: Session, student_id: int, question: str) -> str:
    context = build_student_context(db, student_id)

    system_prompt = (
        "You are a helpful, encouraging academic tutor assistant for a "
        "Student Performance Tracker app. You answer questions about a "
        "SPECIFIC student using ONLY the real data provided below. "
        "Be concise (3-5 sentences unless asked for more detail), "
        "supportive in tone, and give concrete, actionable advice when "
        "relevant. Do not make up data that isn't in the context."
        f"\n\n--- STUDENT DATA ---\n{context}\n--- END STUDENT DATA ---"
    )

    response = _client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.4,
        max_tokens=400,
    )

    return response.choices[0].message.content
