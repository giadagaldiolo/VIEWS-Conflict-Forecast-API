from fastapi import APIRouter, Query
from typing import List, Optional
from app.data import repository

router = APIRouter()



@router.get("/months")
def get_months():
    return repository.get_available_months()


@router.get("/cells")
def get_cells():
    return repository.get_available_cells()


@router.get("/countries")
def get_available_countries():
    return repository.get_available_countries()


@router.get("/cell")
def forecast_by_cell(
    cell_id: List[int] = Query(None),
    metrics: Optional[List[str]] = Query(None)
):
    return repository.get_forecast_by_cell(cell_id, metrics)


@router.get("/country")
def forecast_by_country(
    country_id: Optional[List[str]] = Query(None),
    metrics: Optional[List[str]] = Query(None)
):
    print("country_id received:", country_id)  # DEBUG
    return repository.get_forecast_by_country(country_id, metrics)