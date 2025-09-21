import logging
from fastapi import APIRouter, Query, Path, HTTPException
from typing import List, Optional
from business.cell.cell_service import CellService
from business.country.countries_service import CountryService
from business.month.month_service import MonthService
from business.query.forecast_query_service import ForecastQueryService
from dataAccess.parquet_reader import ParquetFlatReader
from application.schemas import ForecastCell, ForecastValues

logger = logging.getLogger(__name__)

# Initialize the API router
router = APIRouter()

# Instantiate the Parquet data reader and services
reader = ParquetFlatReader(base_path="dataAccess")
cell_service = CellService(reader)
month_service = MonthService(reader)
country_service = CountryService(reader)
forecast_service = ForecastQueryService(reader)

@router.get("/{run}/{loa}/{type_of_violence}/forecasts", response_model=List[ForecastCell])
def get_forecasts(
    run: str = Path(..., description="Forecast run identifier (e.g. 'v1', 'latest')"),
    loa: str = Path(..., description="Level of analysis, e.g. 'cell', 'country'"),
    type_of_violence: str = Path(..., description="Type of violence forecasted"),
    month_id: Optional[List[int]] = Query(None, description="List of month IDs to filter by, e.g. [202101, 202102]"),
    priogrid_id: Optional[List[int]] = Query(None, description="List of grid cell IDs to filter"),
    country_id: Optional[List[int]] = Query(None, description="List of country IDs to filter"),
    metrics: Optional[List[str]] = Query(None, description="List of metric names to include, e.g. ['best', 'p25']"),
):
    """
    Retrieve forecast data based on provided filters.

    Args:
        run (str): Identifier of the forecast run.
        loa (str): Level of analysis (e.g., 'cell', 'country').
        type_of_violence (str): Type of violence being forecasted.
        month_id (List[int], optional): Filter forecasts by specific months.
        priogrid_id (List[int], optional): Filter forecasts by grid cells.
        country_id (List[int], optional): Filter forecasts by country.
        metrics (List[str], optional): Filter forecasts by forecast metric names.

    Returns:
        List[ForecastCell]: A list of forecasted values for each matching cell and month.

    Raises:
        HTTPException: If an unexpected error occurs during data retrieval or processing.
    """
    try:
        results = forecast_service.get_forecasts(month_id, priogrid_id, country_id, metrics)
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
        logger.error("Failed to retrieve forecasts", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{run}/{loa}/{type_of_violence}/months", response_model=List[int])
def list_months(run: str, loa: str, type_of_violence: str):
    """
    Retrieve a list of available month IDs used in forecasts.

    Args:
        run (str): Placeholder for path consistency.
        loa (str): Placeholder for path consistency.
        type_of_violence (str): Placeholder for path consistency.

    Returns:
        List[int]: List of month IDs in YYYYMM format.

    Raises:
        HTTPException: If data loading fails.
    """
    try:
        return month_service.get_months()
    except Exception as e:
        logger.error("Failed to retrieve months", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{run}/{loa}/{type_of_violence}/cells", response_model=List[int])
def list_cells(run: str, loa: str, type_of_violence: str):
    """
    Retrieve a list of grid cell IDs used in forecasts.

    Returns:
        List[int]: List of unique priogrid IDs.

    Raises:
        HTTPException: If data loading fails.
    """
    try:
        return cell_service.get_cells()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/countries", response_model=List[int])
def list_countries(run: str, loa: str, type_of_violence: str):
    """
    Retrieve a list of country IDs used in forecasts.

    Returns:
        List[int]: List of unique country IDs.

    Raises:
        HTTPException: If data loading fails.
    """
    try:
        return country_service.get_countries()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{run}/{loa}/{type_of_violence}/metrics", response_model=List[str])
def list_metrics(run: str, loa: str, type_of_violence: str):
    """
    Retrieve the list of available metric names from forecast results.

    Note:
        The path parameters are accepted for consistency but are not used internally.

    Returns:
        List[str]: List of metric field names (e.g., 'best', 'p25', 'p50', 'p75').

    Raises:
        HTTPException: If field inspection fails.
    """
    try:
        # Get all field names from ForecastValues as a list of strings
        metrics = list(ForecastValues.__fields__.keys())
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def root():
    """
    Health check endpoint.

    Returns:
        dict: API status message.
    """
    return {"message": "API is running. Use /{run}/{loa}/{type_of_violence}/... endpoints."}