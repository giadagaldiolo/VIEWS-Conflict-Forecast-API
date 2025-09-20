from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from .storage_reader import ParquetFlatReader
from .schemas import ForecastCell, ForecastValues
import json

router = APIRouter()

# Inizializza reader
reader = ParquetFlatReader(base_path="app/data")

def iter_forecasts_json(
    month_ids: Optional[List[int]] = None,
    priogrid_ids: Optional[List[int]] = None,
    country_ids: Optional[List[int]] = None,
    metrics: Optional[List[str]] = None,
):
    """
    Streaming generator che restituisce JSON line by line.
    """
    try:
        for record in reader.query(
            month_ids=month_ids,
            priogrid_ids=priogrid_ids,
            country_ids=country_ids,
            metrics=metrics
        ):
            yield json.dumps(record) + "\n"

    except Exception as e:
        yield json.dumps({"error": str(e)}) + "\n"


# ---------------------------
# Forecasts endpoint
# ---------------------------

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
    results = []

    try:
        for record in reader.query(
            month_ids=month_id,
            priogrid_ids=priogrid_id,
            country_ids=country_id,
            metrics=metrics
        ):
            values_dict = record["values"]


            values_dict = {k: v for k, v in record["values"].items() if not metrics or k in metrics}
            values = ForecastValues(**values_dict)


            results.append(ForecastCell(
                priogrid_id=record["priogrid_id"],
                month_id=record["month_id"],
                country_id=record.get("country_id"),
                lat=record.get("lat"),
                lon=record.get("lon"),
                values=values
            ))

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Months endpoint
# ---------------------------
@router.get("/{run}/{loa}/{type_of_violence}/months", response_model=List[int])
def list_months(run: str, loa: str, type_of_violence: str):
    try:
        return reader.list_months()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Grid cells endpoint
# ---------------------------
@router.get("/{run}/{loa}/{type_of_violence}/cells", response_model=List[int])
def list_cells(run: str, loa: str, type_of_violence: str):
    try:
        return reader.list_priogrid_ids()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Countries endpoint
# ---------------------------
@router.get("/{run}/{loa}/{type_of_violence}/countries", response_model=List[int])
def list_countries(
    run: str = Path(...),
    loa: str = Path(...),
    type_of_violence: str = Path(...)
):
    try:
        return reader.list_country_ids()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Ping endpoint
# ---------------------------
@router.get("/ping")
def ping():
    return {"status": "ok"}