import argparse
from pathlib import Path

import joblib
from sklearn.ensemble import IsolationForest

from .features import select_features
from .generate_data import generate_dataset


def train(model_path: str, rows: int = 5000) -> IsolationForest:
    frame = generate_dataset(rows=rows, anomaly_rate=0.01)
    normal_frame = frame[frame["is_anomaly"] == 0]
    model = IsolationForest(n_estimators=150, contamination=0.02, random_state=42)
    model.fit(select_features(normal_frame))

    output = Path(model_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Isolation Forest anomaly detector.")
    parser.add_argument("--model-path", default="models/isolation_forest.joblib")
    parser.add_argument("--rows", type=int, default=5000)
    args = parser.parse_args()
    train(args.model_path, args.rows)


if __name__ == "__main__":
    main()
