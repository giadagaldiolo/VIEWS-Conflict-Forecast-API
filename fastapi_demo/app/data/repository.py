import json
from typing import List, Optional

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


def get_forecast_by_cell(cell_id: int, months: Optional[List[str]] = None, metrics: Optional[List[str]] = None):
    results = [entry for entry in DATA if entry["grid_id"] == cell_id]
    if months:
        results = [r for r in results if r["month"] in months]
    if metrics:
        # keep only requested metrics + grid_id, month
        for r in results:
            keys_to_keep = ["grid_id", "month"] + metrics
            for key in list(r.keys()):
                if key not in keys_to_keep:
                    r.pop(key)
    return results


def get_forecast_by_country(country_id: str, months: Optional[List[str]] = None, metrics: Optional[List[str]] = None):
    results = [entry for entry in DATA if entry["country_id"] == country_id]
    if months:
        results = [r for r in results if r["month"] in months]
    if metrics:
        for r in results:
            keys_to_keep = ["grid_id", "month"] + metrics
            for key in list(r.keys()):
                if key not in keys_to_keep:
                    r.pop(key)
    return results

