# tests/test_forecast.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.api.forecast import router
from fastapi import FastAPI
import numpy as np


# FastAPI test application
app = FastAPI()
app.include_router(router, prefix="/forecast")

client = TestClient(app)


def test_get_months():
    response = client.get("/forecast/months")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(m, int) for m in data)


def test_get_cells():
    response = client.get("/forecast/cells")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("row" in cell and "col" in cell for cell in data)


def test_get_metrics():
    response = client.get("/forecast/metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(isinstance(m, str) for m in data)


def test_forecast_by_cell():
    params = {
        "rows": [87],  # From provided cells values
        "cols": [436],
        "months": [409],
        "metrics": ["pred_ln_sb_best", "pred_ln_ns_best"]
    }
    response = client.get("/forecast/cell", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert all("pred_ln_sb_best" in row for row in data)


def test_forecast_by_country():
    params = {
        "country_id": [163],
        "month_id": [409],
        "metrics": ["pred_ln_sb_best"]
    }
    response = client.get("/forecast/country", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert all(row["country_id"] == 163 for row in data)

def test_forecast_by_month():
    params = {
        "month_id": [409],
        "metrics": ["pred_ln_sb_best"]
    }
    response = client.get("/forecast/month", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)