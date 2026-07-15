"""Validated, observable ETL primitives for NYC finance time-series data."""

from __future__ import annotations

import logging
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

RAW_PATH = os.environ.get("RAW_DATA_PATH", "data/raw/nyc_finance_synthetic.csv")
PROCESSED_PATH = os.environ.get("PROCESSED_DATA_PATH", "data/processed/nyc_finance_processed.csv")
REQUIRED_COLUMNS = {"timestamp", "open", "close", "volume"}


@dataclass(frozen=True)
class PipelineMetrics:
    input_rows: int
    output_rows: int
    duplicate_rows_removed: int
    null_cells: int
    elapsed_seconds: float

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    """Load a CSV and enforce the minimum research data contract."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"Raw data file not found: {source}")

    frame = pd.read_csv(source)
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError("Input dataset is empty")
    return frame


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize timestamps, reject invalid values, deduplicate, and derive returns."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    output = df.copy()
    output["timestamp"] = pd.to_datetime(output["timestamp"], errors="raise", utc=True)
    for column in ("open", "close", "volume"):
        output[column] = pd.to_numeric(output[column], errors="raise")

    if (output["open"] <= 0).any():
        raise ValueError("open must be greater than zero")
    if (output["volume"] < 0).any():
        raise ValueError("volume must be non-negative")

    output = output.drop_duplicates().sort_values("timestamp").reset_index(drop=True)
    output["return"] = (output["close"] - output["open"]) / output["open"]
    output["day_of_week"] = output["timestamp"].dt.day_name()
    return output


def run_pipeline(input_path: str = RAW_PATH, output_path: str = PROCESSED_PATH) -> PipelineMetrics:
    """Execute ETL and return an auditable metrics record."""
    started = time.perf_counter()
    raw = load_raw(input_path)
    transformed = transform(raw)
    save_processed(transformed, output_path)
    return PipelineMetrics(
        input_rows=len(raw),
        output_rows=len(transformed),
        duplicate_rows_removed=len(raw) - len(transformed),
        null_cells=int(transformed.isna().sum().sum()),
        elapsed_seconds=round(time.perf_counter() - started, 6),
    )


def save_processed(df: pd.DataFrame, path: str = PROCESSED_PATH) -> None:
    """Persist atomically enough for a single-process local pipeline."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    df.to_csv(temporary, index=False)
    temporary.replace(destination)
    logger.info("Saved %d rows to %s", len(df), destination)
