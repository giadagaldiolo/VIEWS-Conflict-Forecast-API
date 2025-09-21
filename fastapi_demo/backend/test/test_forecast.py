"""
Integration tests for forecast API endpoints.

This module contains integration tests verifying the correctness and expected behavior of forecast-related API routes.

The tested endpoints include:
- `/months`: Returns available forecast months.
- `/cells`: Returns available priogrid cell IDs.
- `/countries`: Returns available country IDs.
- `/forecasts`: Returns forecast data filtered by month, priogrid, country, and requested metrics.

Tests cover:
- Endpoint availability and response structure.
- Retrieval of forecasts for single and multiple cells/months.
- Filtering by country ID.
- Handling empty result sets.
- Validation of requested metrics, including error handling for invalid inputs.
- Verification of forecast data types and value ranges (e.g., probabilities between 0 and 1).

Usage:
    Run the tests using pytest to ensure API functionality remains consistent.
"""

import pytest
import json
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

# 13値リスト
ALL_METRICS = [
    "pred_ln_sb_best",
    "pred_ln_sb_best_hdi_lower",
    "pred_ln_sb_best_hdi_upper",
    "pred_ln_ns_best",
    "pred_ln_ns_best_hdi_lower",
    "pred_ln_ns_best_hdi_upper",
    "pred_ln_os_best",
    "pred_ln_os_best_hdi_lower",
    "pred_ln_os_best_hdi_upper",
    "pred_ln_sb_prob_hdi_lower",
    "pred_ln_sb_prob_hdi_upper",
    "pred_ln_ns_prob_hdi_lower",
    "pred_ln_ns_prob_hdi_upper",
    "pred_ln_os_prob_hdi_lower",
    "pred_ln_os_prob_hdi_upper",
]

def parse_response(response):
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/x-ndjson"):
        # NDJSONなら各行をJSONとしてパースしてリスト返却
        return [json.loads(line) for line in response.text.splitlines()]
    else:
        # 通常のJSONならそのまま返す
        return response.json()


@pytest.mark.parametrize("endpoint", [
    "/api/preds_001/pgm/sb/months",
    "/api/preds_001/pgm/sb/cells",
    "/api/preds_001/pgm/sb/countries"
])
def test_basic_info(endpoint):
    """
    Test that basic info endpoints respond successfully and return non-empty lists.

    Args:
        endpoint (str): API endpoint to test (months, cells, countries).

    Asserts:
        - HTTP status code is 200.
        - Returned data is a non-empty list.
    """
    response = client.get(endpoint)
    assert response.status_code == 200
    data = parse_response(response)
    assert isinstance(data, list)
    assert len(data) > 0

def test_forecasts_single_cell_all_metrics():
    """
    Test forecast retrieval for a single cell and month with all available metrics.

    Verifies presence of metadata fields and that metric values are within expected ranges:
    - Probability metrics between 0 and 1.
    - HDI and best predictions as floats or lists of floats.
    """
    params = {
        "month_id": 409,
        "priogrid_id": [62356],
        "metrics": ALL_METRICS
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    assert len(data) == 1
    cell = data[0]
    # メタ情報
    for key in ["priogrid_id", "lat", "lon", "country_id"]:
        assert key in cell

    # 各メトリック確認
    for key in ALL_METRICS:
        assert key in cell
        val = cell[key]
        if "prob" in key:
            # probability は 0~1
            if isinstance(val, list):
                for v in val:
                    assert 0.0 <= v <= 1.0
            else:
                assert 0.0 <= val <= 1.0
        elif "hdi_lower" in key or "hdi_upper" in key or "_best" in key:
            # float かリスト
            if isinstance(val, list):
                for v in val:
                    assert isinstance(v, float)
            else:
                assert isinstance(val, float)

def test_forecasts_multiple_cells_and_months_all_metrics():
    params = {
        "month_id": [409, 410],
        "priogrid_id": [62356, 81761],
        "metrics": ALL_METRICS
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    # 2 months * 2 cells = 4
    assert len(data) == 4
    for cell in data:
        for key in ALL_METRICS:
            assert key in cell
            val = cell[key]
            if "prob" in key:
                if isinstance(val, list):
                    for v in val:
                        assert 0.0 <= v <= 1.0
                else:
                    assert 0.0 <= val <= 1.0
            else:
                if isinstance(val, list):
                    for v in val:
                        assert isinstance(v, float)
                else:
                    assert isinstance(val, float)

def test_forecasts_country_query_all_metrics():
    country_id = 818
    params = {
        "country_id": country_id,
        "month_id": 409,
        "metrics": ALL_METRICS
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    for cell in data:
        assert cell["country_id"] == country_id
        for key in ALL_METRICS:
            assert key in cell

def test_empty_response_all_metrics():
    params = {
        "month_id": 9999,
        "priogrid_id": [0],
        "metrics": ALL_METRICS
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    assert data == []

def test_forecasts_no_metrics_returns_meta_only():
    params = {"month_id": 409, "priogrid_id": [62356]}
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    assert len(data) == 1
    cell = data[0]
    # メタ情報だけ返る
    for key in ["priogrid_id", "lat", "lon", "country_id", "month_id", "row", "col"]:
        assert key in cell
    # メトリックはなし
    assert all(k not in cell for k in ["pred_ln_sb_best", "pred_ln_ns_best"])

def test_forecasts_invalid_metric():
    params = {"month_id": 409, "priogrid_id": [62356], "metrics": ["foobar"]}
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 400
    data = parse_response(response)
    assert "Invalid metrics" in data["detail"]

def test_forecasts_nonexistent_ids():
    params = {"month_id": 9999, "priogrid_id": [0], "country_id": 0}
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    assert data == []
