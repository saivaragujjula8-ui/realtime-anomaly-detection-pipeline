import argparse
import json
import time

from kafka import KafkaProducer

from .generate_data import generate_reading


def publish(topic: str, bootstrap_servers: str, interval_seconds: float) -> None:
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )
    while True:
        producer.send(topic, generate_reading(anomaly_rate=0.03).to_dict())
        producer.flush()
        time.sleep(interval_seconds)


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish synthetic turbine telemetry to Kafka.")
    parser.add_argument("--topic", default="turbine-telemetry")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    parser.add_argument("--interval-seconds", type=float, default=0.1)
    args = parser.parse_args()
    publish(args.topic, args.bootstrap_servers, args.interval_seconds)


if __name__ == "__main__":
    main()
