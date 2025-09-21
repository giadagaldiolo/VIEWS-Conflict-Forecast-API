from typing import List
from dataAccess.interface_parquet_reader import IParquetReader
from business.country.interface_country_service import ICountryService

class CountryService(ICountryService):
    """
    Service class to handle operations related to countries.

    Attributes:
        repository (IParquetReader): Repository interface to read Parquet data.
    """

    def __init__(self, repository: IParquetReader):
        """
        Initialize CountryService with a repository.

        Args:
            repository (IParquetReader): Instance implementing Parquet data reading.
        """
        self.repository = repository

    def get_countries(self) -> List[int]:
        """
        Retrieve a list of country IDs from the repository.

        Returns:
            List[int]: List of country IDs.
        """
        return self.repository.list_country_ids()
