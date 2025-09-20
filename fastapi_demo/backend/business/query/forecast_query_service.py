from typing import List, Dict, Any, Optional
from backend.dataAccess.interface_parquet_reader import IParquetReader
from forecast_query_service import IForecastQueryService

class ForecastQueryService(IForecastQueryService):
    def __init__(self, repository: IForecastRepository):
        self.repository = repository

    def get_forecasts(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        return self.repository.query(month_ids, priogrid_ids, country_ids, metrics)