from fastapi import APIRouter, Query, Path, HTTPException
from typing import List, Optional
from business.cell.cell_service import CellService
from business.country.countries_service import CountryService
from business.month.month_service import MonthService
from business.query.forecast_query_service import ForecastQueryService
from dataAccess.parquet_reader import ParquetFlatReader
from application.schemas import ForecastCell, ForecastValues

router = APIRouter()

reader = ParquetFlatReader(base_path="dataAccess")
cell_service = CellService(reader)
month_service = MonthService(reader)
country_service = CountryService(reader)
forecast_service = ForecastQueryService(reader)


@router.get("/{run}/{loa}/{type_of_violence}/forecasts")
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
        results = forecast_service.get_forecasts(month_id, priogrid_id, country_id, metrics)
        converted = []

        for r in results:
            # Se ci sono metriche selezionate, restituisci solo quelle
            if metrics:
                values_dict = {k: v for k, v in r["values"].items() if k in metrics}
            else:
                values_dict = r["values"]

            cell = {
                "priogrid_id": r["priogrid_id"],
                "month_id": r["month_id"],
                "country_id": r.get("country_id"),
                "lat": r.get("lat"),
                "lon": r.get("lon"),
                "values": values_dict  # restituisce solo le metriche richieste
            }
            converted.append(cell)

        return converted

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{run}/{loa}/{type_of_violence}/months", response_model=List[int])
def list_months(run: str, loa: str, type_of_violence: str):
    try:
        return month_service.get_months()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/cells", response_model=List[int])
def list_cells(run: str, loa: str, type_of_violence: str, country_id: int):
    try:
        all_cells = cell_service.get_cells()
        filtered = [c["priogrid_id"] for c in all_cells if c.get("country_id") == country_id]
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{run}/{loa}/{type_of_violence}/countries", response_model=List[int])
def list_countries(run: str, loa: str, type_of_violence: str):
    try:
        return country_service.get_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/metrics", response_model=List[str])
def list_metrics(run: str, loa: str, type_of_violence: str):
    """
    Restituisce l'elenco dei nomi delle metriche disponibili in ForecastValues.
    """
    try:
        # Prendi tutti i campi di ForecastValues come lista di stringhe
        from application.schemas import ForecastValues
        metrics = list(ForecastValues.__fields__.keys())
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def root():
    return {"message": "API is running. Use /{run}/{loa}/{type_of_violence}/... endpoints."}