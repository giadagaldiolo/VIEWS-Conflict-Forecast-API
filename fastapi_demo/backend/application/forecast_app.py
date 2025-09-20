from fastapi import APIRouter, Query, Path, HTTPException
from typing import List, Optional
from backend.business.cell.interface_cell_service import ICellService
from backend.business.cell.interface_country_service import ICountryService
from backend.business.cell.interface_month_service import IMonthService
from backend.business.cell.interface_query_service import IForecastQueryService
from backend.application.schemas import ForecastCell, ForecastValues

router = APIRouter()

# Singleton service
service = ForecastService(repository)

@router.get("/{run}/{loa}/{type_of_violence}/forecasts", response_model=List[ForecastCell])
def get_forecasts(
    run: str = Path(...),
    loa: str = Path(...),
    type_of_violence: str = Path(...),
    month_id: Optional[List[int]] = Query(None),
    priogrid_id: Optional[List[int]] = Query(None),
    country_id: Optional[List[int]] = Query(None),
    metrics: Optional[List[str]] = Query(None),
):
    try:
        results = IForecastQueryService.get_forecasts(month_id, priogrid_id, country_id, metrics)
        # Converti valori in ForecastCell / ForecastValues
        converted = [
            ForecastCell(
                priogrid_id=r["priogrid_id"],
                month_id=r["month_id"],
                country_id=r.get("country_id"),
                lat=r.get("lat"),
                lon=r.get("lon"),
                values=ForecastValues(**r["values"])
            ) for r in results
        ]
        return converted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/months", response_model=List[int])
def list_months(run: str, loa: str, type_of_violence: str):
    try:
        return IMonthService.get_months()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/cells", response_model=List[int])
def list_cells(run: str, loa: str, type_of_violence: str):
    try:
        return ICellService.get_cells()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/countries", response_model=List[int])
def list_countries(run: str, loa: str, type_of_violence: str):
    try:
        return ICountryService.get_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
