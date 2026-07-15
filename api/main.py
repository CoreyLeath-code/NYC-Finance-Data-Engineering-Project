"""Validated inference API with operational health and Prometheus telemetry."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Annotated, Any

import numpy as np
from fastapi import FastAPI, HTTPException, Request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, ConfigDict, Field
from starlette.responses import Response

app = FastAPI(title="NYC Finance ML Inference API", version="0.2.0")
_model: Any | None = None

REQUESTS = Counter("api_http_requests_total", "HTTP requests", ("method", "path", "status"))
LATENCY = Histogram("api_http_request_duration_seconds", "HTTP request latency", ("method", "path"))


def _get_model() -> Any:
    global _model
    if _model is None:
        import joblib

        model_path = Path(os.environ.get("MODEL_PATH", "models/model.pkl"))
        if not model_path.is_file():
            raise FileNotFoundError(f"Model file not found at '{model_path}'")
        _model = joblib.load(model_path)
    return _model


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    features: Annotated[list[float], Field(min_length=1, max_length=512)]


class PredictionResponse(BaseModel):
    prediction: float


@app.middleware("http")
async def observe(request: Request, call_next: Any) -> Response:
    started = time.perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    REQUESTS.labels(request.method, path, response.status_code).inc()
    LATENCY.labels(request.method, path).observe(time.perf_counter() - started)
    return response


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "API running"}


@app.get("/healthz", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz", tags=["operations"])
def ready() -> dict[str, str]:
    model_path = Path(os.environ.get("MODEL_PATH", "models/model.pkl"))
    return {"status": "ready" if model_path.is_file() else "degraded"}


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictionResponse)
def predict(data: PredictionRequest) -> PredictionResponse:
    try:
        model = _get_model()
        prediction = model.predict(np.asarray(data.features, dtype=float).reshape(1, -1))[0]
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="Invalid feature vector") from exc
    return PredictionResponse(prediction=float(prediction))
