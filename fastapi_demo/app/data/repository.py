import json
from typing import List, Optional
from fastapi import Query

# Load data from JSON
with open("app/data/data.json") as f:
    DATA = json.load(f)


def get_available_months() -> List[str]:
    return {entry["month"] for entry in DATA}

def get_available_countries() -> List[str]:
    return sorted({entry["country_id"] for entry in DATA})


def get_available_cells() -> List[dict]:
    cells = []
    seen = set()
    for entry in DATA:
        grid_id = entry["grid_id"]
        if grid_id not in seen:
            seen.add(grid_id)
            cells.append({
                "grid_id": grid_id,
                "country_id": entry["country_id"],
                "lat": entry["lat"],
                "lon": entry["lon"]
            })
    return cells


def get_forecast_by_cell(
    cell_ids: Optional[List[int]] = None,
    metrics: Optional[List[str]] = None
):
    results = DATA
    if cell_ids:
        results = [r for r in results if r["grid_id"] in cell_ids]
    if metrics:
        results = [
            {k: v for k, v in r.items() if k in ["grid_id", "month"] + metrics}
            for r in results
        ]
    return results


def get_forecast_by_country(
    country_ids: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
):
    results = DATA
    if country_ids:
        results = [r for r in results if r["country_id"] in country_ids]
    if metrics:
        results = [
            {k: v for k, v in r.items() if k in ["grid_id", "month"] + metrics}
            for r in results
        ]
    return results




