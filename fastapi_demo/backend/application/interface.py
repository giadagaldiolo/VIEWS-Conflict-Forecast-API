from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IForecastRepository(ABC):
    """Interfaccia per il repository di forecast"""

    @abstractmethod
    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def list_months(self) -> List[int]:
        pass

    @abstractmethod
    def list_priogrid_ids(self) -> List[int]:
        pass

    @abstractmethod
    def list_country_ids(self) -> List[int]:
        pass
