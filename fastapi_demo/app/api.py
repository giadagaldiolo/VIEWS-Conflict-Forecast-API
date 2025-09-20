from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Optional
from .storage_reader import ParquetFlatReader
from .schemas import FORECAST_SCHEMA
import json

router = APIRouter()

# Initialize reader
reader = ParquetFlatReader(base_path="app/data")

# Base metadata columns
BASE_COLS = ["priogrid_id", "month_id", "country_id", "lat", "lon", "row", "col"]

# Forecast columns (MAP + HDIs + probabilities)
FORECAST_COLS = [c for c in FORECAST_SCHEMA.keys() if c not in BASE_COLS]


def iter_forecasts_json(
    month_ids: Optional[List[int]] = None,
    priogrid_ids: Optional[List[int]] = None,
    country_ids: Optional[List[int]] = None,
    metrics: Optional[List[str]] = None,
):
    """
    Streaming generator yielding JSON lines for each record.
    """
    try:
        # Yield records directly from the query without list()
        for record in reader.query(
            month_ids=month_ids,
            priogrid_ids=priogrid_ids,
            country_ids=country_ids,
            metrics=metrics
        ):
            yield json.dumps(record) + "\n"

    except Exception as e:
        # Yield error as JSON
        yield json.dumps({"error": str(e)}) + "\n"


@router.get("/{run}/{loa}/{type_of_violence}/forecasts")
def get_forecasts(
    run: str = Path(..., description="Run ID (e.g., preds_001)"),
    loa: str = Path(..., description="Level of analysis: cm or pgm"),
    type_of_violence: str = Path(..., description="sb, ns, os"),
    month_id: Optional[List[int]] = Query(None, description="Filter by month_id(s)"),
    priogrid_id: Optional[List[int]] = Query(None, description="Filter by priogrid_id(s)"),
    country_id: Optional[List[int]] = Query(None, description="Filter by country_id(s)"),
    metrics: Optional[List[str]] = Query(
        None,
        description=f"Subset of forecast columns (any combination of {FORECAST_COLS})"
    )
):
    """
    Streaming JSON: Returns filtered forecasts with optional subset of metrics.
    """
    # Validate metrics
    if metrics:
        invalid = [m for m in metrics if m not in FORECAST_COLS]
        if invalid:
            raise HTTPException(status_code=400, detail=f"Invalid metrics: {invalid}")

    # Return streaming response
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
def list_months(
    run: str = Path(...),
    loa: str = Path(...),
    type_of_violence: str = Path(...)
):
    """Return all available month_ids"""
    try:
        return reader.list_months()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------
# Grid cells endpoint
# ---------------------------
@router.get("/{run}/{loa}/{type_of_violence}/cells", response_model=List[int])
def list_cells(
    run: str = Path(...),
    loa: str = Path(...),
    type_of_violence: str = Path(...)
):
    """Return all available PRIO grid cell IDs"""
    try:
        return reader.list_priogrid_ids()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ping")
def ping():
    return {"status": "ok"}