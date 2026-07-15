"""Contract and persistence tests for the ETL pipeline."""

import pandas as pd
import pytest

from src.pipelines import etl


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "timestamp": ["2024-01-01 09:00", "2024-01-02 09:00"],
            "open": [100.0, 105.0],
            "close": [110.0, 100.0],
            "volume": [50_000, 75_000],
        }
    )


def test_load_raw_file_not_found():
    with pytest.raises(FileNotFoundError):
        etl.load_raw("nonexistent/path.csv")


def test_load_raw_enforces_schema(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame({"volume": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Missing required columns"):
        etl.load_raw(str(path))


def test_transform_derives_research_fields_without_mutating_input(sample_df):
    original = sample_df.copy()
    result = etl.transform(sample_df)
    assert result["return"].iloc[0] == pytest.approx(0.10)
    assert "day_of_week" in result
    pd.testing.assert_frame_equal(sample_df, original)


def test_transform_rejects_invalid_values(sample_df):
    sample_df.loc[0, "open"] = 0
    with pytest.raises(ValueError, match="open"):
        etl.transform(sample_df)


def test_transform_deduplicates_and_orders(sample_df):
    duplicated = pd.concat([sample_df.iloc[::-1], sample_df.iloc[[0]]], ignore_index=True)
    result = etl.transform(duplicated)
    assert len(result) == 2
    assert result["timestamp"].is_monotonic_increasing


def test_save_processed_roundtrip(sample_df, tmp_path):
    output = tmp_path / "nested" / "processed.csv"
    etl.save_processed(sample_df, str(output))
    loaded = pd.read_csv(output)
    assert list(loaded.columns) == list(sample_df.columns)
    assert len(loaded) == len(sample_df)


def test_run_pipeline_returns_metrics(sample_df, tmp_path):
    source = tmp_path / "input.csv"
    output = tmp_path / "output.csv"
    sample_df.to_csv(source, index=False)
    metrics = etl.run_pipeline(str(source), str(output))
    assert metrics.input_rows == 2
    assert metrics.output_rows == 2
    assert metrics.null_cells == 0
    assert output.exists()
