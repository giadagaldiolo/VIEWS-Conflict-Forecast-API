"""
Extended integration tests for forecast API endpoints.

This module adds additional coverage to verify:
- Multiple filters combined (months, priogrid cells, country, metrics)
- NDJSON response handling
- Null values in metrics
- Correct filtering of requested metrics

Usage:
    Run with pytest to validate forecast API behavior.
"""

import pytest
import json
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

# Correct 13 metrics in your ForecastValues
ALL_METRICS = [
    "MAP",
    "HDI_50_lower",
    "HDI_50_upper",
    "HDI_90_lower",
    "HDI_90_upper",
    "HDI_99_lower",
    "HDI_99_upper",
    "prob_threshold_1",
    "prob_threshold_2",
    "prob_threshold_3",
    "prob_threshold_4",
    "prob_threshold_5",
    "prob_threshold_6",
]


def parse_response(response):
    """
    Parse API response, handling both NDJSON and standard JSON.

    Args:
        response: FastAPI TestClient response object.

    Returns:
        List of dictionaries representing forecast data.
    """
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/x-ndjson"):
        return [json.loads(line) for line in response.text.splitlines()]
    else:
        return response.json()


@pytest.mark.parametrize("endpoint,query", [
    ("/api/preds_001/pgm/sb/months", {}),
    ("/api/preds_001/pgm/sb/cells", {"country_id": 40}),
    ("/api/preds_001/pgm/sb/countries", {})
])
def test_basic_info(endpoint, query):
    """
    Test that basic info endpoints respond successfully and return non-empty lists.
    """
    response = client.get(endpoint, params=query)
    assert response.status_code == 200
    data = parse_response(response)
    assert isinstance(data, list)
    assert len(data) > 0


def test_forecasts_multiple_filters_selected_metrics():
    """
    Test retrieval with multiple filters: months, priogrid cells, country, and only selected metrics.

    Verifies that:
    - Only requested metrics are included in the 'values' field.
    - Metadata fields exist.
    """
    params = {
        "month_id": [409, 410],
        "priogrid_id": [150792, 151512],
        "country_id": [40],
        "metrics": ["MAP", "HDI_50_lower"]  # Use real metric names
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    assert len(data) > 0

    for cell in data:
        # Check metadata
        for key in ["priogrid_id", "month_id", "lat", "lon", "country_id"]:
            assert key in cell

        # Check only selected metrics are present
        assert set(cell["values"].keys()) == {"MAP", "HDI_50_lower"}


def test_forecasts_ndjson_support():
    """
    Test that the API correctly handles NDJSON response format.
    """
    headers = {"Accept": "application/x-ndjson"}
    params = {
        "month_id": [409],
        "priogrid_id": [62356],
        "metrics": ["MAP"]
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params, headers=headers)
    assert response.status_code == 200
    data = parse_response(response)
    assert isinstance(data, list)
    assert all("values" in cell for cell in data)
    assert all("MAP" in cell["values"] for cell in data)


def test_forecasts_null_values_handling():
    """
    Test that metrics with null values are handled properly and returned as null.
    """
    params = {
        "month_id": 409,
        "priogrid_id": [62356],
        "metrics": ["MAP", "HDI_50_upper"]
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    for cell in data:
        for key in ["MAP", "HDI_50_upper"]:
            assert key in cell["values"]
            val = cell["values"][key]
            assert val is None or isinstance(val, (float, list))


def test_forecasts_combined_filters_with_no_results():
    """
    Test that combining filters with non-existent IDs returns an empty list.
    """
    params = {
        "month_id": [9999],
        "priogrid_id": [0],
        "country_id": [0],
        "metrics": ["MAP"]
    }
    response = client.get("/api/preds_001/pgm/sb/forecasts", params=params)
    assert response.status_code == 200
    data = parse_response(response)
    assert data == []
