# storage_reader.py
from pathlib import Path
import polars as pl
from typing import Iterator, Dict, Any, Optional, List
from .schemas import FORECAST_SCHEMA


class StorageReader:
    """Interfaccia astratta per lettori di forecast."""

    def list_months(self) -> List[int]:
        raise NotImplementedError

    def list_priogrid_ids(self) -> List[int]:
        raise NotImplementedError

    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None,
    ) -> Iterator[Dict[str, Any]]:
        raise NotImplementedError


class ParquetFlatReader(StorageReader):
    """
    Lettura ottimizzata di parquet forecasts:
    - Join dei file main + HDI all'avvio.
    - Tutte le query successive filtrano il DataFrame in memoria.
    - Streaming dei record via generator.
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.schema = FORECAST_SCHEMA
        self.base_cols = ["priogrid_id", "month_id", "country_id", "lat", "lon", "row", "col"]

        # File parquet
        main_file = self.base_path / "preds_001.parquet"
        hdi_file = self.base_path / "preds_001_90_hdi.parquet"

        # Carica e fai join dei file all'avvio
        df_main = pl.read_parquet(main_file)
        df_hdi = pl.read_parquet(hdi_file)

        self.df = df_main.join(df_hdi, on=["month_id", "priogrid_id"], how="left")

    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Generator che restituisce record filtrati, con eventuale subset di metriche.
        Streaming riga per riga per performance.
        """
        df = self.df

        # Filtri
        if month_ids:
            df = df.filter(pl.col("month_id").is_in(month_ids))
        if priogrid_ids:
            df = df.filter(pl.col("priogrid_id").is_in(priogrid_ids))
        if country_ids:
            df = df.filter(pl.col("country_id").is_in(country_ids))

        # Se metrics specificate, seleziona solo quelle
        if metrics:
            cols = [c for c in metrics if c in df.columns]
            df = df.select(cols)

        # Streaming riga per riga
        for row in df.iter_rows(named=True):
            yield row

    def list_months(self) -> List[int]:
        return sorted(self.df.select("month_id").unique().to_series().to_list())

    def list_priogrid_ids(self) -> List[int]:
        return sorted(self.df.select("priogrid_id").unique().to_series().to_list())

    def list_country_ids(self) -> List[int]:
        """Return all unique country IDs in the dataset"""
        return sorted(self.df.select("country_id").unique().to_series().to_list())
