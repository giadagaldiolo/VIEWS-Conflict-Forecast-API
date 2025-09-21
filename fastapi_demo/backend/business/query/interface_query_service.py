from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class IForecastQueryService(ABC):
    """
    Interface for forecast query services.

    Defines a method to retrieve forecast data filtered by various optional criteria.
    """

    @abstractmethod
    def get_forecasts(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve forecasts based on optional filtering criteria.

        Args:
            month_ids (Optional[List[int]]): List of month IDs to filter forecasts. Defaults to None.
            priogrid_ids (Optional[List[int]]): List of priogrid IDs to filter forecasts. Defaults to None.
            country_ids (Optional[List[int]]): List of country IDs to filter forecasts. Defaults to None.
            metrics (Optional[List[str]]): List of metric names to include. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of forecast records matching the filters.
        """
        pass