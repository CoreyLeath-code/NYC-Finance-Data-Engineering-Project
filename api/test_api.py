from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root_and_operations_endpoints():
    assert client.get("/").json() == {"status": "API running"}
    assert client.get("/healthz").json() == {"status": "ok"}
    assert client.get("/readyz").status_code == 200
    assert "api_http_requests_total" in client.get("/metrics").text


def test_prediction_with_mock_model():
    model = MagicMock()
    model.predict.return_value = [42.0]
    with patch("api.main._get_model", return_value=model):
        response = client.post("/predict", json={"features": [1.0, 2.0, 3.0]})
    assert response.status_code == 200
    assert response.json() == {"prediction": 42.0}


def test_prediction_missing_model():
    with patch("api.main._get_model", side_effect=FileNotFoundError("no model")):
        response = client.post("/predict", json={"features": [1.0]})
    assert response.status_code == 503
    assert response.json() == {"detail": "Model unavailable"}


def test_prediction_nonfinite_inputs_and_outputs_are_rejected():
    assert client.post("/predict", json={"features": ["NaN"]}).status_code == 422
    model = MagicMock()
    model.predict.return_value = [float("nan")]
    with patch("api.main._get_model", return_value=model):
        response = client.post("/predict", json={"features": [1.0]})
    assert response.status_code == 503
    assert response.json()["detail"] == "Model unavailable"


def test_unknown_urls_do_not_inflate_metrics_cardinality():
    client.get("/untrusted-client-path/very-unique-token-2026")
    metrics = client.get("/metrics").text
    assert 'path="unmatched"' in metrics
    assert "very-unique-token-2026" not in metrics


def test_prediction_rejects_empty_or_extra_input():
    assert client.post("/predict", json={"features": []}).status_code == 422
    assert client.post("/predict", json={"features": [1.0], "name": "blocked"}).status_code == 422
