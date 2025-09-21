from typing import List
from dataAccess.interface_parquet_reader import IParquetReader
from business.month.interface_month_service import IMonthService

class MonthService(IMonthService):
    """
    Service class to handle operations related to months.

    Attributes:
        repository (IParquetReader): Repository interface to read Parquet data.
    """

    def __init__(self, repository: IParquetReader):
        """
        Initialize MonthService with a repository.

        Args:
            repository (IParquetReader): Instance implementing Parquet data reading.
        """
        self.repository = repository

    def get_months(self) -> List[int]:
        """
        Retrieve a list of month IDs from the repository.

        Returns:
            List[int]: List of month identifiers (e.g., 202201 for January 2022).
        """
        return self.repository.list_months()