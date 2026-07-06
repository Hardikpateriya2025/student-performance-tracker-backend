"""
Loads trained models once at import time, and computes live predictions
from a student's REAL grade/attendance history stored in our database.
"""
import os
import joblib
import numpy as np
from sqlalchemy.orm import Session

from app.models.grade import Grade

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

_reg_model = joblib.load(os.path.join(MODEL_DIR, "score_regressor.joblib"))
_clf_model = joblib.load(os.path.join(MODEL_DIR, "risk_classifier.joblib"))
_features = joblib.load(os.path.join(MODEL_DIR, "features.joblib"))


def compute_features_for_student(db: Session, student_id: int) -> dict | None:
    grades = (
        db.query(Grade)
        .filter(Grade.student_id == student_id)
        .order_by(Grade.date)
        .all()
    )
    if not grades:
        return None

    scores = [g.score for g in grades]
    attendances = [g.attendance_percent for g in grades if g.attendance_percent is not None]

    past_avg_score = float(np.mean(scores))
    attendance_percent = float(np.mean(attendances)) if attendances else 75.0

    if len(scores) >= 2:
        score_trend = float((scores[-1] - scores[0]) / len(scores))
    else:
        score_trend = 0.0

    study_hours_per_week = 8.0

    return {
        "past_avg_score": past_avg_score,
        "attendance_percent": attendance_percent,
        "score_trend": score_trend,
        "study_hours_per_week": study_hours_per_week,
    }


def predict_for_student(db: Session, student_id: int) -> dict | None:
    features = compute_features_for_student(db, student_id)
    if features is None:
        return None

    X = np.array([[features[f] for f in _features]])

    predicted_score = float(_reg_model.predict(X)[0])
    at_risk_prob = float(_clf_model.predict_proba(X)[0][1])
    at_risk = bool(_clf_model.predict(X)[0])

    return {
        "predicted_next_score": round(predicted_score, 1),
        "at_risk": at_risk,
        "at_risk_probability": round(at_risk_prob, 3),
        "features_used": {k: round(v, 2) for k, v in features.items()},
    }
