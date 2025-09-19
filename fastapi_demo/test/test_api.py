import pytest
from fastapi.testclient import TestClient
from app.main import app  # FastAPI のエントリーポイントに応じて修正

client = TestClient(app)

# -------------------------------
# 1. Utility Validators
# -------------------------------

def validate_forecast_cell(cell: dict, expected_metrics: list):
    assert "prio_grid_id" in cell
    assert isinstance(cell["prio_grid_id"], int)

    assert "lat" in cell and "lon" in cell
    assert isinstance(cell["lat"], float)
    assert isinstance(cell["lon"], float)

    assert "country_id" in cell
    assert isinstance(cell["country_id"], int)

    # Optional fields
    if "admin1_id" in cell:
        assert isinstance(cell["admin1_id"], int)
    if "admin2_id" in cell:
        assert isinstance(cell["admin2_id"], int)

    assert "values" in cell
    assert isinstance(cell["values"], dict)
    for metric in expected_metrics:
        assert metric in cell["values"]

# -------------------------------
# 2. Months & Cells Metadata
# -------------------------------

def test_get_available_months():
    response = client.get("/forecast/months")
    assert response.status_code == 200
    months = response.json()
    assert isinstance(months, list)
    assert all(isinstance(m, str) and len(m) == 7 and m.count("-") == 1 for m in months)  # "YYYY-MM"

def test_get_available_cells():
    response = client.get("/forecast/cells")
    assert response.status_code == 200
    cells = response.json()
    assert isinstance(cells, list)
    for cell in cells:
        assert "lat" in cell and "lon" in cell
        assert "country_id" in cell
        assert "row" in cell and "col" in cell

# -------------------------------
# 3. Forecast Query - Valid Cases
# -------------------------------

def test_get_forecast_by_valid_country():
    response = client.get("/forecast/country", params=[
        ("country_ids", "840"),  # USA (UN M49)
        ("metrics", "MAP")
    ])
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for cell in data:
        validate_forecast_cell(cell, ["MAP"])

def test_get_forecast_by_grid_ids():
    response = client.get("/forecast/grid", params=[
        ("grid_ids", "12345"),
        ("metrics", "MAP"),
        ("metrics", "HDI_90")
    ])
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for cell in data:
        validate_forecast_cell(cell, ["MAP", "HDI_90"])

def test_get_forecast_by_month_range():
    response = client.get("/forecast/country", params=[
        ("country_ids", "840"),
        ("metrics", "MAP"),
        ("start_month", "2023-01"),
        ("end_month", "2023-06")
    ])
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for cell in data:
        validate_forecast_cell(cell, ["MAP"])

def test_get_forecast_all_metrics():
    all_metrics = ["MAP", "HDI_50", "HDI_90", "HDI_99", "THRESH_01", "THRESH_02", "THRESH_03", "THRESH_04", "THRESH_05", "THRESH_06"]
    response = client.get("/forecast/country", params=[
        ("country_ids", "840"),
        *[( "metrics", m ) for m in all_metrics]
    ])
    assert response.status_code == 200
    data = response.json()
    for cell in data:
        validate_forecast_cell(cell, all_metrics)

# -------------------------------
# 4. Forecast Query - Invalid Cases
# -------------------------------

def test_invalid_country_id_returns_404_or_empty():
    response = client.get("/forecast/country", params=[
        ("country_ids", "9999"),
        ("metrics", "MAP")
    ])
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert response.json() == []

def test_invalid_metric_returns_422():
    response = client.get("/forecast/country", params=[
        ("country_ids", "840"),
        ("metrics", "INVALID_METRIC")
    ])
    assert response.status_code in (400, 422)

def test_missing_metrics_returns_422():
    response = client.get("/forecast/country", params=[
        ("country_ids", "840")
    ])
    assert response.status_code in (400, 422)

def test_empty_parameters():
    response = client.get("/forecast/country")
    assert response.status_code in (400, 422)

# -------------------------------
# 5. Performance Test (Optional)
# -------------------------------

@pytest.mark.skip(reason="Performance test — run manually")
def test_large_country_forecast():
    response = client.get("/forecast/country", params=[
        ("country_ids", "356"),  # India
        ("metrics", "MAP")
    ])
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 1000  # Should return large result set

# -------------------------------
# 6. Format: Line-by-line JSON (Optional)
# -------------------------------

def test_response_format_line_by_line():
    response = client.get("/forecast/country", params=[
        ("country_ids", "840"),
        ("metrics", "MAP"),
        ("format", "jsonl")
    ])
    assert response.status_code == 200
    # Should be line-delimited JSON
    lines = response.text.strip().split("\n")
    for line in lines:
        cell = eval(line)  # Use json.loads(line) in real impl
        validate_forecast_cell(cell, ["MAP"])
