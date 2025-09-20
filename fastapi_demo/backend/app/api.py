from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from .storage_reader import ParquetFlatReader
from .schemas import FORECAST_SCHEMA
import json

router = APIRouter()

# Inizializza reader
reader = ParquetFlatReader(base_path="app/data")

BASE_COLS = ["priogrid_id", "month_id", "country_id", "lat", "lon", "row", "col"]
FORECAST_COLS = [c for c in FORECAST_SCHEMA.keys() if c not in BASE_COLS]


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

@router.get("/forecast")
async def get_forecast():
    return {"message": "Hello from FastAPI forecast API"}

# ---------------------------
# Forecasts endpoint
# ---------------------------
@router.get("/{run}/{loa}/{type_of_violence}/forecasts")
def get_forecasts(
    run: str = Path(...),
    loa: str = Path(...),
    type_of_violence: str = Path(...),
    month_id: Optional[List[int]] = Query(None),
    priogrid_id: Optional[List[int]] = Query(None),
    country_id: Optional[List[int]] = Query(None),
    metrics: Optional[List[str]] = Query(None)
):
    if metrics:
        invalid = [m for m in metrics if m not in FORECAST_COLS]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid metrics: {invalid}")

    return StreamingResponse(
        iter_forecasts_json(
            month_ids=month_id,
            priogrid_ids=priogrid_id,
            country_ids=country_id,
            metrics=metrics
        ),
        media_type="application/json"
    )


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
    """Return all available country IDs"""
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

# ---------------------------
# Countries endpoint
# ---------------------------
@router.get("/countries", response_model=List[dict])
def get_countries():
    """
    Return list of available countries with ID and name.
    """
    try:
        # reader から country_id を取得し、仮に name を ID の文字列に設定
        country_ids = reader.list_country_ids()
        countries = [{"id": cid, "name": str(cid)} for cid in country_ids]
        return countries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Months endpoint
# ---------------------------
@router.get("/months", response_model=List[dict])
def get_months():
    """
    Return list of months with ID and label.
    """
    try:
        month_ids = reader.list_months()
        months = [{"id": mid, "label": str(mid)} for mid in month_ids]
        return months
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------
# Metrics endpoint（オプション）
# ---------------------------
@router.get("/metrics", response_model=List[str])
def get_metrics():
    """
    Return list of available metrics.
    """
    try:
        # 既存の FORECAST_COLS をそのまま返す
        from .schemas import FORECAST_SCHEMA
        BASE_COLS = ["priogrid_id", "month_id", "country_id", "lat", "lon", "row", "col"]
        metrics = [c for c in FORECAST_SCHEMA.keys() if c not in BASE_COLS]
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
