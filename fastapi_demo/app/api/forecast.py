from fastapi import APIRouter, Query
from typing import List, Optional
from app.data import repository

router = APIRouter()


# 1️⃣ /months → lista dei mesi disponibili
@router.get("/months")
def get_months():
    return repository.get_available_months()

# 2️⃣ /cells → lista delle celle
@router.get("/cells")
def get_cells():
    return repository.get_available_cells()

# 3️⃣ /forecast/cell → dati per cell_id (uno o più)
@router.get("/forecast/cell")
def forecast_by_cell(
    cell_id: int,
    months: Optional[List[str]] = None,
    metrics: Optional[List[str]] = None
):
    return repository.get_forecast_by_cell(cell_id, months, metrics)

# 4️⃣ /forecast/country → dati per country_id
@router.get("/forecast/country")
def forecast_by_country(
    country_id: str,
    months: Optional[List[str]] = Query(None),
    metrics: Optional[List[str]] = Query(None)
):
    return repository.get_forecast_by_country(country_id, months, metrics)
