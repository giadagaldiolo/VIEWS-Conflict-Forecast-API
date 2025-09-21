from typing import List, Dict, Any, Optional
from dataAccess.interface_parquet_reader import IParquetReader
from business.query.interface_query_service import IForecastQueryService

class ForecastQueryService(IForecastQueryService):
    """
    Service class for querying forecast data with flexible filters.

    Attributes:
        repository (IParquetReader): Repository interface to access forecast data.
    """
    def __init__(self, repository: IParquetReader):
        """
        Initialize ForecastQueryService with a repository.

        Args:
            repository (IParquetReader): Instance implementing forecast data access.
        """
        self.repository = repository

    def get_forecasts(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query forecasts filtered by optional month IDs, priogrid IDs, country IDs, and metrics.

        Args:
            month_ids (Optional[List[int]]): List of month identifiers to filter forecasts. Defaults to None (no filter).
            priogrid_ids (Optional[List[int]]): List of spatial grid cell IDs to filter forecasts. Defaults to None.
            country_ids (Optional[List[int]]): List of country IDs to filter forecasts. Defaults to None.
            metrics (Optional[List[str]]): List of metric names to include in the results. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of forecast records matching the filters, each represented as a dictionary.
        """
        return self.repository.query(month_ids, priogrid_ids, country_ids, metrics)