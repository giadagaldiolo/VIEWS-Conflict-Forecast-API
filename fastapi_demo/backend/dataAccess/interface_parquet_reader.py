from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class IParquetReader(ABC):
    """
    Interface for the forecast data repository.

    Any implementation must adhere to this contract to provide forecast data access.
    """

    @abstractmethod
    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return a list of filtered forecast records.

        Each record is a dictionary containing keys such as
        'priogrid_id', 'month_id', 'country_id', 'lat', 'lon', and metric values.

        Args:
            month_ids (Optional[List[int]]): List of month IDs to filter by. Defaults to None.
            priogrid_ids (Optional[List[int]]): List of spatial grid cell IDs to filter by. Defaults to None.
            country_ids (Optional[List[int]]): List of country IDs to filter by. Defaults to None.
            metrics (Optional[List[str]]): List of metric names to include in results. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of forecast records matching the filters.
        """
        pass

    @abstractmethod
    def list_months(self) -> List[int]:
        """
        Return all available month IDs.

        Returns:
            List[int]: List of month identifiers.
        """
        pass

    @abstractmethod
    def list_cells(self) -> List[int]:
        """
        Return all available priogrid IDs.

        Returns:
            List[int]: List of spatial grid cell identifiers.
        """
        pass

    @abstractmethod
    def list_country_ids(self) -> List[int]:
        """
        Return all available country IDs.

        Returns:
            List[int]: List of country identifiers.
        """
        pass
