import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

# Tutti i 13 valori nel dict values
ALL_METRICS = [
    "MAP",
    "HDI_50_lower", "HDI_50_upper",
    "HDI_90_lower", "HDI_90_upper",
    "HDI_99_lower", "HDI_99_upper",
    "prob_threshold_1", "prob_threshold_2", "prob_threshold_3",
    "prob_threshold_4", "prob_threshold_5", "prob_threshold_6"
]

def test_forecasts_single_cell_values():
    params = {
        "month_id": 409,
        "priogrid_id": [62356]
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    cell = data[0]

    # Controlla metadati
    for key in ["priogrid_id", "lat", "lon", "country_id"]:
        assert key in cell

    # Controlla che i 13 valori siano presenti in cell["values"]
    for key in ALL_METRICS:
        val = cell["values"].get(key)
        assert val is None or isinstance(val, float)
        if val is not None and "prob" in key:
            assert 0.0 <= val <= 1.0

def test_forecasts_multiple_cells_and_months():
    params = {
        "month_id": [409, 410],
        "priogrid_id": [62356, 81761]
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4  # 2 months x 2 cells
    for cell in data:
        for key in ALL_METRICS:
            assert key in cell["values"]

def test_forecasts_country_query():
    country_id = 818
    params = {
        "country_id": country_id,
        "month_id": 409
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = response.json()
    for cell in data:
        assert cell["country_id"] == country_id
        for key in ALL_METRICS:
            assert key in cell["values"]

def test_empty_response():
    params = {
        "month_id": 9999,
        "priogrid_id": [0]
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    assert response.json() == []

def test_forecasts_with_selected_metrics():
    # Seleziono solo alcune metriche
    selected_metrics = ["MAP", "HDI_50_lower", "prob_threshold_1"]
    params = {
        "month_id": 409,
        "priogrid_id": [62356],
        "metrics": selected_metrics
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    cell = data[0]

    # Controlla che i valori richiesti siano float o None
    for key in selected_metrics:
        val = cell["values"].get(key)
        assert val is None or isinstance(val, float)
        if val is not None and "prob" in key:
            assert 0.0 <= val <= 1.0

    # Controlla che metriche non richieste siano None
    for key in ALL_METRICS:
        if key not in selected_metrics:
            val = cell["values"].get(key)
            assert val is None
