import json
from typing import List, Optional

# Load data from JSON
with open("app/data/data.json") as f:
    DATA = json.load(f)


def get_available_months() -> List[str]:
    """Return unique months available in the dataset."""
    return sorted({entry["month"] for entry in DATA})


def get_available_countries() -> List[str]:
    """Return unique countries available in the dataset."""
    return sorted({entry["country_id"] for entry in DATA})


def get_available_cells() -> List[dict]:
    """Return unique grid cells with metadata."""
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


def filter_results(
    results: List[dict],
    months: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
) -> List[dict]:
    """Helper to filter by months and metrics."""
    if months:
        results = [r for r in results if r["month"] in months]
    if metrics:
        results = [
            {k: v for k, v in r.items() if k in ["grid_id", "month"] + metrics}
            for r in results
        ]
    return results


def get_forecast_by_cell(
    cell_ids: Optional[List[int]] = None,
    months: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
) -> List[dict]:
    """Return forecast for one or more grid cells."""
    results = DATA
    if cell_ids:
        results = [r for r in results if r["grid_id"] in cell_ids]
    return filter_results(results, months, metrics)


def get_forecast_by_country(
    country_ids: Optional[List[str]] = None,
    months: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
) -> List[dict]:
    """Return forecast for all grid cells in one or more countries."""
    results = DATA
    if country_ids:
        results = [r for r in results if r["country_id"] in country_ids]
    return filter_results(results, months, metrics)


def get_forecast_by_month(
    months: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
) -> List[dict]:
    """Return forecast filtered by month(s) only."""
    results = DATA
    return filter_results(results, months, metrics)
