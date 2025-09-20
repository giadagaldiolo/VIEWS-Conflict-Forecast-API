from typing import List
from backend.dataAccess.interface_parquet_reader import IParquetReader
from forecast_month_service import IMonthService

class MonthService(IMonthService):
    def __init__(self, repository: IForecastRepository):
        self.repository = repository

    def get_months(self) -> List[int]:
        return self.repository.list_months()