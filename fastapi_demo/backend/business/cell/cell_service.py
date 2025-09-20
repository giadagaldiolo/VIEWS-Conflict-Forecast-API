from typing import List
from backend.dataAccess.interface_parquet_reader import IParquetReader
from forecast_cell_service import ICellService

class CellService(ICellService):
    def __init__(self, repository: IForecastRepository):
        self.repository = repository

    def get_cells(self) -> List[int]:
        return self.repository.list_priogrid_ids()
