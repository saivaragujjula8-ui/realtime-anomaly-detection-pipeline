import argparse
import json
from pathlib import Path
import time

import joblib

from .generate_data import generate_reading
from .scoring import score_reading
from .train_model import train


def run_demo(model_path: str, output_path: str = "alerts/local_alerts.jsonl", events: int = 100) -> list[dict]:
    model_file = Path(model_path)
    if not model_file.exists():
        train(str(model_file))

    model = joblib.load(model_file)
    alerts: list[dict] = []
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as handle:
        for _ in range(events):
            reading = generate_reading(anomaly_rate=0.08).to_dict()
            prediction = score_reading(model, reading)
            if prediction.is_anomaly:
                alert = {**reading, "anomaly_score": prediction.anomaly_score}
                alerts.append(alert)
                handle.write(json.dumps(alert) + "\n")
            time.sleep(0.005)
    return alerts


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local streaming anomaly demo.")
    parser.add_argument("--model-path", default="models/isolation_forest.joblib")
    parser.add_argument("--events", type=int, default=100)
    args = parser.parse_args()
    alerts = run_demo(args.model_path, events=args.events)
    print(f"Generated {len(alerts)} alerts")


if __name__ == "__main__":
    main()
