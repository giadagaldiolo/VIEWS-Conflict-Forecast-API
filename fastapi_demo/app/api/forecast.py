from fastapi import APIRouter, Query
from typing import List, Optional
from app.data import repository

router = APIRouter()



@router.get("/forecast/months")
def get_months():
    return repository.get_available_months()


@router.get("/forecast/cells")
def get_cells():
    return repository.get_available_cells()


@router.get("/forecast/countries")
def available_countries():
    return get_available_countries()


@router.get("/forecast/cell")
def forecast_by_cell(
    cell_id: List[int] = Query(None),
    metrics: Optional[List[str]] = Query(None)
):
    return repository.get_forecast_by_cell(cell_id, metrics)


@router.get("/forecast/country")
def forecast_by_country(
    country_id: Optional[List[str]] = Query(None),
    metrics: Optional[List[str]] = Query(None)
):
    print("country_id ricevuto:", country_id)  # DEBUG
    return repository.get_forecast_by_country(country_id, metrics)