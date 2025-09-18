import json
from typing import List, Optional
from fastapi import Query

# Load data from JSON
with open("app/data/data.json") as f:
    DATA = json.load(f)


def get_available_months() -> List[str]:
    months = {entry["month"] for entry in DATA}  # set ensures uniqueness
    return sorted(months)


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


def get_forecast_by_cell(cell_ids: Optional[List[int]] = None, months: Optional[List[str]] = None, metrics: Optional[List[str]] = None):
    if cell_ids:
        results = [entry for entry in DATA if entry["grid_id"] in cell_ids]
    else:
        results = DATA.copy()  # cell_id指定なしなら全件取得
    if months:
        results = [r for r in results if r["month"] in months]
    if metrics:
        for r in results:
            keys_to_keep = ["grid_id", "month"] + metrics
            for key in list(r.keys()):
                if key not in keys_to_keep:
                    r.pop(key)
    return results


def get_forecast_by_country(
    country_ids: Optional[List[str]] = None,
    months: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
):
    if not country_ids:
        results = DATA
    else:
        results = [entry for entry in DATA if entry.get("country_id") in country_ids]

    if months:
        results = [r for r in results if r.get("month") in months]

    if metrics:
        for r in results:
            keys_to_keep = ["grid_id", "month"] + metrics
            for key in list(r.keys()):
                if key not in keys_to_keep:
                    r.pop(key)

    return results




