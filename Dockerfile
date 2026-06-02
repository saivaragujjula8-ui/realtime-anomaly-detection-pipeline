FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-m", "src.local_stream_demo", "--model-path", "models/isolation_forest.joblib"]
