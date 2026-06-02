# Real-Time Anomaly Detection Pipeline

Kafka + PySpark streaming project for detecting industrial turbine sensor anomalies with an Isolation Forest model.

This repo includes a local runnable simulation and production-oriented streaming files so it is useful both for demos and GitHub review.

## Features

- Synthetic turbine telemetry generator
- Isolation Forest training pipeline
- Local batch/stream simulation for quick demos
- Kafka producer skeleton
- PySpark Structured Streaming job skeleton
- Metrics for detection rate and false positive rate
- Docker Compose for Kafka
- Tests and GitHub Actions CI

## Architecture

```text
Telemetry Sensors -> Kafka Topic -> PySpark Streaming -> Feature Pipeline -> Isolation Forest -> Alerts Sink
```

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m src.train_model --model-path models/isolation_forest.joblib
python -m src.local_stream_demo --model-path models/isolation_forest.joblib
```

Run tests:

```bash
pytest
```

## Kafka Demo

Start Kafka:

```bash
docker compose up -d
```

Publish simulated telemetry:

```bash
python -m src.kafka_producer --topic turbine-telemetry
```

Run the Spark job after installing Spark locally:

```bash
spark-submit src/spark_streaming_job.py
```

## Reported Outcome

The resume claim is represented as an experiment target:

- 99% detection rate
- 0.5% false positive rate
- Sub-second scoring latency
- 3 months of streaming data in production-style evaluation

The included synthetic demo provides repeatable local validation; real metrics should be recomputed on actual deployment telemetry.
