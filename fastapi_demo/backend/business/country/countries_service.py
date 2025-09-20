from typing import List
from backend.dataAccess.interface_parquet_reader import IParquetReader
from forecast_country_service import ICountryService

class CountryService(ICountryService):
    def __init__(self, repository: IForecastRepository):
        self.repository = repository

    def get_countries(self) -> List[int]:
        return self.repository.list_country_ids()
