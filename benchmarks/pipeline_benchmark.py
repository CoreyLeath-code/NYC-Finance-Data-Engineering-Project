"""Reproducible in-memory ETL microbenchmark with JSON provenance."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from src.pipelines.etl import transform


def make_dataset(rows: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    opened = rng.uniform(80.0, 120.0, rows)
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2025-01-01", periods=rows, freq="s", tz="UTC"),
            "open": opened,
            "close": opened * (1.0 + rng.normal(0.0, 0.002, rows)),
            "volume": rng.integers(1_000, 500_000, rows),
        }
    )


def benchmark(rows: int, repeats: int, seed: int) -> dict[str, object]:
    source = make_dataset(rows, seed)
    timings: list[float] = []
    for _ in range(repeats):
        started = time.perf_counter()
        result = transform(source)
        timings.append(time.perf_counter() - started)

    median = statistics.median(timings)
    ordered = sorted(timings)
    p95 = ordered[min(len(ordered) - 1, int(0.95 * len(ordered)))]
    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "benchmark": "in-memory ETL transform microbenchmark",
        "dataset": {"synthetic": True, "rows": rows, "seed": seed},
        "protocol": {"repeats": repeats, "warm_cache": True},
        "metrics": {
            "median_seconds": round(median, 6),
            "p95_seconds": round(p95, 6),
            "median_rows_per_second": round(rows / median, 2),
            "output_rows": len(result),
            "null_cells": int(result.isna().sum().sum()),
        },
        "environment": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "samples_seconds": [round(value, 6) for value in timings],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--output", default="benchmarks/results/latest.json")
    args = parser.parse_args()
    if args.rows < 1 or args.repeats < 1:
        parser.error("rows and repeats must be positive")

    record = benchmark(args.rows, args.repeats, args.seed)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
