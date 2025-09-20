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
    rows: List[int] = Query(..., description="Row indices of cells to filter, one or more"),
    cols: List[int] = Query(..., description="Column indices of cells to filter, one or more"),
    months: Optional[List[int]] = Query(None, description="Month IDs to filter, e.g. 202501"),
    metrics: Optional[List[str]] = Query(None, description="Metrics to include in the result")
):
    """
    Returns forecast values for one or more cells specified by rows and cols.
    """
    return repository.get_forecast_by_cell(rows=rows, cols=cols, months=months, metrics=metrics)


@router.get("/country", summary="Forecast By Country", tags=["Forecast"])
def forecast_by_country(
    country_id: List[int] = Query(..., description="IDs of countries to filter, one or more"),
    months: Optional[List[int]] = Query(None, description="Month IDs to filter"),
    metrics: Optional[List[str]] = Query(None, description="Metrics to include")
):
    """
    Returns forecast values for all grid cells in one or more countries.
    """
    return repository.get_forecast_by_country(country_ids=country_id, months=months, metrics=metrics)


@router.get("/month", summary="Forecast By Month", tags=["Forecast"])
def forecast_by_month(
    months: List[int] = Query(..., description="List of month IDs to filter, e.g. [202501]"),
    metrics: Optional[List[str]] = Query(None, description="List of metric keys to include")
):
    return repository.get_forecast_by_month(months, metrics)


@router.get("/metrics", summary="Available Metrics", tags=["Info"])
def get_metrics():
    """Returns all available metric keys (pred_* columns)."""
    return repository.get_available_metrics()
