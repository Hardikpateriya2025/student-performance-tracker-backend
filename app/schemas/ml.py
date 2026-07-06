from pydantic import BaseModel
from typing import Dict


class PredictionOut(BaseModel):
    student_id: int
    predicted_next_score: float
    at_risk: bool
    at_risk_probability: float
    features_used: Dict[str, float]
