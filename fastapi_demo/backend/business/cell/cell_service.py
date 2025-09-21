from typing import List
from dataAccess.interface_parquet_reader import IParquetReader
from business.cell.interface_cell_service import ICellService

class CellService(ICellService):
    def __init__(self, repository: IParquetReader):
        self.repository = repository

    def get_cells(self) -> List[int]:
        return self.repository.list_cells()
