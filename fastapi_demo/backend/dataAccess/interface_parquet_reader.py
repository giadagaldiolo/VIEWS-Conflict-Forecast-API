from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class IParquetReader(ABC):
    """
    Interfaccia per il repository delle previsioni.
    Ogni implementazione deve rispettare questo contratto.
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
        Restituisce un elenco di record forecast filtrati.
        Ogni record è un dict con priogrid_id, month_id, country_id, lat, lon e valori delle metriche.
        """
        pass

    @abstractmethod
    def list_months(self) -> List[int]:
        """Restituisce tutti i month_id disponibili"""
        pass

    @abstractmethod
    def list_cells(self) -> List[int]:
        """Restituisce tutti i priogrid_id disponibili"""
        pass

    @abstractmethod
    def list_country_ids(self) -> List[int]:
        """Restituisce tutti i country_id disponibili"""
        pass
