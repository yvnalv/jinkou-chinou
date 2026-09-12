"""Model serving template (FastAPI). Copy into the project as e.g. src/serve.py.

Loads the artifacts written by train_pipeline.template.py (model.joblib + metadata.json) from
MODEL_DIR, applies the SAME engineer_features() used in training (imported from the training
module, so training and serving cannot drift apart), validates requests against the training
schema, returns predictions with the model version, and appends every prediction to a JSONL log
that drift_report.py and model_report.py can analyse once labels arrive.

Run:   MODEL_DIR=models/churn uvicorn serve:app --host 0.0.0.0 --port 8000
Call:  POST /predict {"records": [{"event_date": "2026-09-01", "tenure_months": 12, "plan": "pro", ...}]}
       (raw inputs as they exist at prediction time; engineered features are computed here)

Production notes: run behind a process manager with several workers, put authentication and rate
limiting in front, ship the prediction log to durable storage, and never log raw personal data.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

import importlib

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# One feature-engineering function for training and serving prevents train-serving skew.
# Point FEATURE_MODULE at the module that defines engineer_features(df, time_col).
engineer_features = importlib.import_module(os.environ.get("FEATURE_MODULE", "train")).engineer_features

MODEL_DIR = Path(os.environ.get("MODEL_DIR", "models/latest"))
PREDICTION_LOG = Path(os.environ.get("PREDICTION_LOG", MODEL_DIR / "predictions.jsonl"))
MAX_RECORDS = int(os.environ.get("MAX_RECORDS", "1000"))
LOG_FEATURES = os.environ.get("LOG_FEATURES", "true").lower() == "true"  # set false if inputs hold personal data

model = joblib.load(MODEL_DIR / "model.joblib")
metadata = json.loads((MODEL_DIR / "metadata.json").read_text(encoding="utf-8"))
FEATURES: list[str] = metadata["features"]
NUMERIC = set(metadata["numeric_features"])
MODEL_VERSION = f"{metadata['model_name']}@{metadata['created_at']}"
_log_lock = Lock()

app = FastAPI(title="Model service", version=MODEL_VERSION)


class PredictRequest(BaseModel):
    records: list[dict[str, Any]] = Field(..., min_length=1, max_length=MAX_RECORDS)


class Prediction(BaseModel):
    prediction: Any
    probability: float | None = None


class PredictResponse(BaseModel):
    request_id: str
    model_version: str
    predictions: list[Prediction]


def to_frame(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = engineer_features(pd.DataFrame(records), metadata.get("time_col"))
    missing = [f for f in FEATURES if f not in frame.columns]
    if missing:
        raise HTTPException(status_code=422, detail={"error": "missing inputs", "missing_features": missing})
    incomplete = frame[FEATURES].isna().all(axis=1)
    if incomplete.any():
        raise HTTPException(status_code=422, detail={"error": "records without any feature values",
                                                     "records": incomplete[incomplete].index.tolist()[:20]})
    frame = frame[FEATURES].copy()  # unknown fields are ignored; order matches training
    for col in FEATURES:
        if col in NUMERIC:
            converted = pd.to_numeric(frame[col], errors="coerce")
            bad = frame[col].notna() & converted.isna()
            if bad.any():
                raise HTTPException(status_code=422, detail={"error": f"'{col}' must be numeric",
                                                             "records": bad[bad].index.tolist()[:20]})
            frame[col] = converted
        else:
            frame[col] = frame[col].astype("object")
    return frame


def log_predictions(request_id: str, frame: pd.DataFrame, preds: list[Prediction], latency_ms: float) -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="milliseconds")
    lines = []
    for i, pred in enumerate(preds):
        row = {"timestamp": now, "request_id": request_id, "model_version": MODEL_VERSION,
               "prediction": pred.prediction, "score": pred.probability, "latency_ms": round(latency_ms, 2)}
        if LOG_FEATURES:
            row.update({k: (None if pd.isna(v) else v) for k, v in frame.iloc[i].items()})
        lines.append(json.dumps(row, default=str))
    PREDICTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with _log_lock, PREDICTION_LOG.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_version": MODEL_VERSION}


@app.get("/metadata")
def get_metadata() -> dict:
    keys = ("model_name", "task", "target", "features", "classes", "metric", "test_score", "created_at", "versions")
    return {k: metadata.get(k) for k in keys}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    start = time.perf_counter()
    frame = to_frame(request.records)
    labels = model.predict(frame)
    probs = None
    if metadata["task"] == "classification" and hasattr(model, "predict_proba") and len(metadata.get("classes") or []) == 2:
        probs = model.predict_proba(frame)[:, 1]
    preds = [Prediction(prediction=(label.item() if hasattr(label, "item") else label),
                        probability=None if probs is None else round(float(probs[i]), 6))
             for i, label in enumerate(labels)]
    request_id = str(uuid.uuid4())
    log_predictions(request_id, frame, preds, (time.perf_counter() - start) * 1000)
    return PredictResponse(request_id=request_id, model_version=MODEL_VERSION, predictions=preds)
