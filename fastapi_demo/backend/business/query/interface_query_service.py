from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class IForecastQueryService(ABC):
    @abstractmethod
    def get_forecasts(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        pass