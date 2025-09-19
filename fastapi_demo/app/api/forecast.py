from fastapi import APIRouter, Query
from typing import List, Optional
from app.data import repository

router = APIRouter()


@router.get("/months", summary="Get Months", tags=["Info"])
def get_months():
    """Returns all available months in the dataset."""
    return repository.get_available_months()


@router.get("/cells", summary="Get Cells", tags=["Info"])
def get_cells():
    """Returns all available grid cells."""
    return repository.get_available_cells()


@router.get("/countries", summary="Get Countries", tags=["Info"])
def get_countries():
    """Returns all available countries."""
    return repository.get_available_countries()



@router.get("/cell", summary="Forecast By Cell", tags=["Forecast"])
def forecast_by_cell(
    cell_id: List[int] = Query(..., description="IDs of cells to filter, one or more"),
    months: Optional[List[str]] = Query(None, description="Months to filter, e.g., 2025-01"),
    metrics: Optional[List[str]] = Query(None, description="Metrics to include in the result")
):
    """
    Returns forecast values for one or more cells.
    If 'months' or 'metrics' are not provided, returns all months/all metrics.
    """
    return repository.get_forecast_by_cell(cell_id, months, metrics)


@router.get("/country", summary="Forecast By Country", tags=["Forecast"])
def forecast_by_country(
    country_id: List[str] = Query(..., description="IDs of countries to filter, one or more"),
    months: Optional[List[str]] = Query(None, description="Months to filter"),
    metrics: Optional[List[str]] = Query(None, description="Metrics to include")
):
    """
    Returns forecast values for all grid cells in one or more countries.
    """
    return repository.get_forecast_by_country(country_id, months, metrics)


@router.get("/month", summary="Forecast By Month", tags=["Forecast"])
def forecast_by_month(
    months: List[str] = Query(..., description="List of months to filter, e.g. ['2025-01']"),
    metrics: Optional[List[str]] = Query(None, description="List of metric keys to include")
):
    return repository.get_forecast_by_month(months, metrics)

@router.get("/metrics", summary="Available Metrics", tags=["Info"])
def get_metrics():
    """Returns all available metric keys (pred_* columns)."""
    return repository.get_available_metrics()
