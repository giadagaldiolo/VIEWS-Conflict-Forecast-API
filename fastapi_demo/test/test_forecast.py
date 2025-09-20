from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
import json

client = TestClient(app)

def get_json_lines(response):
    """NDJSON に対応"""
    try:
        return [json.loads(line) for line in response.text.splitlines()]
    except json.JSONDecodeError:
        # 通常の JSON の場合
        return response.json()

def test_forecasts_single_cell():
    response = client.get(
        "/api/preds_001/pgm/sb/forecasts",
        params={
            "month_id": 409,
            "priogrid_id": [62356],
            "metrics": ["pred_ln_sb_best"]
        }
    )
    assert response.status_code == 200
    data = get_json_lines(response)
    assert len(data) > 0
    assert "pred_ln_sb_best" in data[0]

def test_forecasts_multiple_months():
    response = client.get(
        "/api/preds_001/pgm/sb/forecasts",
        params={
            "month_id": [409, 410],
            "priogrid_id": [62356],
            "metrics": ["pred_ln_sb_best"]
        }
    )
    assert response.status_code == 200
    data = get_json_lines(response)
    assert len(data) == 2

def test_forecasts_country_query():
    response = client.get(
        "/api/preds_001/pgm/sb/forecasts",
        params={
            "country_id": 818,
            "month_id": 409,
            "metrics": ["pred_ln_sb_best"]
        }
    )
    assert response.status_code == 200
    data = get_json_lines(response)
    for cell in data:
        assert cell["country_id"] == 818
