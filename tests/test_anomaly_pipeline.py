from pathlib import Path

from src.generate_data import generate_dataset
from src.local_stream_demo import run_demo
from src.train_model import train


def test_train_and_run_demo(tmp_path: Path) -> None:
    model_path = tmp_path / "model.joblib"
    alert_path = tmp_path / "alerts.jsonl"

    train(str(model_path), rows=300)
    alerts = run_demo(str(model_path), str(alert_path), events=20)

    assert model_path.exists()
    assert alert_path.exists()
    assert isinstance(alerts, list)


def test_generator_has_expected_columns() -> None:
    frame = generate_dataset(rows=10)
    assert {"rpm", "vibration", "temperature_c", "pressure_bar", "power_kw", "is_anomaly"}.issubset(frame.columns)
