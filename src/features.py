import pandas as pd


FEATURE_COLUMNS = ["rpm", "vibration", "temperature_c", "pressure_bar", "power_kw"]


def select_features(frame: pd.DataFrame) -> pd.DataFrame:
    missing = [column for column in FEATURE_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing feature columns: {missing}")
    return frame[FEATURE_COLUMNS]
