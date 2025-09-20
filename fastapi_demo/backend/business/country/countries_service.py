from typing import List
from dataAccess.interface_parquet_reader import IParquetReader
from business.country.interface_country_service import ICountryService

class CountryService(ICountryService):
    def __init__(self, repository: IParquetReader):
        self.repository = repository

    def get_countries(self) -> List[int]:
        return self.repository.list_country_ids()
