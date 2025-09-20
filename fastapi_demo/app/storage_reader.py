from pathlib import Path
import polars as pl
from typing import Iterator, Dict, Any, Optional, List

from .schemas import FORECAST_SCHEMA


class StorageReader:
    """Abstract interface for forecast data readers."""

    def list_months(self) -> List[int]:
        raise NotImplementedError

    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Return an iterator of records keyed by (month_id, priogrid_id)."""
        raise NotImplementedError

class ParquetFlatReader(StorageReader):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.schema = FORECAST_SCHEMA
        self.base_cols = ["priogrid_id", "month_id", "country_id", "lat", "lon", "row", "col"]
        self.main_cols = [c for c in FORECAST_SCHEMA if c.startswith("pred_ln_") and "hdi" not in c]
        self.hdi_cols = [c for c in FORECAST_SCHEMA if "hdi" in c]

        # identify files
        self.main_file = self.base_path / "preds_001.parquet"
        self.hdi_file = self.base_path / "preds_001_90_hdi.parquet"

    def _scan(self, metrics: List[str]) -> pl.LazyFrame:
        # decide quale file leggere
        use_hdi = any(c in self.hdi_cols for c in metrics)
        main_metrics = [c for c in metrics if c in self.main_cols or c in self.base_cols]
        lf = pl.scan_parquet(self.main_file).select(main_metrics)

        if use_hdi:
            hdi_metrics = [c for c in metrics if c in self.hdi_cols]
            lf_hdi = pl.scan_parquet(self.hdi_file).select(["month_id", "priogrid_id"] + hdi_metrics)
            lf = lf.join(lf_hdi, on=["month_id", "priogrid_id"], how="left")

        return lf

    def query(
        self,
        month_ids: Optional[List[int]] = None,
        priogrid_ids: Optional[List[int]] = None,
        country_ids: Optional[List[int]] = None,
        metrics: Optional[List[str]] = None,
    ) -> Iterator[Dict[str, Any]]:
        # default: tutte le colonne base + MAP
        if metrics is None:
            metrics = self.base_cols + self.main_cols

        lf = self._scan(metrics)

        # Apply filters
        if month_ids:
            lf = lf.filter(pl.col("month_id").is_in(month_ids))
        if priogrid_ids:
            lf = lf.filter(pl.col("priogrid_id").is_in(priogrid_ids))
        if country_ids:
            lf = lf.filter(pl.col("country_id").is_in(country_ids))

        # Collect and yield row by row
        df = lf.collect()
        for record in df.to_dicts():
            yield record


    def list_priogrid_ids(self) -> List[int]:
        lf = self._scan()
        cells = lf.select("priogrid_id").unique().collect().to_series().to_list()
        return sorted(cells)