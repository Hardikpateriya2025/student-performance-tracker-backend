"""
Generates a synthetic student performance dataset for ML training.
Run this once to create app/ml/data/synthetic_students.csv

Why synthetic data: our real database has only a couple of students so far.
A model trained on 2-3 rows would be meaningless. This script creates
thousands of realistic student records with genuine, sensible correlations
(higher attendance + consistent past scores -> higher future scores, with
natural noise), so the model actually learns a real pattern. At prediction
time, the trained model is applied to REAL student data from our database.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

N_STUDENTS = 2000

def generate_dataset(n=N_STUDENTS):
    # Base ability: each student has an underlying "true skill" level (0-100)
    true_skill = np.clip(np.random.normal(65, 15, n), 10, 100)

    # Attendance is correlated with skill (engaged students attend more) + noise
    attendance = np.clip(true_skill * 0.7 + np.random.normal(20, 12, n), 30, 100)

    # Past average score: close to true skill, with its own noise (measurement variance)
    past_avg_score = np.clip(true_skill + np.random.normal(0, 8, n), 0, 100)

    # Score trend: is the student improving (+) or declining (-) recently?
    score_trend = np.random.normal(0, 6, n)

    # Study hours per week (another realistic feature)
    study_hours = np.clip(np.random.normal(8, 4, n), 0, 30)

    # TARGET: next exam score.
    # Driven by true skill, attendance, recent trend, study hours, plus noise.
    next_score = (
        0.55 * true_skill
        + 0.20 * attendance
        + 0.15 * study_hours * 2.0   # scaled contribution
        + 0.5 * score_trend
        + np.random.normal(0, 6, n)
    )
    next_score = np.clip(next_score, 0, 100)

    # at_risk label: 1 if next_score would be a fail (< 40), else 0
    at_risk = (next_score < 40).astype(int)

    df = pd.DataFrame({
        "past_avg_score": past_avg_score.round(2),
        "attendance_percent": attendance.round(2),
        "score_trend": score_trend.round(2),
        "study_hours_per_week": study_hours.round(2),
        "next_score": next_score.round(2),
        "at_risk": at_risk,
    })
    return df


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("app/ml/data/synthetic_students.csv", index=False)
    print(f"Generated {len(df)} synthetic student records.")
    print(df.describe())
    print(f"\nAt-risk rate: {df['at_risk'].mean():.1%}")
