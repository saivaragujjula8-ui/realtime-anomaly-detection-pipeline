from dataclasses import dataclass, asdict
import random
import time

import pandas as pd


@dataclass(frozen=True)
class TurbineReading:
    timestamp_ms: int
    turbine_id: str
    rpm: float
    vibration: float
    temperature_c: float
    pressure_bar: float
    power_kw: float
    is_anomaly: int

    def to_dict(self) -> dict:
        return asdict(self)


def generate_reading(turbine_id: str = "TURBINE-001", anomaly_rate: float = 0.02) -> TurbineReading:
    is_anomaly = int(random.random() < anomaly_rate)
    rpm = random.gauss(1800, 45)
    vibration = random.gauss(0.35, 0.06)
    temperature = random.gauss(78, 4)
    pressure = random.gauss(22, 1.2)
    power = random.gauss(1450, 80)

    if is_anomaly:
        rpm += random.choice([-1, 1]) * random.uniform(180, 420)
        vibration += random.uniform(0.35, 0.9)
        temperature += random.uniform(14, 35)
        pressure += random.choice([-1, 1]) * random.uniform(4, 8)

    return TurbineReading(
        timestamp_ms=int(time.time() * 1000),
        turbine_id=turbine_id,
        rpm=round(rpm, 2),
        vibration=round(vibration, 4),
        temperature_c=round(temperature, 2),
        pressure_bar=round(pressure, 2),
        power_kw=round(power, 2),
        is_anomaly=is_anomaly,
    )


def generate_dataset(rows: int = 2000, anomaly_rate: float = 0.02) -> pd.DataFrame:
    return pd.DataFrame([generate_reading(anomaly_rate=anomaly_rate).to_dict() for _ in range(rows)])
