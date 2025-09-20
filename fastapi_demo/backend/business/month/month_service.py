from typing import List
from dataAccess.interface_parquet_reader import IParquetReader
from business.month.interface_month_service import IMonthService

class MonthService(IMonthService):
    def __init__(self, repository: IParquetReader):
        self.repository = repository

    def get_months(self) -> List[int]:
        return self.repository.list_months()