from typing import List
from dataAccess.interface_parquet_reader import IParquetReader
from business.cell.interface_cell_service import ICellService

class CellService(ICellService):
    """
    Service class to handle operations related to spatial cells.
    """

    def __init__(self, repository: IParquetReader):
        """
        Initialize CellService with a repository.

        Args:
            repository (IParquetReader): Instance implementing Parquet data reading.
        """
        self.repository = repository

    def get_cells(self) -> List[int]:
        """
        Retrieve a list of priogrid IDs from the repository.

        Returns:
            List[int]: List of priogrid IDs.
        """
        return self.repository.list_priogrid_ids()
