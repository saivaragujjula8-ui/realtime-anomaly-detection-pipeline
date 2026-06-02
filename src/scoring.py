from dataclasses import dataclass

import pandas as pd

from .features import FEATURE_COLUMNS, select_features


@dataclass(frozen=True)
class Prediction:
    is_anomaly: bool
    anomaly_score: float


def score_reading(model, reading: dict) -> Prediction:
    frame = pd.DataFrame([reading])
    prediction = model.predict(select_features(frame))[0]
    score = float(model.decision_function(frame[FEATURE_COLUMNS])[0])
    return Prediction(is_anomaly=prediction == -1, anomaly_score=round(score, 5))
